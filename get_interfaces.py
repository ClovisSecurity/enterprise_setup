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

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False, device_params={'name': 'csr'}) as m:
    for rpc in payload:
        try:
          response = m.dispatch(et.fromstring(rpc))
          # print(response)
          data = response.xml
          
          query_response = xmltodict.parse(data)["rpc-reply"]["data"]["interfaces"]["interface"]
          pprint(query_response)
          
        except RPCError as e:
          data = e.xml
          pass
        except Exception as e:
          traceback.print_exc()
          exit(1)
        
        for interface in query_response:
            name = interface['name']
            desc = interface['description']
            mac = interface['phys-address']
            oper_status = interface['admin-status']
            shutdown_bool = True
            
            if oper_status == "id-state-up":
                shutdown_bool = False
            
            ip = interface['ipv4']
            subnet = interface['ipv4-subnet-mask']
            output_acl = interface['output-security-acl']
            int_info = InterfaceInfo(name = name, desc = desc, vlans=[""], ip=(ip, subnet), mac = mac, shut=shutdown_bool)
            print(int_info.name, int_info.desc, int_info.mac, shutdown_bool)
            print(int_info.ip[0], int_info.ip[1], output_acl)
        
        exit()
    m.close_session()
