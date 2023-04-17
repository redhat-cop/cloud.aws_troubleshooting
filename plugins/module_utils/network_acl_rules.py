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
    TroubleShootingError,
)
from ansible.module_utils._text import to_text


def evaluate_network_acls(events):
    def evaluate_traffic_basedon_cidr(
        acl_entries, egress, required_ports, remote_cidr, acl_id
    ):
        allowed_ports = []
        denied_ports = []
        allowed_cidrs = {}
        denied_cidrs = {}
        try:
            for port in required_ports:
                if not (port in allowed_ports or port in denied_ports):
                    for entry in acl_entries:
                        if not (port in allowed_ports or port in denied_ports):
                            if entry["Egress"] == egress:
                                if (
                                    entry["Protocol"] == "-1"
                                    or entry["Protocol"] == required_ports[port]
                                ):
                                    for cidr in remote_cidr:
                                        if not (
                                            port in allowed_ports
                                            or port in denied_ports
                                        ):
                                            if ip_network(
                                                entry["CidrBlock"], strict=False
                                            ).overlaps(ip_network(cidr, strict=False)):
                                                if "PortRange" in entry.keys():
                                                    if port in range(
                                                        entry["PortRange"]["From"],
                                                        entry["PortRange"]["To"] + 1,
                                                    ):
                                                        if (
                                                            entry["RuleAction"]
                                                            == "allow"
                                                        ):
                                                            allowed_ports.append(port)
                                                            allowed_cidrs[port] = [
                                                                entry["CidrBlock"],
                                                                entry["RuleNumber"],
                                                            ]
                                                        else:
                                                            denied_ports.append(port)
                                                            denied_cidrs[port] = [
                                                                entry["CidrBlock"],
                                                                entry["RuleNumber"],
                                                            ]
                                                    else:
                                                        continue
                                                else:
                                                    if entry["RuleAction"] == "allow":
                                                        allowed_ports.append(port)
                                                        allowed_cidrs[port] = [
                                                            entry["CidrBlock"],
                                                            entry["RuleNumber"],
                                                        ]
                                                        break
                                                    else:
                                                        denied_ports.append(port)
                                                        denied_cidrs[port] = [
                                                            entry["CidrBlock"],
                                                            entry["RuleNumber"],
                                                        ]
                                                        break
                                            else:
                                                continue
                                        else:
                                            break
                                else:
                                    continue
                            else:
                                continue
                        else:
                            break
                else:
                    continue

                continue
            if len(denied_ports) > 0:
                raise TrafficNotAllowedError(
                    "Network acl {} is not allowing traffic for port(s) {}".format(
                        acl_id, denied_ports
                    )
                )
        except Exception as err:
            raise ValidationError(to_text(err))

    def evaluate_traffic_basedon_ip(
        acl_entries, egress, required_ports, remote_ips, acl_id
    ):
        allowed_ports = []
        denied_ports = []
        allowed_ips = {}
        denied_ips = {}
        try:
            for port in required_ports:
                if not (port in allowed_ports or port in denied_ports):
                    for entry in acl_entries:
                        if not (port in allowed_ports or port in denied_ports):
                            if entry["Egress"] == egress:
                                if (
                                    entry["Protocol"] == "-1"
                                    or entry["Protocol"] == required_ports[port]
                                ):
                                    for ip in remote_ips:
                                        if not (
                                            port in allowed_ports
                                            or port in denied_ports
                                        ):
                                            if ip_address(ip) in ip_network(
                                                entry["CidrBlock"], strict=False
                                            ):
                                                if "PortRange" in entry.keys():
                                                    if port in range(
                                                        entry["PortRange"]["From"],
                                                        entry["PortRange"]["To"] + 1,
                                                    ):
                                                        if (
                                                            entry["RuleAction"]
                                                            == "allow"
                                                        ):
                                                            allowed_ports.append(port)
                                                            allowed_ips[port] = [
                                                                entry["CidrBlock"],
                                                                entry["RuleNumber"],
                                                            ]
                                                        else:
                                                            denied_ports.append(port)
                                                            denied_ips[port] = [
                                                                entry["CidrBlock"],
                                                                entry["RuleNumber"],
                                                            ]
                                                    else:
                                                        continue
                                                else:
                                                    if entry["RuleAction"] == "allow":
                                                        allowed_ports.append(port)
                                                        allowed_ips[port] = [
                                                            entry["CidrBlock"],
                                                            entry["RuleNumber"],
                                                        ]
                                                        break
                                                    else:
                                                        denied_ports.append(port)
                                                        denied_ips[port] = [
                                                            entry["CidrBlock"],
                                                            entry["RuleNumber"],
                                                        ]
                                                        break
                                            else:
                                                continue
                                        else:
                                            break
                                else:
                                    continue
                            else:
                                continue
                        else:
                            break
                else:
                    continue

                continue
            if len(denied_ports) > 0:
                raise TrafficNotAllowedError(
                    "Network acl {} is not allowing traffic for port(s) {}".format(
                        acl_id, denied_ports
                    )
                )
        except Exception as err:
            raise ValidationError(to_text(err))

    try:
        # RDS Info
        reqPorts = {events["RDSEndpointPort"]: "6"}
        rdsNacls = events["RDSNetworkAclRules"]
        rdsCidrs = events["RDSSubnetCidrs"]

        # EC2 Instance Info
        ec2Nacls = events["EC2NetworkAclRules"]
        ec2InstanceIPs = events["EC2InstanceIPs"]

        # Verify Egress traffic from EC2 Instance to RDS subnets
        for acl in ec2Nacls:
            try:
                evaluate_traffic_basedon_cidr(
                    acl["Entries"], True, reqPorts, rdsCidrs, acl["NetworkAclId"]
                )
            except TroubleShootingError as err:
                raise TrafficNotAllowedError(
                    "Please review network acl {0} for egress rules allowing port(s) {1}".format(
                        acl["NetworkAclId"], to_text(err)
                    )
                )

        # Verify Ingress traffic to RDS from EC2 Instance IP
        for acl in rdsNacls:
            try:
                evaluate_traffic_basedon_ip(
                    acl["Entries"], False, reqPorts, ec2InstanceIPs, acl["NetworkAclId"]
                )
            except TroubleShootingError as err:
                raise TrafficNotAllowedError(
                    "Please review network acl {0} for ingress rules allowing port(s) {1}".format(
                        acl["NetworkAclId"], to_text(err)
                    )
                )

        return "Network ACL validation successful"

    except Exception as err:
        raise ValidationError(to_text(err))
