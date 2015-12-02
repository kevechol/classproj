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
    intf_list = ['TEST INTF']
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
    print json.dumps(show_dict, indent=4)
    intf_list = ['TEST VLAN']
    return vlan_list

def main():
    # args = sys.argv

    switch_dict = get_switches()
    print json.dumps(switch_dict, indent=4)
    intfs = get_intfs('172.31.217.134')
    print json.dumps(intfs, indent=4)
    vlans = get_vlans('172.31.217.134')
    print json.dumps(vlans, indent=4)

if __name__ == "__main__":
  main()

