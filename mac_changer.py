#!usr/bin/env python3

import subprocess
import optparse
import re

def get_arg():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="interface to change mac address")
    parse.add_option("-m", "--mac", dest="mac", help="change of mac address")
    (option, arguments) = parse.parse_args()
    if not option.interface:
        parse.error("please specify correct interface, use --help for usage")
    elif not option.mac:
        parse.error("please specify correct mac, use --help for usage")
    return option
def mac_change(interface, mac):
    print("change of mac address for " + interface + " to " + mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("could not read MAC address")


options = get_arg()
get_current_mac = current_mac(options.interface)
print("current MAC = " + str(get_current_mac))

mac_change(options.interface, options.mac)
get_current_mac = current_mac(options.interface)

if get_current_mac == options.mac:
    print("MAC address was succesfully changed to " + get_current_mac)
else:
    print("MAC address did not get changed")