=======================================
cloud.aws_troubleshooting Release Notes
=======================================

.. contents:: Topics


v2.0.0
======

Release Summary
---------------

This major release drops support for ansible-core versions lower than 2.14 and Python versions lower than 3.9.

Breaking Changes / Porting Guide
--------------------------------

- Remove support for ansible-core < 2.14 (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/33).
- role/aws_setup_credentials - Due to ansible-lint issue, the AWS generated credentials are now stored into variable `aws_setup_credentials__output` instead of `aws_role_credentials`  (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/24)."
- role/connectivity_troubleshooter_validated - Due to ansible-lint issue, the next hop information stored into variable `connectivity_troubleshooter_validate__next_hop` instead of `next_hop`  (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/24)."

Minor Changes
-------------

- add `no_log=true` when setting credentials using role aws_setup_credentials (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/29).

Bugfixes
--------

- fix issue for role/connectivity_troubleshooter_igw calling module `cloud.aws_troubleshooting.eval_src_igw_route` with wrong value for parameters `src_subnet_id` and `src_network_interface` (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/29).
- fix issue for role/connectivity_troubleshooter_local using wrong value for source subnet id, should be `connectivity_troubleshooter_local__src_subnet_id` instead of `src_subnet_id` and for destination subnet id, should be `connectivity_troubleshooter_local__dst_subnet_id` instead of `dst_subnet_id` (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/29).
- fix issue for role/connectivity_troubleshooter_nat using wrong value for source subnet id, should be `connectivity_troubleshooter_nat__src_subnet_id` instead of `src_subnet_id` and add missing steps to gather information about NAT subnet network ACLs and source ENI (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/29).

v1.0.3
======

Bugfixes
--------

- Fix collection FQCN name issue for role troubleshooting_rds_connectivity (https://github.com/redhat-cop/cloud.aws_troubleshooting/pull/13).

v1.0.2
======

Minor Changes
-------------

- various playbooks - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various plugins - formating using black (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various roles - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various tests - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).

v1.0.1
======

Release Summary
---------------

Re-release 1.0.0 with updated README and generated CHNAGELOG, initial release of the collection

Minor Changes
-------------

- various playbooks - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various plugins - formating using black (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various roles - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
- various tests - minor linting fixes (https://github.com/ansible-collections/cloud.aws_troubleshooting/pull/6).
