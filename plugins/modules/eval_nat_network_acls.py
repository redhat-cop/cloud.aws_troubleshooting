#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: eval_nat_network_acls
short_description: Evaluate ingress and egress NAT network ACLs
description:
  - Evaluate ingress and egress NAT network ACLs.
  - Confirms whether the NACLs allow the needed traffic between the source and destination resources.
author:
  - Alina Buzachis (@alinabuzachis)
options:
  src_ip:
    description:
    - The private IPv4 address of the AWS resource in your Amazon VPC you want to test connectivity from.
    type: str
    required: true
  src_subnet_id:
    description:
    - Source Subnet id.
    type: str
    required: true
  src_port_range:
    description:
    - The port range used by the AWS resource in your Amazon VPC you want to test connectivity from.
    type: str
  dst_ip:
    description:
    - The IPv4 address of the resource you want to connect to.
    type: str
    required: true
  dst_port:
    description:
    - The port number you want to connect to on the destination resource.
    type: str
    required: true
  nat_subnet_id:
    description:
    - NAT Subnet id.
    type: str
    required: true
  nat_network_acls:
    description:
    - NAT network ACLs.
    type: list
    elements: dict
    required: true
  routes:
    description:
    - NAT routes.
    type: list
    elements: dict
    required: true
"""


EXAMPLES = r"""
- name: Evaluate ingress and egress NAT network ACLs
  cloud.aws_troubleshooting.eval_nat_network_acls:
    dst_ip: "8.8.8.8"
    dst_port: 80
    nat_network_acls:
      - egress:
          - - 100
            - "all"
            - "allow"
            - "0.0.0.0/0"
            - null
            - null
            - 0
            - 65535
      - ingress:
          - - 100
            - "all"
            - "allow"
            - "0.0.0.0/0"
            - null
            - null
            - 0
            - 65535
    nat_subnet_id: "subnet-0ffc739798db41a1c"
    routes:
      - destination_cidr_block: "192.168.0.0/24"
        gateway_id: "local"
        instance_id: null
        interface_id: null
        network_interface_id: null
        origin: "CreateRouteTable"
        state: "active"
      - destination_cidr_block: "0.0.0.0/0"
        gateway_id: "igw-0b9da14cbd81d415c"
        instance_id: null
        interface_id: null
        network_interface_id: null
        origin: "CreateRoute"
        state: "active"
    src_ip: "192.168.0.28"
    src_subnet_id: "subnet-05ad2d0f8648dfb41"
"""


RETURN = r"""
result:
  type: str
  description: Results from evaluating NAT network ACLS.
  returned: success
  sample: 'NAT Network ACLs evaluation successful'
