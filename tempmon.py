#!/usr/bin/env python
"""
    Netconf python example by yang-explorer (https://github.com/CiscoDevNet/yang-explorer)

    Installing python dependencies:
    > pip install lxml ncclient

    Running script: (save as example.py)
    > python tempmon.py -a 192.168.1.222 -u <username> -p <password> --port 830
"""

import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError
import time

payload = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <environment-sensors xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper">
    <environment-sensor/>
  </environment-sensors>
</filter>
"""

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False) as m:
#                        device_params={'name': 'other'}) as m:

        # execute netconf operation
        try:
            response = m.get(payload).xml
            data = ET.fromstring(response)
        except RPCError as e:
            data = e._raw

ns = {'tel': 'http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper'}

def CtoF(temp):
    return temp * 1.8 + 32

file = open("/data/temp.txt", "w")

file.write(time.strftime("%c") + "\n" + "\n")

for child in data.iter('{http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper}environment-sensor'):
   name = child.find('tel:name', ns).text
   reading = int(child.find('tel:current-reading', ns).text)
   switch = child.find('tel:location', ns).text
   units = child.find('tel:sensor-units', ns).text
   state = child.find('tel:state', ns).text
   if name == "Temp Sensor 0":
       reading = CtoF(reading)
       file.write(switch + ' Inlet Sensor ' + str(reading) + ' Fahrenheit ' + state + "\n")
   elif name == "Temp Sensor 1":
       reading = CtoF(reading)
       file.write(switch + ' Exhaust Sensor ' + str(reading) + ' Fahrenheit ' + state + "\n")
   elif name == "Temp Sensor 2":
       reading = CtoF(reading)
       file.write(switch + ' Hotspot Sensor ' + str(reading) + ' Fahrenheit ' + state + "\n\n")
   else:
        file.write(switch + " " + name + " " + state + "\n")

file.close()
