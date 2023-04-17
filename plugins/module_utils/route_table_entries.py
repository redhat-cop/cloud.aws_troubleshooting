from ipaddress import ip_network

from ansible.module_utils._text import to_text
from ansible_collections.cloud.aws_troubleshooting.plugins.module_utils.exception import (
    ValidationError,
    CidrOverlapeError,
    MissingRouteError,
)


def evaluate_route_tables(events):

    try:
        # RDS Info
        rdsSubnetIds = events["RDSSubnetIds"]
        rdsCidrs = events["RDSSubnetCidrs"]
        rdsRouteTables = events["RDSRouteTables"]
        rdsVpcRouteTables = events["RDSVpcRouteTables"]
        rdsVpcId = events["RDSVpcId"]

        # EC2 Instance Info
        ec2SubnetId = [events["EC2SubnetId"]]
        ec2InstanceIPs = events["EC2InstanceIPs"]
        ec2RouteTables = events["EC2RouteTables"]
        ec2VpcRouteTables = events["EC2VpcRouteTables"]
        ec2VpcId = events["EC2VpcId"]

        rds_rtb_list = []
        ec2_rtb_list = []
        b_check_vpc_rtb_rds = False
        b_check_vpc_rtb_ec2 = False

        rds_rtb_subnet_list = []  # All subnets that contain a valid rtb
        ec2_rtb_subnet_list = []

        # Initializing RouteTables
        for rtb in rdsRouteTables:
            for assoc in rtb["Associations"]:
                if assoc["SubnetId"] in rdsSubnetIds:
                    rds_rtb_subnet_list.append(assoc["SubnetId"])
        if len(rds_rtb_subnet_list) < len(rdsSubnetIds):
            b_check_vpc_rtb_rds = True

        for rtb in ec2RouteTables:
            for assoc in rtb["Associations"]:
                if assoc["SubnetId"] in ec2SubnetId:
                    ec2_rtb_subnet_list.append(assoc["SubnetId"])
        if len(ec2_rtb_subnet_list) < len(ec2SubnetId):
            b_check_vpc_rtb_ec2 = True

        # First verification: Check whether resources are in the same VPC. If not, Cidr cannot overlap
        if not rdsVpcId == ec2VpcId:
            for rdsCidr in rdsCidrs:
                for ec2InstanceIP in ec2InstanceIPs:
                    if ip_network(rdsCidr, strict=False).overlaps(
                        ip_network(ec2InstanceIP, strict=False)
                    ):
                        raise CidrOverlapeError(
                            "Resources are located in different VPCs, however, Cidrs are overlapping"
                        )
        else:
            return "Resources located in the same VPC"

        # Second verification: Check whether resources are using the same route table
        for rtb in rdsRouteTables:
            rds_rtb_list.append(rtb["RouteTableId"])

        for rtb in ec2RouteTables:
            ec2_rtb_list.append(rtb["RouteTableId"])

        if (
            (rdsRouteTables == ec2RouteTables)
            and not b_check_vpc_rtb_ec2
            and not b_check_vpc_rtb_rds
        ):
            return "Source and destination resources are using the same route table(s): {}".format(
                ec2_rtb_list
            )

        # Third verification: Check wheter route is through a peering connection
        # Verify whether RDS RTBs contains route to EC2 network
        for rtb in rdsRouteTables:
            required_ips = list(ec2InstanceIPs)
            for route in rtb["Routes"]:
                if "VpcPeeringConnectionId" not in route.keys():
                    continue
                if len(required_ips) == 0:
                    break
                for remote_ip in ec2InstanceIPs:
                    if ip_network(route["DestinationCidrBlock"], strict=False).overlaps(
                        ip_network(remote_ip, strict=False)
                    ):
                        required_ips.remove(remote_ip)
            if len(required_ips) == 0:
                rds_rtb_list.remove(rtb["RouteTableId"])

        if b_check_vpc_rtb_rds:
            for rtb in rdsVpcRouteTables:
                required_ips = list(ec2InstanceIPs)
                for route in rtb["Routes"]:
                    if "VpcPeeringConnectionId" not in route.keys():
                        continue
                    if len(required_ips) == 0:
                        break
                    for remote_ip in ec2InstanceIPs:
                        if ip_network(
                            route["DestinationCidrBlock"], strict=False
                        ).overlaps(ip_network(remote_ip, strict=False)):
                            if remote_ip in required_ips:
                                required_ips.remove(remote_ip)
                if len(required_ips) == 0:
                    rds_rtb_list.remove(rtb["RouteTableId"])

        # Verify whether EC2 RTB contains route to RDS network
        for rtb in ec2RouteTables:
            required_cidrs = list(rdsCidrs)
            for route in rtb["Routes"]:
                if "VpcPeeringConnectionId" not in route.keys():
                    continue
                if len(required_cidrs) == 0:
                    break
                for remote_cidr in rdsCidrs:
                    if ip_network(route["DestinationCidrBlock"], strict=False).overlaps(
                        ip_network(remote_cidr, strict=False)
                    ):
                        if remote_cidr in required_cidrs:
                            required_cidrs.remove(remote_cidr)
            if len(required_cidrs) == 0:
                ec2_rtb_list.remove(rtb["RouteTableId"])

        if b_check_vpc_rtb_ec2:
            for rtb in ec2VpcRouteTables:
                required_ips = list(rdsCidrs)
                for route in rtb["Routes"]:
                    if "VpcPeeringConnectionId" not in route.keys():
                        continue
                    if len(required_cidrs) == 0:
                        break
                    for remote_cidr in rdsCidrs:
                        if ip_network(
                            route["DestinationCidrBlock"], strict=False
                        ).overlaps(ip_network(remote_cidr, strict=False)):
                            required_cidrs.remove(remote_cidr)
                if len(required_ips) == 0:
                    ec2_rtb_list.remove(rtb["RouteTableId"])

        if len(rds_rtb_list) > 0:
            raise MissingRouteError(
                "Please review route table(s) {} for entries matching {} Cidr".format(
                    rds_rtb_list, ec2InstanceIPs
                )
            )

        if len(ec2_rtb_list) > 0:
            raise MissingRouteError(
                "Please review route table(s) {} for entries matching {} Cidr".format(
                    ec2_rtb_list, rdsCidrs
                )
            )

        return "Route table validation successful"

    except Exception as err:
        raise ValidationError(to_text(err))
