#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: validate_route_tables
short_description: Evaluates Route tables
author:
  - Aubin Bikouo (@abikouo)
description:
  - Compare the Source to Destination routes.
  - Source can be an EC2 instance trying to connect to an RDS instance (Destination).

options:
  dest_subnets:
    description:
    - Destination Subnet.
    type: list
    elements: dict
    required: true
  dest_route_tables:
    description:
    - Destination Route Tables.
    type: list
    elements: dict
    required: true
  dest_vpc_route_tables:
    description:
    - Destination Route Tables.
    type: list
    elements: dict
    required: true
  src_subnets:
    description:
    - Source Subnets.
    type: list
    elements: dict
    required: true
  src_private_ip:
    description:
    - Source Private IPs.
    type: list
    elements: str
    required: true
  src_route_tables:
    description:
    - Source Route Tables.
    type: list
    elements: dict
    required: true
  src_vpc_route_tables:
    description:
    - Source Route Tables.
    type: list
    elements: dict
    required: true

"""

EXAMPLES = r"""
- name: Evaluate routes from EC2 instance to RDS Instance
  cloud.aws_troubleshooting.validate_route_tables:
    dest_subnets:
        - assign_ipv6_address_on_creation": false
          availability_zone: "eu-west-2b"
          availability_zone_id: "euw2-az3"
          available_ip_address_count: 250
          cidr_block: "172.10.2.0/24"
          default_for_az: false
          enable_dns64: false
          id: "subnet-032f1a2598b6318ed"
          ipv6_cidr_block_association_set: []
          ipv6_native": false
          map_customer_owned_ip_on_launch: false
          map_public_ip_on_launch: false
          owner_id": "00000000000"
          private_dns_name_options_on_launch:
            enable_resource_name_dns_a_record: false
            enable_resource_name_dns_aaaa_record": false
            hostname_type": "ip-name"
          state: "available"
          subnet_arn: "arn:aws:ec2:eu-west-2:721066863947:subnet/subnet-032f1a2598b6318ed"
          subnet_id: "subnet-032f1a2598b6318ed"
          vpc_id: "vpc-0274c44deffd7368a"
        - assign_ipv6_address_on_creation": false
          availability_zone: "eu-west-2a"
          availability_zone_id: "euw2-az2"
          available_ip_address_count: 250
          cidr_block: "172.10.1.0/24"
          default_for_az: false
          enable_dns64: false
          id: "subnet-0af56e0d353f88cb8"
          ipv6_cidr_block_association_set: []
          ipv6_native": false
          map_customer_owned_ip_on_launch: false
          map_public_ip_on_launch: false
          owner_id": "00000000000"
          private_dns_name_options_on_launch:
            enable_resource_name_dns_a_record: false
            enable_resource_name_dns_aaaa_record": false
            hostname_type": "ip-name"
          state: "available"
          subnet_arn: "arn:aws:ec2:eu-west-2:721066863947:subnet/subnet-0af56e0d353f88cb8"
          subnet_id: "subnet-0af56e0d353f88cb8"
          vpc_id: "vpc-0274c44deffd7368a"
    dest_route_tables:
        - associations:
            - association_state:
                state: "associated"
              id: "rtbassoc-0c5c333773772843b"
              main: false
              route_table_association_id: "rtbassoc-0c5c333773772843b"
              route_table_id: "rtb-07a81d1afe14a009c"
              subnet_id: "subnet-0ab63680e1e0316e2"
          id: "rtb-07a81d1afe14a009c"
          owner_id: "721066863947"
          propagating_vgws: []
          route_table_id: "rtb-07a81d1afe14a009c"
          routes:
            - destination_cidr_block: "10.1.0.0/16"
              gateway_id: "local"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRouteTable"
              state: "active"
            - destination_cidr_block: "0.0.0.0/0"
              gateway_id: "igw-057753b539008784c"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRoute"
              state": "active"
          vpc_id": "vpc-0bee28efef41e1de4"
    dest_vpc_route_tables:
        - associations:
            - association_state:
                state: "associated"
              id: "rtbassoc-0c5c333773772843b"
              main: false
              route_table_association_id: "rtbassoc-0c5c333773772843b"
              route_table_id: "rtb-07a81d1afe14a009c"
              subnet_id: "subnet-0ab63680e1e0316e2"
          id: "rtb-07a81d1afe14a009c"
          owner_id: "721066863947"
          propagating_vgws: []
          route_table_id: "rtb-07a81d1afe14a009c"
          routes:
            - destination_cidr_block: "10.1.0.0/16"
              gateway_id: "local"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRouteTable"
              state: "active"
            - destination_cidr_block: "0.0.0.0/0"
              gateway_id: "igw-057753b539008784c"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRoute"
              state": "active"
          vpc_id": "vpc-0bee28efef41e1de4"
    src_subnets:
        - assign_ipv6_address_on_creation": false
          availability_zone: "eu-west-2a"
          availability_zone_id: "euw2-az2"
          available_ip_address_count: 250
          cidr_block: "172.10.1.0/24"
          default_for_az: false
          enable_dns64: false
          id: "subnet-0af56e0d353f88cb8"
          ipv6_cidr_block_association_set: []
          ipv6_native": false
          map_customer_owned_ip_on_launch: false
          map_public_ip_on_launch: false
          owner_id": "00000000000"
          private_dns_name_options_on_launch:
            enable_resource_name_dns_a_record: false
            enable_resource_name_dns_aaaa_record": false
            hostname_type": "ip-name"
          state: "available"
          subnet_arn: "arn:aws:ec2:eu-west-2:721066863947:subnet/subnet-0af56e0d353f88cb8"
          subnet_id: "subnet-0af56e0d353f88cb8"
          vpc_id: "vpc-0274c44deffd7368a"
    src_private_ip:
        - 172.0.1.4
    src_route_tables:
        - associations:
            - association_state:
                state: "associated"
              id: "rtbassoc-0c5c333773772843b"
              main: false
              route_table_association_id: "rtbassoc-0c5c333773772843b"
              route_table_id: "rtb-07a81d1afe14a009c"
              subnet_id: "subnet-0ab63680e1e0316e2"
          id: "rtb-07a81d1afe14a009c"
          owner_id: "721066863947"
          propagating_vgws: []
          route_table_id: "rtb-07a81d1afe14a009c"
          routes:
            - destination_cidr_block: "10.1.0.0/16"
              gateway_id: "local"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRouteTable"
              state: "active"
            - destination_cidr_block: "0.0.0.0/0"
              gateway_id: "igw-057753b539008784c"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRoute"
              state": "active"
          vpc_id": "vpc-0bee28efef41e1de4"
    src_vpc_route_tables
        - associations:
            - association_state:
                state: "associated"
              id: "rtbassoc-0c5c333773772843b"
              main: false
              route_table_association_id: "rtbassoc-0c5c333773772843b"
              route_table_id: "rtb-07a81d1afe14a009c"
              subnet_id: "subnet-0ab63680e1e0316e2"
          id: "rtb-07a81d1afe14a009c"
          owner_id: "721066863947"
          propagating_vgws: []
          route_table_id: "rtb-07a81d1afe14a009c"
          routes:
            - destination_cidr_block: "10.1.0.0/16"
              gateway_id: "local"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRouteTable"
              state: "active"
            - destination_cidr_block: "0.0.0.0/0"
              gateway_id: "igw-057753b539008784c"
              instance_id: null
              interface_id: null
              network_interface_id: null
              origin: "CreateRoute"
              state": "active"
          vpc_id": "vpc-0bee28efef41e1de4"

