#! usr/bin/env
import subprocess
import optparse
import re
def get_arguments():
    passed_option = optparse.OptionParser()
    passed_option.add_option("-i", "--interface", dest="interface", help="interface to be changed(MAC address)")
    passed_option.add_option("-m", "--mac", dest="new_mac", help="new MAC address)")
    (value, option) =passed_option.parse_args()
    if not value.interface:
        passed_option.error("Enter the interface,use --help for further details")
    elif not value.new_mac:
        passed_option.error("Enter the new mac,use --help for further details")
    return value

def change_mac(interface,new_mac):
    '''unsecuredcommand
    subprocess.call("ifconfig " +interface+ " down", shell=True)
    subprocess.call("ifconfig " +interface+ " hw ether "+new_mac, shell=True)
    subprocess.call("ifconfig "+interface+ " up", shell=True)'''
    #securedcommand
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

'''interface = value.interface
new_mac = value.new_mac'''

value = get_arguments()
change_mac(value.interface,value.new_mac)

def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig",value.interface])
    ifconfig_output =re.search(r"\w.:..:..:..:..:.\w",ifconfig_output)
    if not ifconfig_output:
        print("could not read MAC address")
    else:
        return ifconfig_output.group(0)
current_mac=get_current_mac(value.interface)
print("current MAC="+str(current_mac))
if current_mac == value.new_mac:
    print("the MAC address is changed successfully")
else:
    print("the MAC address is not changed")
