#!/usr/bin/env python
# __author__ = 'TMagill'

from device import Device
import json
import xmltodict
import sys

def get_switches():
    '''
    This returns a dictionaryof switch info to be presented to user.
    '''
    sw_dict = {"switches": [{"hostname": "N9K1","ip_addr": "172.31.217.133","model": "Nexus 9396"},{"hostname": "N9K2","ip_addr": "172.31.217.133", "model": "Nexus 9396"},{"hostname": "N9K3","ip_addr": "172.31.217.133","model": "Nexus 9396"},{"hostname": "N9K4", "ip_addr":"172.31.217.133", "model": "Nexus 9396"}]}
    return sw_dict

def get_intfs(switch_ip):
    '''
    This connects to the chosen switch and gets all of the ports. and vlans.
    This is filtered to access ports only.
    '''
    switch_user = 'admin'
    switch_pw = 'cisco123'

    switch = Device(ip=switch_ip, username=switch_user, password=switch_pw)
    switch.open()
    command = switch.show('show interface')
    show_dict = xmltodict.parse(command[1])
    results = show_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']
    intf_list = []
    for result in results:
        if 'eth_mode' in result and result['eth_mode'] == 'access':
            intf_list.append(result['interface'])
    return intf_list

def get_vlans(switch_ip):
    '''
    This connects to the chosen switch and gets all of the ports. and vlans.
    This is filtered to access ports only.
    '''
    switch_user = 'admin'
    switch_pw = 'cisco123'

    switch = Device(ip=switch_ip, username=switch_user, password=switch_pw)
    switch.open()
    command = switch.show('show vlan')
    show_dict = xmltodict.parse(command[1])
    results = show_dict['ins_api']['outputs']['output']['body']['TABLE_vlanbrief']['ROW_vlanbrief']
    vlan_list = []
    for result in results:
        if 'USER' in  result['vlanshowbr-vlanname']:
            vlan_list.append([result['vlanshowbr-vlanid-utf'], result['vlanshowbr-vlanname']])
    # print json.dumps(show_dict, indent=4)
    return vlan_list

def show_run(switch_ip, intf_id):
    switch_user = 'admin'
    switch_pw = 'cisco123'

    switch = Device(ip=switch_ip, username=switch_user, password=switch_pw)
    switch.open()
    command = switch.show('show interface ' + intf_id + ' switchport')
    show_dict = xmltodict.parse(command[1])
    results = show_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']
    oper_mode = results['oper_mode']
    access_vlan = results['access_vlan']
    command = switch.show('show interface ' + intf_id)
    show_dict = xmltodict.parse(command[1])
    results = show_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']
    desc = results['desc']
    config_text = 'interface ' + intf_id + '\n  description ' + desc + '\n  switchport mode ' + oper_mode + '\n  switchport access vlan ' + access_vlan + '\n!\n'
    return config_text


def conf_intfs(conf_dict):
    '''
    This connects to the chosen switch and gets all of the ports. and vlans.
    This is filtered to access ports only.
    '''
    config_changes_list = ""
    switch_user = 'admin'
    switch_pw = 'cisco123'
    switch_ip = conf_dict['switch_ip']
    switch = Device(ip=switch_ip, username=switch_user, password=switch_pw)
    switch.open()

    for item in range(len(conf_dict['intf_id'])):
        change_vlan = 'config t ; interface ' + conf_dict['intf_id'][item] + ' ; switchport access vlan ' + conf_dict['vlan_id']
        change_desc = 'config t ; interface ' + conf_dict['intf_id'][item] + ' ; description ' + conf_dict['intf_desc']
        switch.conf(change_vlan)
        switch.conf(change_desc)
        config_changes_list += show_run(switch_ip, conf_dict['intf_id'][item])

    return config_changes_list

def main():
    # args = sys.argv
    conf_in = {"switch_ip": "172.31.217.135", "intf_desc": "Configured by NXAPI", "intf_id": ["Ethernet1/3", "Ethernet1/4"],"vlan_id": "32"}
    switch_dict = get_switches()
    # print json.dumps(switch_dict, indent=4)
    intfs = get_intfs('172.31.217.135')
    # print intfs
    vlans = get_vlans('172.31.217.135')
    # print vlans

    output = conf_intfs(conf_in)
    print output

if __name__ == "__main__":
    main()
