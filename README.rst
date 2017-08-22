Usage of zabbix-ctl
===================

1. Create hostgroup
===================
    zabbixctl hostgroup create --group "group_name"

2. Delete hostgroup
===================
    zabbixctl hostgroup delete --group "group_name"

3. List hostgroups
==================
    zabbixctl hostgroup list

4. Add new node into zabbix monitoring system
=============================================
    zabbixctl host create --host "host_name" --groups "first" "second" --host-ip 127.0.0.1 --templates "first" "second"

5. Delete host from zabbix
==========================
    zabbixctl host delete --host "host_name"

7. List of zabbix hosts
=======================
    zabbixctl host list

8. Create zabbix screen for host
================================
    zabbixctl screen create --host "host_name"

9. Delete zabbix screen
=======================
    zabbixctl screen delete --host "host_name"

10. View zabbix screens
=======================
    zabbixctl screen list

How to enable debug mode
========================
    zabbixctl --debug <other arguments>

How to use config file from not default path
============================================
    zabbixctl --config <path_to_config_file> <other arguments>
