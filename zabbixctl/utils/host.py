#!/usr/bin/python
# Copyright 2015: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import prettytable
import sys
import zabbixctl.utils


def get_hostid_by_name(zapi, host):
    obj = zapi.host.getobjects(name=host)
    if len(obj) == 0:
        print("Error: Host '%s' not found." % host)
        sys.exit(0)
    hid = obj[0]["hostid"]
    return hid


def create_host(cfg, args, zapi):
    group_id = []
    template_id = []

    for group in args.groups:
        gid = zabbixctl.utils.hostgroup.get_groupid_by_name(zapi, group)
        group_id.append({"groupid": str(gid)})

    for template in args.templates:
        tid = zabbixctl.utils.template.get_templateid_by_name(zapi, template)
        template_id.append({"templateid": str(tid)})

    try:
        zapi.host.create({
            "host": args.host,
            "interfaces": [{
                "type": 1,
                "dns": "",
                "main": 1,
                "ip": args.host_ip,
                "port": args.host_port,
                "useip": 1,
                }],
            "groups": group_id,
            "templates": template_id
            })
    except Exception as e:
        print(e)
        sys.exit(1)


def delete_host(cfg, args, zapi):
    hid = get_hostid_by_name(zapi, args.host)
    zapi.host.delete(hid)


def _decode_available_states(available):
    _available_states = {0: "Unknown",
                         1: "Available",
                         2: "Uvailable"}
    return _available_states[int(available)]


def _decode_monitoring_states(monitoring):
    _monitoring_states = {0: "Monitored",
                          1: "Unmonitored"}
    return _monitoring_states[int(monitoring)]


def list_hosts(cfg, args, zapi):
    hosts_list = zapi.host.getobjects()
    pt = prettytable.PrettyTable(
        ["Hostname", "Monitored", "Available", "Error"])
    for host in hosts_list:
        pt.add_row((host["host"],
                    _decode_monitoring_states(host["status"]),
                    _decode_available_states(host["available"]),
                    host["error"]))
    print(pt)
