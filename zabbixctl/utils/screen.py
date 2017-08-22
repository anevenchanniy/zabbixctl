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


def create_screen(cfg, args, zapi):
    screen = {}
    result = {}
    # Get screen configuration data
    width = int(cfg.get('screens', 'width'))
    height = int(cfg.get('screens', 'height'))
    hsize = int(cfg.get('screens', 'hsize'))

    result = zapi.screen.get(filter={"name": args.host})
    if result:
        print("Error: screen %s already exists" % args.host)
        sys.exit(1)

    result = zapi.host.get(selectGraphs="['graphid']",
                           searchByAny=1,
                           filter={'host': args.host})

    # calculate vertical size
    num_item = len(result[0]['graphs'])
    if screen and screen['screenitems']:
        num_item += len(screen['screenitems'])
    vsize = num_item / hsize
    if num_item % hsize != 0:
        vsize += 1

    hpos = 0
    vpos = 0
    if screen:
        for i in screen['screenitems']:
            if hpos < int(i['x']):
                hpos = int(i['x'])
            if vpos < int(i['y']):
                vpos = int(i['y'])

        if hpos >= (hsize - 1):
            hpos = 0
            vpos += 1

    graphs = []
    screen_items = []
    for graph in result[0]['graphs']:
        graphs.append((graph['graphid']))

    for graph in graphs:
        data = {'colspan': 0,
                'rowspan': 0,
                'resourcetype': 0,
                'resourceid': graph,
                'x': hpos,
                'y': vpos,
                'width': width,
                'height': height,
                }
        screen_items.append(data)
        hpos += 1
        if hpos >= hsize:
            hpos = 0
            vpos += 1

    # create screen
    screen_creation_result = zapi.screen.create({
        'name': args.host,
        'hsize': hsize,
        'vsize': vsize,
        'screenitems': screen_items})

    print('Screen creation result = %s' % screen_creation_result)


def delete_screen(cfg, args, zapi):
    obj = zapi.screen.get(filter={"name": args.host})
    if obj:
        zapi.screen.delete(obj[0]['screenid'])


def list_screens(cfg, args, zapi):
    obj = zapi.screen.get(output="extend", selectScreenItems="extend")
    if len(obj) == 0:
        print("Error: No screens found.")
        sys.exit(1)
    pt = prettytable.PrettyTable(['Screen ID', 'Screen name'])
    for i in range(0, len(obj)):
        pt.add_row((obj[i]['screenid'], obj[i]['name']))
    print(pt)
