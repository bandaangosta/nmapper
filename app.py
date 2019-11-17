#!/usr/bin/env python3

import os
import sys

# Activate Python virtual environment containing all needed libraries and dependencies)
try:
    CURRENT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    if os.path.exists(os.path.join(CURRENT_DIR, 'venv/bin/activate_this.py')):
        activate_this = os.path.join(CURRENT_DIR, 'venv', 'bin', 'activate_this.py')
    else:
        print('No virtual environment is available')
        sys.exit()
    try:
        # Python 2
        execfile(activate_this, dict(__file__=activate_this))
    except NameError:
        # Python 3
        exec(open(activate_this).read(), {'__file__': activate_this})
except:
    raise

import nmap
import prettytable
import configparser

def getHosts():
    nm = nmap.PortScanner()
    # nm.scan(hosts='192.168.1.0/24', arguments='-sP -PE -PA21,23,80,3389')
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')

    # MAC address is only retrieved when run as sudo
    hosts_list = [(x, nm[x]['hostnames'][0]['name'], nm[x]['addresses'].get('mac'), nm[x]['status']['state']) for x in nm.all_hosts()]
    output = []
    for host, hostname, mac, status in hosts_list:
        output.append({'host': host, 'hostname': hostname, 'mac': mac, 'status': status})
    return {'hosts': output}

def printHostsTable(arrHosts, dictAlias={}):

    table = prettytable.PrettyTable(['Host', 'Hostname', 'MAC', 'Alias', 'Status'])
    table.align['Host'] = 'r'
    table.align['Hostname'] = 'r'
    table.align['MAC'] = 'r'
    table.align['Alias'] = 'r'
    for row in arrHosts:
        table.add_row([
                       row['host'],
                       row['hostname'],
                       row['mac'],
                       dictAlias.get(row['mac']),
                       row['status']
                      ])
    print('\n{}\n'.format(table))

def main():
    # Read configuration file
    if os.path.exists('settings.ini'):
        alias = configparser.ConfigParser(delimiters=['='])
        alias.optionxform = str
        alias.read('settings.ini')
    else:
        alias = None

    data = getHosts()
    if data['hosts']:
        # Present results
        if alias:
            printHostsTable(data['hosts'], alias['alias'])
        else:
            printHostsTable(data['hosts'])
    else:
        print('No hosts found')

if __name__ == '__main__':
    sys.exit(main())
