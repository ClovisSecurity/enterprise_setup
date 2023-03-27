#! /usr/bin/env python

from data_obj import InterfaceInfo, InterfaceTrouble, RouterInfo, NatInfo, AccessList
import traceback
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
from router_info import router
from pprint import pprint
import xmltodict
from script35 import payload

"""
Program uses NETCONF to pull XML data from router
"""

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], 
                     hostkey_verify=False, device_params={'name': 'csr'}) as conn:
    for rpc in payload:
        try:
          response = conn.dispatch(et.fromstring(rpc))
          # print(response)
          data = response.xml
          
          query_response = xmltodict.parse(data)["rpc-reply"]["data"]["interfaces"]["interface"]
          pprint(query_response)
          
        except RPCError as exception:
          data = exception.xml
          pass
        except Exception as exception:
          traceback.print_exc()
          exit(1)
        
        for interface in query_response:
            name = interface['name']
            desc = interface['description']
            mac = interface['phys-address']
            oper_status = interface['admin-status']
            shutdown_bool = True
            
            if oper_status == "if-state-up":
                shutdown_bool = False
            else:
                shutdown_bool = True
            
            ip = interface['ipv4']
            subnet = interface['ipv4-subnet-mask']
            output_acl = interface['output-security-acl']
            int_info = InterfaceInfo(name = name, desc = desc, vlans=[""], ip=(ip, subnet), mac = mac, shut=shutdown_bool)
            
            print(int_info.name, int_info.desc, int_info.mac, shutdown_bool)
            print(int_info.ip[0], int_info.ip[1], output_acl)
            
            trunk_status = interface['ether-state']['negotiated-duplex-mode']
            int_trouble_data = InterfaceTrouble(name = interface['name'], trunk_status=trunk_status, speed=interface['speed'], 
                                                mtu=interface['mtu'], last_change=interface['last-change'])
            
            print(f"Name: {int_trouble_data.name}\nShutdown: {shutdown_bool}\nTrunk Status: {int_trouble_data.trunk_status}\nSpeed: \
                  {int_trouble_data.speed}\nMTU: {int_trouble_data.mtu}\nLast Change: {int_trouble_data.last_change}")
        
        exit()
    conn.close_session()
