import traceback
import lxml.etree as et
import xmltodict
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError
from router_info import router

int_name = "GigabitEthernet3"
desc = "Person Smarter Than Cisco Employee's Interface"
enable_bool = "true"
ip = "10.10.40.48"
ip_prefix = "24"

# Payload adds an IP address to an interface 
payload = [
f'''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <running/>
  </target>
  <config>
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
      <interface>
        <name>{int_name}</name>
        <config>
          <name>{int_name}</name>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
          <description>{desc}</description>
          <enabled>{enable_bool}</enabled>
        </config>
        <subinterfaces>
          <subinterface>
            <index>0</index>
            <config>
              <index>0</index>
              <description>{desc}</description>
              <enabled>{enable_bool}</enabled>
            </config>
            <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
              <addresses>
                <address>
                  <ip>{ip}</ip>
                  <config>
                    <ip>{ip}</ip>
                    <prefix-length>{ip_prefix}</prefix-length>
                  </config>
                </address>
              </addresses>
              <proxy-arp>
                <config>
                  <mode>DISABLE</mode>
                </config>
              </proxy-arp>
            </ipv4>
          </subinterface>
        </subinterfaces>
      </interface>
    </interfaces>
  </config>
</edit-config>
''',
]
with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], 
                     hostkey_verify=False, device_params={'name': 'csr'}) as conn:
    for rpc in payload:
        try:
          response = conn.dispatch(et.fromstring(rpc))
          # print(response)
          data = response.xml
          
        except RPCError as exception:
          data = exception.xml
          pass
        except Exception as exception:
          traceback.print_exc()
          exit(1)
          
          
        # beautify output
        if et.iselement(data):
            data = et.tostring(data, pretty_print=True).decode()

        try:
            out = et.tostring(
                et.fromstring(data.encode('utf-8')),
                pretty_print=True
            ).decode()
        except Exception as e:
            traceback.print_exc()
            exit(1)

        print(out)