"""


from ipaddress import ip_address, ip_network

from ansible.module_utils.basic import AnsibleModule


class EvalNatNetworkAcls(AnsibleModule):
    def __init__(self):
        argument_spec = dict(
            src_ip=dict(type="str", required=True),
            src_port_range=dict(type="str"),
            src_subnet_id=dict(type="str", required=True),
            dst_ip=dict(type="str", required=True),
            dst_port=dict(type="str", required=True),
            nat_subnet_id=dict(type="str", required=True),
            nat_network_acls=dict(type="list", elements="dict", required=True),
            routes=dict(type="list", elements="dict", required=True),
        )

        super(EvalNatNetworkAcls, self).__init__(argument_spec=argument_spec)

        for key in argument_spec:
            setattr(self, key, self.params.get(key))

        self.execute_module()

    def eval_nat_nacls(self):
        src_ip = ip_address(self.src_ip)
        dst_ip = ip_address(self.dst_ip)
        dst_port = int(self.dst_port)
        src_port_from = None
        src_port_to = None
        # entry list format
        keys = [
            "rule_number",
            "protocol",
            "rule_action",
            "cidr_block",
            "icmp_type",
            "icmp_code",
            "port_from",
            "port_to",
        ]
        if self.src_port_range:
            src_port_from = int(self.src_port_range.split("-")[0])
            src_port_to = int(self.src_port_range.split("-")[1])

        egress_acls = [acl["egress"] for acl in self.nat_network_acls if acl["egress"]][0]
        ingress_acls = [acl["ingress"] for acl in self.nat_network_acls if acl["ingress"]][0]

        def check_egress_towards_dst(acls, dst_ip, dst_port):
            for item in acls:
                acl = dict(zip(keys, item))
                # Check ipv4 acl rule only
                if acl.get("cidr_block"):
                    # Check IP
                    if dst_ip in ip_network(acl["cidr_block"], strict=False):
                        # Check Port
                        if (acl.get("protocol") == "all") or (
                            dst_port
                            in range(
                                acl["port_from"],
                                acl["port_to"] + 1,
                            )
                        ):
                            # Check Action
                            if acl["rule_action"] == "allow":
                                break
                            else:
                                self.fail_json(
                                    msg=f"NatGateway Subnet {self.src_subnet_id}\
                                       Network Acl Egress Rules do not allow\
                                       outbound traffic to destination: \
                                       {self.dst_ip} : {str(dst_port)}"
                                )

            self.fail_json(
                msg="NatGateway Subnet {0} Network Acl Egress Rules do not allow outbound traffic to destination: {1} : {2}".format(
                    self.src_subnet_id, self.dst_ip, str(dst_port)
                )
            )

        def check_ingress_from_dst(acls, src_ip):
            for item in acls:
                acl = dict(zip(keys, item))
                # Check ipv4 acl rule only
                if acl.get("cidr_block"):
                    # Check IP
                    if src_ip in ip_network(acl["cidr_block"], strict=False):
                        # Check Port
                        if (acl.get("protocol") == "all") or (
                            src_port_from
                            and src_port_to
                            and set(range(src_port_from, src_port_to)).issubset(
                                range(
                                    acl["port_from"],
                                    acl["port_to"] + 1,
                                )
                            )
                        ):
                            # Check Action
                            if acl["rule_action"] == "allow":
                                break
                            else:
                                self.fail_json(
                                    msg=f"NatGateway Subnet {self.src_subnet_id} \
                                        Network Acl Ingress Rules do not allow \
                                        inbound traffic from destination: {self.dst_ip}"
                                )

            self.fail_json(
                msg="NatGateway Subnet {0} Network Acl Ingress Rules do not allow inbound traffic from destination: {1}".format(
                    self.src_subnet_id, self.dst_ip
                )
            )

        def check_ingress_from_src(acls, src_ip, dst_port):
            for item in acls:
                acl = dict(zip(keys, item))
                # Check ipv4 acl rule only
                if acl.get("cidr_block"):
                    # Check IP
                    if src_ip in ip_network(acl["cidr_block"], strict=False):
                        # Check Port
                        if (acl.get("protocol") == "all") or (
                            dst_port
                            in range(
                                acl["port_from"],
                                acl["port_to"] + 1,
                            )
                        ):
                            # Check Action
                            if acl["rule_action"] == "allow":
                                break
                            else:
                                self.fail_json(
                                    msg="NatGateway Subnet Network Acl \
                                          Ingress Rules do not allow inbound \
                                          traffic from source: {0} towards destination port {1}".format(
                                        self.src_ip, str(dst_port)
                                    )
                                )

            self.fail_json(
                msg="NatGateway Subnet Network Acl Ingress Rules do not allow inbound traffic from source {0} towards destination port {1}".format(
                    self.src_ip, str(dst_port)
                )
            )

        def check_egress_towards_src(acls, dst_ip):
            for item in acls:
                acl = dict(zip(keys, item))
                # Check ipv4 acl rule only
                if acl.get("cidr_block"):
                    # Check IP
                    if dst_ip in ip_network(acl["cidr_block"], strict=False):
                        # Check Port
                        if (acl.get("protocol") == "all") or (
                            src_port_from
                            and src_port_to
                            and set(range(src_port_from, src_port_to)).issubset(
                                range(
                                    acl["port_from"],
                                    acl["port_to"] + 1,
                                )
                            )
                        ):
                            # Check Action
                            if acl["rule_action"] == "allow":
                                break
                            else:
                                self.fail_json(
                                    msg="NatGateway Subnet Network Acl Egress Rules do not allow outbound traffic to source: {0}".format(
                                        self.src_ip
                                    )
                                )

            self.fail_json(
                msg=f"NatGateway Subnet Network Acl Egress Rules do not allow outbound traffic to source: {0}".format(
                    self.src_ip
                )
            )

        check_egress_towards_dst(egress_acls, dst_ip, dst_port)
        check_ingress_from_dst(ingress_acls, dst_ip)

        if self.src_subnet_id == self.nat_subnet_id:
            return True

        check_ingress_from_src(ingress_acls, src_ip, dst_port)
        check_egress_towards_src(egress_acls, src_ip)

        return True

    def get_nat_next_hop(self):
        destination = ip_address(self.dst_ip)
        most_specific = -1

        if self.src_subnet_id == self.nat_subnet_id:
            self.fail_json(
                msg="NatGateway and Source cannot be placed in the same subnet, NatGateway should be in a public subnet"
            )

        for route in self.routes:
            next_hop = None
            # Confirms whether the source has a public IP address associated with the resource, if the route destination is an internet gateway.
            if route.get("destination_cidr_block"):
                mask = int(route["destination_cidr_block"].split("/")[1])
                if (
                    "destination_prefix_list_id" not in str(route)
                    and destination in ip_network(route["destination_cidr_block"], strict=False)
                    and mask > most_specific
                ):
                    if route["state"] != "blackhole":
                        most_specific = mask
                        next_hop = route
        # 0.0.0.0/0
        if most_specific >= 0 and "igw-" in str(next_hop):
            return True
        self.fail_json(msg="No Internet Gateway route found for destination: {0}".format(self.dst_ip))

    def execute_module(self):
        try:
            # Evaluate ingress and egress NAT network ACLs
            self.eval_nat_nacls()
            self.get_nat_next_hop()
            self.exit_json(result="NAT Network ACLs evaluation successful")
        except Exception as e:
            self.fail_json(msg="NAT Network ACLs evaluation failed: {0}".format(e))


def main():
    EvalNatNetworkAcls()


if __name__ == "__main__":
    main()
