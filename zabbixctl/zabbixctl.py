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
import argparse
import logging
import pyzabbix
import sys
from utils import config
from utils import host
from utils import hostgroup
from utils import screen
from utils import template


CONFIG_FILE = "/etc/zabbixctl.cfg"


def parse_args():
    parser = argparse.ArgumentParser(description="Zabbix configuration tool")
    """ Parse CLI arguments"""
    subparsers = parser.add_subparsers(help="zabbix-ctl sub-commands help")
    # create the parser for the "--debug" command
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode")
    # create the parser for the "--config" command
    parser.add_argument(
        "--config",
        type=str,
        default=CONFIG_FILE,
        help="Specify config file")
    # create the parser for the "host" item
    parser_host = subparsers.add_parser(
        "host",
        help="Opertations with zabbix host objects")
    # add subparser for host parser
    host_subparser = parser_host.add_subparsers(
        help="zabbix-ctl host sub-commands help")
    parser_host_list = host_subparser.add_parser(
        "list",
        help="List zabbix hosts")
    parser_host_list.set_defaults(func=host.list_hosts)
    # add delete subparser for host parser
    parser_host_delete = host_subparser.add_parser(
        "delete",
        help="Delete zabbix hosts")
    parser_host_delete.set_defaults(func=host.delete_host)
    parser_host_delete.add_argument(
        "--host",
        required=True,
        help="Hostname")
    parser_host_list.set_defaults(func=host.list_hosts)
    # add create subparser for host parser
    parser_host_create = host_subparser.add_parser(
        "create",
        help="Create zabbix host")
    parser_host_create.set_defaults(func=host.create_host)
    # Add arguments
    parser_host_create.add_argument(
        "--host",
        required=True,
        help="Hostname of host")
    parser_host_create.add_argument(
        "--groups",
        nargs="+",
        required=True,
        help="Space separated Zabbix host groups names")
    parser_host_create.add_argument(
        "--host-ip",
        required=True,
        help="IP address of host")
    parser_host_create.add_argument(
        "--host-port",
        required=False,
        default=10050,
        help="IP address of host")
    parser_host_create.add_argument(
        "--templates",
        required=True,
        nargs="+",
        help="Space separated Zabbix templates names")
    """ create the parser for the "hostgroup" item """
    parser_hostgroup = subparsers.add_parser(
        'hostgroup',
        help="Opertations with zabbix hostgroup objects")
    # add subparser for host parser
    hostgroup_subparser = parser_hostgroup.add_subparsers(
        help="zabbix-ctl hostgroup sub-commands help")
    parser_hostgroup_list = hostgroup_subparser.add_parser(
        "list",
        help="List zabbix hostsgroups")
    parser_hostgroup_list.set_defaults(func=hostgroup.list_groups)
    parser_hostgroup_create = hostgroup_subparser.add_parser(
        "create",
        help="List zabbix hostsgroups")
    parser_hostgroup_create.set_defaults(func=hostgroup.create_group)
    parser_hostgroup_create.add_argument(
        "--group",
        required=True,
        help="Zabbix hostgroup")
    parser_hostgroup_delete = hostgroup_subparser.add_parser(
        "delete",
        help="Delete zabbix hostsgroup")
    parser_hostgroup_delete.set_defaults(func=hostgroup.delete_group)
    parser_hostgroup_delete.add_argument(
        "--group",
        required=True,
        help="Zabbix hostgroup")
    """ create the parser for the "screen" item"""
    parser_screen = subparsers.add_parser(
        "screen",
        help="Opertations with zabbix screen objects")
    screen_subparser = parser_screen.add_subparsers(
        help="zabbix-ctl screen sub-commands help")
    parser_screen_list = screen_subparser.add_parser(
        "list",
        help="List zabbix screens")
    parser_screen_list.set_defaults(func=screen.list_screens)
    parser_screen_delete = screen_subparser.add_parser(
        "delete",
        help="Delete zabbix screen")
    parser_screen_delete.set_defaults(func=screen.delete_screen)
    parser_screen_delete.add_argument(
        "--host",
        required=True,
        help="Hostname")
    parser_screen_create = screen_subparser.add_parser(
        "create",
        help="Delete zabbix screen")
    parser_screen_create.set_defaults(func=screen.create_screen)
    parser_screen_create.add_argument(
        "--host",
        required=True,
        help="Hostname")
    """ create the parser for the template item """
    parser_template = subparsers.add_parser(
        "template",
        help="Opertations with zabbix templte objects")
    template_subparser = parser_template.add_subparsers(
        help="zabbix-ctl hostgroup sub-commands help")
    parser_template_list = template_subparser.add_parser(
        "list",
        help="List zabbix templates")
    parser_template_list.set_defaults(func=template.list_templates)
    return parser


def main():
    cfg = config.Config()
    zapi = pyzabbix.ZabbixAPI()
    args = parse_args().parse_args()
    cfg.init(args.config)

    if args.debug:
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger("pyzabbix")
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)

    zapi = pyzabbix.ZabbixAPI(cfg.get("zabbix", "uri"))
    try:
        zapi.login(cfg.get("zabbix", "user"),
                   cfg.get("zabbix", "password"))
    except Exception as e:
        print(e)
        sys.exit(1)

    args.func(cfg, args, zapi)


if __name__ == "__main__":
    main(sys.argv[1:])
