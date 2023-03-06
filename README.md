# cloud.aws_troubleshooting
The collection includes a variety of Ansible roles to help troubleshoot AWS Resources.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.11.0**.

## Included content

Click on the name of a role to view that content's documentation:

<!--start collection content-->
### Roles
Name | Description
--- | ---
[cloud.aws_troubleshooting.aws_setup_credentials](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/aws_setup_credentials/README.md)|A role to define credentials for aws modules.
[cloud.aws_troubleshooting.connectivity_troubleshooter](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_detach_and_delete_internet_gateway/README.md)|A role to troubleshoot connectivity issues between the following: a) AWS resources within an Amazon Virtual Private Cloud (Amazon VPC); b) AWS resources in different Amazon VPCs within the same AWS Region that are connected using VPC peering; c) AWS resources in an Amazon VPC and an internet resource using an internet gateway; d) AWS resources in an Amazon VPC and an internet resource using a network address translation (NAT) gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_igw](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_multiregion_cloudtrail/README.md)|A role to troubleshoot connectivity issues between AWS resources in an Amazon VPC and an internet resource using an internet gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_local](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_multiregion_cloudtrail/README.md)|A role to troubleshoot connectivity issues between AWS resources within an Amazon Virtual Private Cloud (Amazon VPC).
[cloud.aws_troubleshooting.connectivity_troubleshooter_nat](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_multiregion_cloudtrail/README.md)|A role to troubleshoot connectivity issues between AWS resources in an Amazon VPC and an internet resource using a network address translation (NAT) gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_peering](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_multiregion_cloudtrail/README.md)|A role to troubleshoot connectivity issues between AWS resources in different Amazon VPCs within the same AWS Region that are connected using VPC peering.
[cloud.aws_troubleshooting.connectivity_troubleshooter_validate](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/awsconfig_multiregion_cloudtrail/README.md)|A role to validate input parameters for troubleshoot_connectivity_* roles and return connection next hop.
[cloud.aws_troubleshooting.troubleshoot_rds_connectivity](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/troubleshoot_rds_connectivity/README.md)|A role to troubleshoot RDS connectivity from an EC2 instance.

<!--end collection content-->

## Installation and Usage

### Installing the Collection from Ansible Galaxy
Before using the amazon_roles collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install cloud.aws_troubleshooting

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
    ---
    collections:
    - name: cloud.aws_troubleshooting
        version: 1.0.0
```

## License
GNU General Public License v3.0 or later
See [LICENSE](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/LICENSE) to see the full text.