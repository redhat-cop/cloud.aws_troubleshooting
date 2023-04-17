#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: validate_network_acls
short_description: Evaluates network ACLs
author:
  - Aubin Bikouo (@abikouo)
description:
  - Compare the Source to Destination network ACLs.
  - Source can be an EC2 instance trying to connect to an RDS instance (Destination).

options:
  dest_subnet_cidrs:
    description:
    - Destination Subnet CIDRs.
    type: list
    elements: str
    required: true
  dest_network_acl_rules:
    description:
    - Destination Network ACL Rules.
    type: list
    elements: dict
    required: true
  dest_port:
    description:
    - Destination Endpoint Ports.
    type: list
    elements: int
    required: true
  src_network_acl_rules:
    description:
    - Source Network ACL Rules.
    type: list
    elements: dict
    required: true
  src_private_ip:
    description:
    - Source Private IP.
    type: list
    elememts: str
    required: true

"""

EXAMPLES = r"""
- name: Evaluate network ACLS from EC2 instance to RDS Instance
  cloud.aws_troubleshooting.validate_network_acls:
    dest_subnet_cidrs:
        - 10.1.0.0/24
        - 10.1.2.0/24
    dest_network_acl_rules:
        - egress:
            - [100, "all", "allow", "0.0.0.0/0", null, null, 0, 65535]
          ingress:
            - [100, "all", "allow", "0.0.0.0/0", null, null, 0, 65535]
          is_default: true
          nacl_id: "acl-01124846ef9f50ff2"
          owner_id: "000000000000"
          subnets:
            - "subnet-0af56e0d353f88cb8"
            - "subnet-032f1a2598b6318ed"]
          vpc_id: "vpc-0274c44deffd7368a
    dest_port:
        - 5432
    src_network_acl_rules:
        - egress:
            - [100, "all", "allow", "0.0.0.0/0", null, null, 0, 65535]
          ingress:
            - [100, "all", "allow", "0.0.0.0/0", null, null, 0, 65535]
          is_default: true
          nacl_id: "acl-01124846ef9f50ff2"
          owner_id: "000000000000"
          subnets:
            - subnet-0af56e0d353f88cb8
            - subnet-032f1a2598b6318ed
          vpc_id: "vpc-0274c44deffd7368a"
    src_private_ip:
        - 172.10.3.10

"""

RETURN = r"""
result:
  type: str
  description: Results from comparing the Source network ACLs to the Destination network ACLs.
  returned: success
  sample: 'Network ACL validation successful'
"""

from collections import namedtuple
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.exception import (
    TroubleShootingError,
)
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.network_acl_rules import (
    evaluate_network_acls,
)
from ansible.module_utils._text import to_text

# NACL Entry format
# [
#   100,            -> Rule number
#   "all",          -> protocol
#   "allow",        -> Rule action
#   "0.0.0.0/0",    -> CIDR block
#   null,           -> icmp type
#   null,           -> icmp code
#   0,              -> port range from
#   65535           -> port range to
# ]
NACLEntry = namedtuple(
    "NACLEntry",
    [
        "rule_number",
        "protocol",
        "rule_action",
        "cidr_block",
        "icmp_type",
        "icmp_code",
        "port_range_from",
        "port_range_to",
    ],
)


def ansible_to_amazon_acl(acl):
    result = snake_dict_to_camel_dict(acl, capitalize_first=True)
    result["Associations"] = result["Subnets"]
    result["NetworkAclId"] = result["NaclId"]
    result["Entries"] = [
        {
            "CidrBlock": entry[3],
            "Egress": True,
            "Protocol": entry[1],
            "RuleAction": entry[2],
            "RuleNumber": entry[0],
            "PortRange": {"From": entry[6], "To": entry[6]},
        }
        for entry in result["Egress"]
    ]

    result["Entries"] += [
        {
            "CidrBlock": entry[3],
            "Egress": False,
            "Protocol": entry[1],
            "RuleAction": entry[2],
            "RuleNumber": entry[0],
            "PortRange": {"From": entry[6], "To": entry[6]},
        }
        for entry in result["Ingress"]
    ]

    return result


class ValidateNetworkACL(AnsibleModule):
    def __init__(self):

        argument_spec = dict(
            dest_subnet_cidrs=dict(type="list", elements="str", required=True),
            dest_network_acl_rules=dict(type="list", elements="dict", required=True),
            dest_port=dict(type="list", elements="int", required=True),
            src_network_acl_rules=dict(type="list", elements="dict", required=True),
            src_private_ip=dict(type="list", elements="str", required=True),
        )

        super(ValidateNetworkACL, self).__init__(argument_spec=argument_spec)

        for key in argument_spec:
            setattr(self, key, self.params.get(key))

        self.execute_module()

    def execute_module(self):

        try:
            events = self.build_events()
            result = evaluate_network_acls(events)
            self.exit_json(msg=result)

        except TroubleShootingError as err:
            self.fail_json(msg="Network validation failed: {0}".format(to_text(err)))

    def build_events(self):

        events = {}
        events["EC2InstanceIPs"] = self.src_private_ip
        events["EC2NetworkAclRules"] = [
            ansible_to_amazon_acl(acl) for acl in self.src_network_acl_rules
        ]
        events["RDSEndpointPort"] = self.dest_port[0]
        events["RDSSubnetCidrs"] = self.dest_subnet_cidrs
        events["RDSNetworkAclRules"] = [
            ansible_to_amazon_acl(acl) for acl in self.dest_network_acl_rules
        ]
        return events


def main():

    ValidateNetworkACL()


if __name__ == "__main__":
    main()
