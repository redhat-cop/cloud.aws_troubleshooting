connectivity_troubleshooter_validate
====================================

A role to validate input parameters for troubleshoot_connectivity_* roles and return connection next hop.

* Verifies that an elastic network interface and VPC route tables exist for the provided source IP and VPC.
* Verifies that the route table includes a route for the provided destination IP.
* Returns the next hop from the provided source IP to the provided destination IP.

Requirements
------------

N/A

Role Variables
--------------

* **connectivity_troubleshooter_validate_destination_ip**: (Required) The IPv4 address of the resource you want to connect to.
* **connectivity_troubleshooter_validate_destination_port**: (Required) The port number you want to connect to on the destination resource.
* **connectivity_troubleshooter_validate_source_ip**: (Required) The private IPv4 address of the AWS resource in your Amazon VPC you want to test connectivity from.
* **connectivity_troubleshooter_validate_source_vpc**: (Optional) The ID of the Amazon VPC you want to test connectivity from.

Dependencies
------------

N/A

Example Playbook
----------------

```yaml
---
- name: AWS connectivity_troubleshooter_validate example
  hosts: localhost

  roles:
    - role: cloud.aws_troubleshooting.connectivity_troubleshooter_validate
      connectivity_troubleshooter_validate_destination_ip: 172.31.2.8
      connectivity_troubleshooter_validate_destination_port: 443
      connectivity_troubleshooter_validate_source_ip: 172.31.2.7
```

License
-------

GNU General Public License v3.0 or later

See [LICENSE](https://github.com/redhat-cop/cloud.aws_troubleshooting/blob/main/LICENSE) to see the full text.

Author Information
------------------

* Ansible Cloud Content Team
