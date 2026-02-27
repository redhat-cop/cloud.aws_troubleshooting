# AWS Troubleshooting Collection for Ansible
The Ansible AWS Troubleshooting collection includes a variety of Ansible content to help efficiently diagnose and resolve connectivity and configuration issues within AWS environments. This collection is maintained by the Red Hat Communities of Practice.

## Contents

- [Description](#description)
- [Communication](#communication)
- [Requirements](#requirements)
  - [Ansible Version Compatibility](#ansible-version-compatibility)
  - [Python Version Compatibility](#python-version-compatibility)
  - [AWS Version Compatibility](#aws-version-compatibility)
- [Included Content](#included-content)
- [Installation](#installation)
  - [Installing Dependencies](#installing-dependencies)
- [Use Cases](#use-cases)
- [Testing](#testing)
- [Contributing to This Collection](#contributing-to-this-collection)
- [Support](#support)
- [Release Notes](#release-notes)
- [Related Information](#related-information)
- [Code of Conduct](#code-of-conduct)
- [License Information](#license-information)

## Description

The primary purpose of this collection is to simplify and streamline the diagnosis and resolution of AWS connectivity and resource configuration issues through automation. By leveraging this collection, organizations can reduce manual troubleshooting effort, minimize errors, and ensure consistent diagnostic approaches. This leads to faster issue resolution and a more reliable infrastructure.

This collection was formerly known as `redhat_cop.cloud_aws_troubleshooting`.

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  * [Posts tagged with 'aws'](https://forum.ansible.com/tag/aws): subscribe to participate in collection-related conversations.
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Requirements

### Ansible Version Compatibility

<!--start requires_ansible-->
This collection has been tested against the following Ansible versions: **>=2.17.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Python Version Compatibility

This collection requires Python 3.10+.

### AWS Version Compatibility

This collection requires the following collection dependencies:
- [amazon.aws](https://github.com/ansible-collections/amazon.aws) (>=10.0.0)
- [community.aws](https://github.com/ansible-collections/community.aws) (>=10.0.0)

## Included Content

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

The cloud.aws_troubleshooting collection can be installed with the Ansible Galaxy command-line tool:

```shell
ansible-galaxy collection install cloud.aws_troubleshooting
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cloud.aws_troubleshooting
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.
To upgrade the collection to the latest available version, run the following command:

```shell
ansible-galaxy collection install cloud.aws_troubleshooting --upgrade
```

A specific version of the collection can be installed by using the `version` keyword in the `requirements.yml` file:

```yaml
---
collections:
  - name: cloud.aws_troubleshooting
    version: 5.0.0
```

or using the `ansible-galaxy` command as follows:

```shell
ansible-galaxy collection install cloud.aws_troubleshooting:==5.0.0
```

To consume this Validated Content from Automation Hub, please ensure that you add the following lines to your ansible.cfg file:

```ini
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```

The token can be obtained from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

### Installing Dependencies

The collection dependencies are not installed by `ansible-galaxy` by default. They must be installed separately:

```shell
ansible-galaxy collection install amazon.aws:>=10.0.0
ansible-galaxy collection install community.aws:>=10.0.0
```

The Python module dependencies can be installed using pip:

```shell
pip install boto3>=1.26.0 botocore>=1.29.0
```

Refer to the following for more details:
* [Using Ansible collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)

## Use Cases

You can call roles by their Fully Qualified Collection Name (FQCN), such as `cloud.aws_troubleshooting.connectivity_troubleshooter`, or by their short name if you list the `cloud.aws_troubleshooting` collection in the playbook's `collections` keyword:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  tasks:
    - name: Troubleshoot connectivity between AWS resources
      ansible.builtin.include_role:
        name: cloud.aws_troubleshooting.connectivity_troubleshooter
      vars:
        connectivity_troubleshooter_source_ip: "{{ ip_instance_1 }}"
        connectivity_troubleshooter_destination_ip: "{{ ip_instance_2 }}"
        connectivity_troubleshooter_destination_port: 80

    - name: Troubleshoot RDS connectivity from EC2 instance
      ansible.builtin.include_role:
        name: cloud.aws_troubleshooting.troubleshoot_rds_connectivity
      vars:
        troubleshoot_rds_connectivity_db_instance_id: "{{ rds_identifier }}"
        troubleshoot_rds_connectivity_ec2_instance_id: "{{ ec2_instance_id }}"
```

If upgrading older playbooks which were built prior to Ansible 2.10 and this collection's existence, you can also define `collections` in your play and refer to this collection's roles as you did in Ansible 2.9 and below, as in this example:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - cloud.aws_troubleshooting

  tasks:
    - name: Troubleshoot connectivity between AWS resources
      ansible.builtin.include_role:
        name: connectivity_troubleshooter
      vars:
        connectivity_troubleshooter_source_ip: "{{ ip_instance_1 }}"
        connectivity_troubleshooter_destination_ip: "{{ ip_instance_2 }}"
        connectivity_troubleshooter_destination_port: 80
```

For documentation on how to use individual roles and other content included in this collection, please see the links in the [Included Content](#included-content) section.

## Testing

This collection is tested using GitHub Actions. To learn more about testing, refer to [CI.md](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/CI.md).

## Contributing to This Collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [AWS Troubleshooting collection repository](https://github.com/redhat-cop/cloud.aws_troubleshooting).

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

See [CONTRIBUTING.md](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/CONTRIBUTING.md) for more details.

### More information about contributing

- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly

## Support

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

For the latest supported versions, refer to the release notes below.

If you encounter issues or have questions, you can submit a support request through the following channels:
 - GitHub Issues: Report bugs, request features, or ask questions by opening an issue in the [GitHub repository](https://github.com/redhat-cop/cloud.aws_troubleshooting/).

## Release Notes

See the [raw generated changelog](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/CHANGELOG.rst).

## Related Information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## License Information

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
