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

import ConfigParser
import os
import sys


class NoQuotesConfigParser(ConfigParser.ConfigParser):
    def get(self, section, option):
        value = ConfigParser.ConfigParser.get(self, section, option)
        value = self._unwrap_quotes(value)
        return value

    @staticmethod
    def _unwrap_quotes(src):
        quotes = ('"', "'")
        for quote in quotes:
            if src.startswith(quote) and src.endswith(quote):
                return src.strip(quote)
        return src


class Config(object):
    def __init__(self):
        self.config = NoQuotesConfigParser()

    def init(self, config_file):
        if not os.path.exists(config_file):
            print("Open configuration file %s failed!" % config_file)
            sys.exit(1)
        self.config = NoQuotesConfigParser()
        self.config.read(config_file)

    def get(self, section, option):
        try:
            result = self.config.get(section, option)
            return result
        except Exception as e:
            print(e)
            sys.exit(1)
