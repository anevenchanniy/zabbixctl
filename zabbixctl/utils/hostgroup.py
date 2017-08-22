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
import pyzabbix
import sys


def get_groupid_by_name(zapi, group):
    obj = zapi.hostgroup.getobjects(name=group)
    if len(obj) == 0:
        print("Error: Group '%s' not found." % group)
        sys.exit(1)
    gid = obj[0]["groupid"]
    return gid


def create_group(cfg, args, zapi):
    try:
        zapi.hostgroup.create(name=args.group)
    except pyzabbix.ZabbixAPIException as e:
        print(e[0])
        sys.exit(1)


def delete_group(cfg, args, zapi):
    gid = get_groupid_by_name(zapi, args.group)
    zapi.hostgroup.delete(gid)


def list_groups(cfg, args, zapi):
    groups_list = zapi.hostgroup.getobjects()
    pt = prettytable.PrettyTable(["Host Group ID", "Host Group name"])
    for group in groups_list:
        pt.add_row((group["groupid"], group["name"]))
    print(pt)