"""

RETURN = r"""
result:
  type: str
  description: Results from comparing the Source route table to the Destination routes.
  returned: success
  sample: 'Route table validation successful'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import snake_dict_to_camel_dict
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.exception import (
    TroubleShootingError,
)
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.route_table_entries import (
    evaluate_route_tables,
)
from ansible.module_utils._text import to_text


class ValidateRouteTables(AnsibleModule):
    def __init__(self):

        argument_spec = dict(
            dest_subnets=dict(type="list", elements="dict", required=True),
            dest_route_tables=dict(type="list", elements="dict", required=True),
            dest_vpc_route_tables=dict(type="list", elements="dict", required=True),
            src_subnets=dict(type="list", elements="dict", required=True),
            src_private_ip=dict(type="list", elements="str", required=True),
            src_route_tables=dict(type="list", elements="dict", required=True),
            src_vpc_route_tables=dict(type="list", elements="dict", required=True),
        )

        super(ValidateRouteTables, self).__init__(argument_spec=argument_spec)

        self.execute_module()

    def execute_module(self):

        events = {}
        events["EC2InstanceIPs"] = self.params.get("src_private_ip")
        events["EC2SubnetId"] = self.params.get("src_subnets")[0].get("id")
        events["EC2RouteTables"] = [
            snake_dict_to_camel_dict(r, capitalize_first=True)
            for r in self.params.get("src_route_tables")
        ]
        events["EC2VpcRouteTables"] = [
            snake_dict_to_camel_dict(r, capitalize_first=True)
            for r in self.params.get("src_vpc_route_tables")
        ]
        events["EC2VpcId"] = self.params.get("src_subnets")[0].get("vpc_id")
        events["RDSSubnetCidrs"] = [
            s.get("cidr_block") for s in self.params.get("dest_subnets")
        ]
        events["RDSSubnetIds"] = [s.get("id") for s in self.params.get("dest_subnets")]
        events["RDSRouteTables"] = [
            snake_dict_to_camel_dict(r, capitalize_first=True)
            for r in self.params.get("dest_route_tables")
        ]
        events["RDSVpcId"] = self.params.get("dest_subnets")[0].get("vpc_id")
        events["RDSVpcRouteTables"] = [
            snake_dict_to_camel_dict(r, capitalize_first=True)
            for r in self.params.get("dest_vpc_route_tables")
        ]

        try:
            result = evaluate_route_tables(events)
            self.exit_json(msg=result)

        except TroubleShootingError as err:
            self.fail_json(
                msg="Route table validation failed: {0}".format(to_text(err))
            )


def main():

    ValidateRouteTables()


if __name__ == "__main__":
    main()
