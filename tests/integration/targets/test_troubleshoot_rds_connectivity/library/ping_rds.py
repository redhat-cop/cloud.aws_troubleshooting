#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: ping_rds
short_description: Connect to a RDS database
description:
  - This module connect to an RDS instance and list all tables
  - This module is used to run integration test for role troubleshoot_rds_connectivity only.
author:
  - Aubin Bikouo (@abikouo)
options:
  host:
    description:
    - The host name of the PostGreSQL instance.
    type: str
    required: true
  dbname:
    description:
    - The data name of the PostGreSQL instance.
    type: str
    required: true
  user:
    description:
    - The user name of the PostGreSQL instance.
    type: str
    required: true
  password:
    description:
    - The user passowrd of the PostGreSQL instance.
    type: str
    required: true
    no_log: true
"""


EXAMPLES = r"""
- name: Connect to a database instance
  ping_rds:
    host: ansible-test-20231017-rds.cudidmkulhom.eu-west-2.rds.amazonaws.com
    dbname: mysampledb123
    user: ansible
    password: test123!
"""


RETURN = r"""
result:
  type: str
  description: Wheter the client succeed to connect to the PostGreSQL instance.
  returned: success
  sample: 'The connection has been successfully established with PostGreSQL instance.'
"""

import psycopg2
from ansible.module_utils.basic import AnsibleModule


class PingRDSinstance(AnsibleModule):
    def __init__(self):
        argument_spec = dict(
            host=dict(type="str", required=True),
            dbname=dict(type="str", required=True),
            user=dict(type="str", required=True),
            password=dict(type="str", required=True, no_log=True),
        )

        super(PingRDSinstance, self).__init__(argument_spec=argument_spec)

        for key in argument_spec:
            setattr(self, key, self.params.get(key))

        self.dbconnection = None
        self.execute_module()

    def connect(self):
        conn_string = f"host={self.host} user={self.user} dbname={self.dbname} password={self.password} sslmode='require'"
        conn = psycopg2.connect(conn_string, connect_timeout=10)
        conn.close()

    def execute_module(self):
        try:
            # Run a simple Read query
            params = {
                "result": "The connection has been successfully established with PostGreSQL instance.",
            }
            self.connect()
            self.exit_json(**params)
        except Exception as e:
            self.fail_json(
                msg="An error occurred while trying to connect to RDS instance: {0}".format(
                    e
                )
            )


def main():
    PingRDSinstance()


if __name__ == "__main__":
    main()
