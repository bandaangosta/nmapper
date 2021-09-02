import os
import shutil
import datetime
import nmap
import prettytable
import configparser
import typer
from config_path import ConfigPath

from rich.console import Console
from rich.table import Table
from rich.progress import track

class Nmapper():
    """Class to query local network to list and describe existing hosts"""

    # Application constants for local configuration file definition
    APP_NAME = 'nmapper'
    APP_VENDOR_DOMAIN = 'jlo.cl'
    APP_CONFIG_FILE_TYPE = '.ini'

    def __init__(self, path_settings=None, verbose=True):
        self.verbose = verbose

        if path_settings is None:
            # OS-independent definition of local configuration file
            conf_path = ConfigPath(self.APP_NAME, self.APP_VENDOR_DOMAIN, self.APP_CONFIG_FILE_TYPE)
            local_path = conf_path.saveFilePath(mkdir=True)
        else:
            local_path = path_settings

        # Template configuration file provided with package
        config_template = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), 'resources', 'settings.ini')

        # On first-time execution, create new configuration file from template file in package
        if not os.path.exists(local_path):
            if(shutil.copyfile(config_template, local_path)):
                if self.verbose:
                    print("Created local configuration file: ", local_path)

        # Read configuration file
        if not os.path.exists(local_path):
            self.path_settings = config_template
        else:
            self.path_settings = local_path

        if os.path.exists(self.path_settings):
            self.settings = configparser.ConfigParser(delimiters=['='])
            self.settings.optionxform = str
            self.settings.read(self.path_settings)
        else:
            self.settings = None

        if not self.settings:
            self.alias = {}
            self.config = {}
        else:
            self.alias = self.settings['alias']
            self.config = self.settings['config']

        self.base_ip_nmap = self.config.get('BASE_IP_NMAP', '192.168.1.0')
        self.attempts = self.config.get('NUM_ATTEMPTS', '3')

    def get_hosts(self, base_ip: str = None):
        '''Scan network for active hosts'''

        nm = nmap.PortScanner()

        if base_ip is None:
            _base_ip = self.base_ip_nmap
        else:
            _base_ip = base_ip

        nm.scan(hosts='{}/24'.format(_base_ip), arguments='-sn')

        # MAC address is only retrieved when run as sudo
        hosts_list = [(x, nm[x]['hostnames'][0]['name'], nm[x]['addresses'].get('mac'), nm[x]['status']['state']) for x in nm.all_hosts()]
        output = []
        for host, hostname, mac, status in hosts_list:
            output.append({'host': host, 'hostname': hostname, 'mac': mac, 'status': status})
        return {'hosts': output}

    def get_hosts_multi_attempts(self, base_ip: str = None, attempts: int = None):
        '''Scan network for active hosts, doing several passes for added reliability'''

        if attempts is None:
            _attempts = int(self.config.get('NUM_ATTEMPTS', '3'))
        else:
            _attempts = attempts

        if base_ip is None:
            _base_ip = self.base_ip_nmap
        else:
            _base_ip = base_ip

        if self.verbose:
            print('Getting hosts in {}/24, {} passes...'.format(_base_ip, _attempts))

        i = 0
        totalHosts = []

        for i in track(range(_attempts)):
            data = self.get_hosts(base_ip)
            totalHosts.extend(data['hosts'])
            i = i + 1

        final_hosts = {}
        for host in totalHosts:
            final_hosts[host['host']] = host

        if final_hosts:
            _final_hosts = list(final_hosts.values())
            _final_hosts.sort(key=lambda z: int(z['host'].split('.')[-1]))

            # Plain list of all hosts found, for comparison
            ips = [x['host'] for x in _final_hosts]

            # Get previous lists of hosts found
            if self.settings.has_section('results'):
                _last_ips = self.settings['results'].get('last', '')
                last_ips = _last_ips.split(',')
            else:
                self.settings.add_section('results')
                last_ips = []

            # New hosts since last scan
            new_hosts = list(set(ips).difference(set(last_ips)))

            # Removed hosts since last scan
            lost_hosts = list(set(last_ips).difference(set(ips)))

            # Save host ips for future comparison on next run
            self.settings.set('results', 'last', ','.join(ips))
            self.write_config_file()

            return {'hosts': _final_hosts, 'new_hosts': new_hosts, 'removed_hosts': lost_hosts}
        else:
            return {'hosts': [], 'new_hosts': [], 'removed_hosts': []}

    def write_config_file(self):
        '''Write configuration file to disk'''
        with open(self.path_settings, 'w') as f:
            self.settings.write(f)

    def print_hosts_table(self, arrHosts):
        '''Print scan results table'''

        utcnow = datetime.datetime.utcnow()
        print('Scan timestamp: {} UTC\n'.format(utcnow.strftime("%Y-%m-%d %H:%M")))


        table = Table(title=f'{len(arrHosts)} hosts in {self.base_ip_nmap}/24')
        table.add_column('Host', justify='right')
        table.add_column('Hostname', justify='right')
        table.add_column('MAC', justify='right')
        table.add_column('Alias', justify='right')
        table.add_column('Status', justify='right')

        for row in arrHosts:
            if row['mac']:
                alias = self.alias.get(row['mac']) or self.alias.get(row['mac'].lower())
            else:
                alias = None
            table.add_row(
                row['host'],
                row['hostname'],
                row['mac'],
                alias,
                f"[green]{row['status']}" if row['status'] =="up" else f"[red]{row['status']}"
            )

        console = Console()
        console.print(table)

    def print_config(self):
        '''Prints application parameters from config file'''

        table = prettytable.PrettyTable(['Key', 'Value'])
        table.align['Key'] = 'r'
        table.align['Value'] = 'r'

        for item in self.config.items():
            table.add_row([item[0], item[1]])
        print('\n{}\n'.format(table))

    def edit_config(self, attempts: int=typer.Argument(None), base_ip: str=typer.Argument(None)):
        '''Edit number of attempts or base ip in config file'''

        if attempts:
            if attempts < 1:
                print('Number of attempts must be greater than 1')
                return False

            with open(self.path_settings, 'w') as f:
                self.settings.set('config', 'NUM_ATTEMPTS', str(attempts))
                self.settings.write(f)

        if base_ip:
            # TODO: validation of IP address format
            with open(self.path_settings, 'w') as f:
                self.settings.set('config', 'BASE_IP_NMAP', str(base_ip))
                self.settings.write(f)

    def print_alias(self):
        '''Prints mac address -> alias list from config file'''

        table = prettytable.PrettyTable(['Index', 'Key', 'Value'])
        table.align['Index'] = 'r'
        table.align['Key'] = 'r'
        table.align['Value'] = 'r'

        for i,item in enumerate(self.alias.items()):
            table.add_row([i, item[0], item[1]])
        print('\n{}\n'.format(table))

    def add_alias(self, mac:str, alias: str):
        '''Add a new mac address -> alias in config file'''

        with open(self.path_settings, 'w') as f:
            self.settings.set('alias', mac, alias)
            self.settings.write(f)

    def remove_alias(self, index: int):
        '''Remove existing host alias from config file'''

        try:
            alias_list = list(self.settings['alias'].items())
            mac = alias_list[index][0]
        except IndexError:
            print('Incorrect index. No element was deleted.')
            return False

        with open(self.path_settings, 'w') as f:
            self.settings.remove_option('alias', mac)
            self.settings.write(f)
