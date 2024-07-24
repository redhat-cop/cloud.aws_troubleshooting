# cloud.aws_troubleshooting Validated Content Collection

This repository hosts the cloud.aws_troubleshooting Ansible Collection.

## Description

The cloud.aws_troubleshooting validated content collection in Ansible is designed to help users efficiently diagnose and resolve issues within their AWS environments. This collection includes a variety of Ansible roles and playbooks specifically tailored for troubleshooting common problems encountered in AWS infrastructure.

## Requirements

The [amazon.aws](https://github.com/ansible-collections/amazon.aws) and [community.aws](https://github.com/ansible-collections/amazon.aws) collections MUST be installed in order for this collection to work.

<!--start requires_ansible-->
### Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.15.0**.

### Included content

Click on the name of a role to view that content's documentation:

<!--start collection content-->
### Roles

Name | Description
--- | ---
[cloud.aws_troubleshooting.aws_setup_credentials](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/aws_setup_credentials/README.md)|A role to define credentials for aws modules.
[cloud.aws_troubleshooting.connectivity_troubleshooter](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter/README.md)|A role to troubleshoot connectivity issues between the following: a) AWS resources within an Amazon Virtual Private Cloud (Amazon VPC); b) AWS resources in different Amazon VPCs within the same AWS Region that are connected using VPC peering; c) AWS resources in an Amazon VPC and an internet resource using an internet gateway; d) AWS resources in an Amazon VPC and an internet resource using a network address translation (NAT) gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_igw](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter_igw/README.md)|A role to troubleshoot connectivity issues between AWS resources in an Amazon VPC and an internet resource using an internet gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_local](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter_local/README.md)|A role to troubleshoot connectivity issues between AWS resources within an Amazon Virtual Private Cloud (Amazon VPC).
[cloud.aws_troubleshooting.connectivity_troubleshooter_nat](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter_nat/README.md)|A role to troubleshoot connectivity issues between AWS resources in an Amazon VPC and an internet resource using a network address translation (NAT) gateway.
[cloud.aws_troubleshooting.connectivity_troubleshooter_peering](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter_peering/README.md)|A role to troubleshoot connectivity issues between AWS resources in different Amazon VPCs within the same AWS Region that are connected using VPC peering.
[cloud.aws_troubleshooting.connectivity_troubleshooter_validate](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/connectivity_troubleshooter_validate/README.md)|A role to validate input parameters for troubleshoot_connectivity_* roles and return connection next hop.
[cloud.aws_troubleshooting.troubleshoot_rds_connectivity](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/roles/troubleshoot_rds_connectivity/README.md)|A role to troubleshoot RDS connectivity from an EC2 instance.

<!--end collection content-->

## Installation

To consume this Validated Content from Automation Hub, please ensure that you add the following lines to your ansible.cfg file.

```ini
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```

The token can be obtained from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

Once the above steps are done, you can run the following command to install the collection.

```shell
ansible-galaxy collection install cloud.aws_troubleshooting
```

## Use cases

Once installed, you can reference the cloud.aws_troubleshooting collection content by its fully qualified collection name (FQCN), for example:

```yaml
  - hosts: all
    tasks:
       - name: Include 'cloud.aws_troubleshooting.connectivity_troubleshooter' role
        ansible.builtin.include_role:
          name: cloud.aws_troubleshooting.connectivity_troubleshooter
        vars:
          connectivity_troubleshooter_destination_ip: "{{ ip_instance_2 }}"
          connectivity_troubleshooter_destination_port: 80
          connectivity_troubleshooter_source_ip: "{{ ip_instance_1 }}"
```

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against this collection repository.

### Testing and Development

The project uses `ansible-lint` and `black`.
Assuming this repository is checked out in the proper structure,
e.g. `collections_root/ansible_collections/cloud/aws_troubleshooting/`, run:

```shell
  tox -e linters
```

Sanity and unit tests are run as normal:

```shell
  ansible-test sanity
```

If you want to run cloud integration tests, ensure you log in to the cloud:

```shell
# using the "default" profile on AWS
  aws configure set aws_access_key_id     my-access-key
  aws configure set aws_secret_access_key my-secret-key
  aws configure set region                eu-north-1

  ansible-test integration [target]
```

This collection is tested using GitHub Actions. To know more about CI, refer to [CI.md](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/CI.md).

## Support

You can also join us on:

- Libera.Chat IRC - the ``#ansible-aws`` [irc.libera.chat](https://libera.chat/) channel

## Release Notes

See the [raw generated changelog](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/CHANGELOG.rst).

## Related Information

 - [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html).
 - [Ansible Rulebook documentation](https://ansible.readthedocs.io/projects/rulebook/en/stable/index.html).
 - [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## License

GNU General Public License v3.0 or later
See [LICENSE](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/LICENSE) to see the full text.
