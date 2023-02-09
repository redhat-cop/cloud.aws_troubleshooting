#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: validate_security_group_rules
short_description: Evaluates Security group Rules
author:
  - Aubin Bikouo (@abikouo)
description:
  - Compare the Source to Destination Security group Rules.
  - Source can be an EC2 instance trying to connect to an RDS instance (Destination).

options:
  dest_subnet_cidrs:
    description:
    - Destination Subnets CIDRs.
    type: list
    elements: str
    required: true
  dest_security_groups:
    description:
    - Destination Security Groups Rules.
    type: list
    elements: dict
    required: true
  dest_port:
    description:
    - Destination Endpoint Port.
    type: str
    required: true
  protocol:
    description:
    - Protocol to evaluate Security Group.
    type: str
    default: tcp
  src_security_groups:
    description:
    - Source Security Groups Rules.
    type: list
    elements: dict
    required: true
  src_private_ip:
    description:
    - Source Private IP.
    type: str
    elements: str
    required: true

"""

EXAMPLES = r"""
- name: Evaluate Security group rules from EC2 instance to RDS Instance
  cloud.aws_troubleshooting.validate_security_group_rules:
    dest_subnet_cidrs:
        - 10.1.0.0/24
        - 10.1.2.0/24
    dest_security_groups:
        - description: "Security group for EC2 instance"
          group_id: "sg-0bd2d9a14af754812"
          group_name: "aubin-sg"
          ip_permissions:
            - from_port: 5432
              to_port: 5432
              ip_protocol: "tcp"
              ip_ranges":
                - cidr_ip: "0.0.0.0/0"
              ipv6_ranges: []
              prefix_list_ids: []
              user_id_group_pairs: []
          ip_permissions_egress:
            - ip_protocol": -1
              ip_ranges:
                - cidr_ip: "0.0.0.0/0"
              ipv6_ranges: []
              prefix_list_ids: []
              user_id_group_pairs: []
          owner_id: "0000000000000"
          vpc_id: "vpc-0bee28efef41e1de4"
    dest_port: 5432
    src_security_groups:
        - description: "Security group for EC2 instance"
          group_id: "sg-0bd2d9a14af8a8998"
          group_name: "aubin-sg"
          ip_permissions:
            - from_port: 22
              to_port: 22
              ip_protocol: "tcp"
              ip_ranges":
                - cidr_ip: "0.0.0.0/0"
              ipv6_ranges: []
              prefix_list_ids: []
              user_id_group_pairs: []
          ip_permissions_egress:
            - ip_protocol": -1
              ip_ranges:
                - cidr_ip: "0.0.0.0/0"
              ipv6_ranges: []
              prefix_list_ids: []
              user_id_group_pairs: []
          owner_id: "0000000000000"
          vpc_id: "vpc-0bee28efef41e1de4"
    src_private_ip: "172.10.3.10"

"""

RETURN = r"""
result:
  type: str
  description: Results from comparing the Source security group rules to the Destination security group rules
  returned: success
  sample: 'Security Group validation successful'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.exception import (
    TroubleShootingError,
)
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.securitygroup_rules import (
    evaluate_security_groups,
)
from ansible.module_utils._text import to_text


class ValidateSecurityGroupRules(AnsibleModule):
    def __init__(self):

        argument_spec = dict(
            dest_subnet_cidrs=dict(type="list", elements="str", required=True),
            dest_security_groups=dict(type="list", elements="dict", required=True),
            dest_port=dict(type="list", elements="int", required=True),
            src_security_groups=dict(type="list", elements="dict", required=True),
            src_private_ip=dict(type="list", elements="str", required=True),
            protocol=dict(type="str", default="tcp"),
        )

        super(ValidateSecurityGroupRules, self).__init__(argument_spec=argument_spec)

        self.execute_module()

    def execute_module(self):

        events = {}
        events["RDSSecurityGroupIds"] = [
            grp["group_id"] for grp in self.params.get("dest_security_groups")
        ]
        events["RDSSecurityGroups"] = [
            snake_dict_to_camel_dict(grp, capitalize_first=True)
            for grp in self.params.get("dest_security_groups")
        ]
        events["RDSSubnetCidrs"] = self.params.get("dest_subnet_cidrs")
        events["RDSEndpointPort"] = self.params.get("dest_port")[0]
        events["EC2SecurityGroupIds"] = [
            grp["group_id"] for grp in self.params.get("src_security_groups")
        ]
        events["EC2SecurityGroups"] = [
            snake_dict_to_camel_dict(grp, capitalize_first=True)
            for grp in self.params.get("src_security_groups")
        ]
        events["EC2InstanceIPs"] = self.params.get("src_private_ip")

        try:
            result = evaluate_security_groups(events)
            self.exit_json(msg=result)

        except TroubleShootingError as err:
            self.fail_json(
                msg="Security Group validation failed: {0}".format(to_text(err))
            )


def main():

    ValidateSecurityGroupRules()


if __name__ == "__main__":
    main()
