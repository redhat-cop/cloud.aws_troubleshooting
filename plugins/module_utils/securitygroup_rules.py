#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ipaddress import ip_network, ip_address
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.exception import (
    TrafficNotAllowedError,
    ValidationError,
)
from ansible.module_utils._text import to_text


def evaluate_security_groups(events):
    def evaluate_security_group_rules_basedon_cidr(
        sg_rules, remote_cidrs, remote_sg, protocol, port, sg_id
    ):
        required_cidrs = list(remote_cidrs)
        for rule in sg_rules:
            if (
                rule["IpProtocol"] == protocol
                and port in range(rule["FromPort"], rule["ToPort"] + 1)
            ) or (rule["IpProtocol"] == "-1"):
                for group in rule["UserIdGroupPairs"]:
                    if group["GroupId"] in remote_sg:
                        return True
                for remote_cidr in remote_cidrs:
                    for cidrs in rule["IpRanges"]:
                        if ip_network(cidrs["CidrIp"], strict=False).overlaps(
                            ip_network(remote_cidr, strict=False)
                        ):
                            required_cidrs.remove(remote_cidr)
                            break
        if len(required_cidrs) > 0:
            raise ValidationError(
                "Security group {} is not allowing {} traffic to/from IP ranges {} for port(s) {}.".format(
                    sg_id, protocol, required_cidrs, port
                )
            )
        return True

    def evaluate_security_group_rules_basedon_ip(
        sg_rules, remote_ip, remote_sg, protocol, port, sg_id
    ):
        for rule in sg_rules:
            if (
                rule["IpProtocol"] == protocol
                and port in range(rule["FromPort"], rule["ToPort"] + 1)
            ) or (rule["IpProtocol"] == "-1"):
                for group in rule["UserIdGroupPairs"]:
                    if group["GroupId"] in remote_sg:
                        return True
                for cidrs in rule["IpRanges"]:
                    if ip_address(remote_ip) in ip_network(
                        cidrs["CidrIp"], strict=False
                    ):
                        return True
        raise ValidationError(
            "Security group {} is not allowing {} traffic to/from IP {} for port(s) {}.".format(
                sg_id, protocol, remote_ip, port
            )
        )

    try:
        # RDS Info
        dbPort = events["RDSEndpointPort"]
        ingressRules = events["RDSSecurityGroups"]
        dbSecurityGroup = events["RDSSecurityGroupIds"]
        dbSubnetCidrs = events["RDSSubnetCidrs"]

        # EC2 Instance Info
        ec2InstanceIP = events["EC2InstanceIPs"][0]
        egressRules = events["EC2SecurityGroups"]
        ec2InstanceSecurityGroup = events["EC2SecurityGroupIds"]

        # Verify Egress traffic from EC2 Instance to RDS subnets
        for egressRule in egressRules:
            result = evaluate_security_group_rules_basedon_cidr(
                egressRule["IpPermissionsEgress"],
                dbSubnetCidrs,
                dbSecurityGroup,
                "tcp",
                dbPort,
                egressRule["GroupId"],
            )
            if result:
                break
        if not result:
            raise TrafficNotAllowedError(
                "Please review security group(s) {} for rules allowing egress TCP traffic to port {}".format(
                    ec2InstanceSecurityGroup, dbPort
                )
            )

        # Verify Ingress traffic to RDS from EC2 Instance IP
        for ingressRule in ingressRules:
            result = evaluate_security_group_rules_basedon_ip(
                ingressRule["IpPermissions"],
                ec2InstanceIP,
                ec2InstanceSecurityGroup,
                "tcp",
                dbPort,
                ingressRule["GroupId"],
            )
            if result:
                break
        if not result:
            raise TrafficNotAllowedError(
                "Please review security group(s) {} for rules allowing ingress TCP traffic from port {}".format(
                    dbSecurityGroup, dbPort
                )
            )

        return "Security Group validation successful"

    except TrafficNotAllowedError:
        raise

    except Exception as err:
        raise ValidationError(to_text(err))
