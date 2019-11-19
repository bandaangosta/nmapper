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

class Nmapper():
    """Class to query local network to list and describe existing hosts"""
    def __init__(self, pathSettings=None):
        # Read configuration file
        if pathSettings is None:
            pathSettings = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), 'settings.ini')
        if os.path.exists(pathSettings):
            self.settings = configparser.ConfigParser(delimiters=['='])
            self.settings.optionxform = str
            self.settings.read(pathSettings)
        else:
            self.settings = None

        if not self.settings:
            self.alias = {}
            self.config = {}
        else:
            self.alias = self.settings['alias']
            self.config = self.settings['config']

    def getHosts(self):
        nm = nmap.PortScanner()
        # nm.scan(hosts='192.168.1.0/24', arguments='-sP -PE -PA21,23,80,3389')
        nm.scan(hosts='{}/24'.format(self.config.get('base_ip_nmap', '192.168.1.0')), arguments='-sn')

        # MAC address is only retrieved when run as sudo
        hosts_list = [(x, nm[x]['hostnames'][0]['name'], nm[x]['addresses'].get('mac'), nm[x]['status']['state']) for x in nm.all_hosts()]
        output = []
        for host, hostname, mac, status in hosts_list:
            output.append({'host': host, 'hostname': hostname, 'mac': mac, 'status': status})
        return {'hosts': output}

    def getHostsMulti(self):
        i = 0
        totalHosts = []

        while i < int(self.config.get('num_attempts', '3')):
            data = self.getHosts()
            totalHosts.extend(data['hosts'])
            i = i + 1

        finalHosts = {}
        for host in totalHosts:
            finalHosts[host['host']] = host

        if finalHosts:
            return {'hosts': list(finalHosts.values())}
        else:
            return {'hosts': []}

    def printHostsTable(self, arrHosts):

        print('Number of hosts found: {}'.format(len(arrHosts)))

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
                           self.alias.get(row['mac']),
                           row['status']
                          ])
        print('\n{}\n'.format(table))

def main():
    nmapper = Nmapper()

    print('Getting hosts in {}...'.format(nmapper.config.get('base_ip_nmap')))
    hosts = nmapper.getHostsMulti()

    # Present results
    if hosts['hosts']:
        nmapper.printHostsTable(hosts['hosts'])
    else:
        print('No hosts found')

if __name__ == '__main__':
    sys.exit(main())
