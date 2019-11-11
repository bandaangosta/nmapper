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

nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-sP -PE -PA21,23,80,3389')
hosts_list = [(x, nm[x]['hostnames'][0]['name'], nm[x]['status']['state']) for x in nm.all_hosts()]
for host, hostname, status in hosts_list:
    print('{}:{}:{}'.format(host, hostname, status))