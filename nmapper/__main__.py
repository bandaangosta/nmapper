from pprint import pprint
import typer
from nmapper import nmapper
from nmapper import __version__
from typing import Optional

# Command-line application commands and subcommands based in Typer
app = typer.Typer(add_completion=True)
config_app = typer.Typer(short_help="Application configuration commands")
app.add_typer(config_app, name="config")
alias_app = typer.Typer(short_help="MAC address alias commands")
app.add_typer(alias_app, name="alias")

@app.callback()
def callback():
    """
    Scan and list local network hosts.
    One of its applications is to find recently connected devices.

    Usage:

    \b
    nmapper hosts
    nmapper hosts 1     # for 1 scan pass, instead of 3 (default)
    nmapper config list # to show all configuration options
    nmapper config --help # for more configuration commands, including edition of defaults
    nmapper alias list # to show all MAC address aliases
    nmapper alias --help # for more alias commands, including adding and removing aliases

    Retrieving MAC addresses can only be done when application is run with elevated privileges
    """

@app.command(short_help='List local network hosts')
def hosts(attempts: Optional[int] = typer.Argument(None), base_ip: Optional[str] = typer.Argument(None)):
    nm = nmapper.Nmapper()
    hosts = nm.get_hosts_multi_attempts(base_ip, attempts)

    # Present results
    if hosts['hosts']:
        nm.print_hosts_table(hosts['hosts'])
    else:
        print('No hosts found')
        return

    # Show new/removed hosts
    print('New hosts since last scan:')
    if 'new_hosts' in hosts:
        print('\n'.join(hosts['new_hosts']))

    print('\nRemoved hosts since last scan:')
    if 'removed_hosts' in hosts:
        print('\n'.join(hosts['removed_hosts']))

@app.command(short_help='Show current version')
def version():
    print(__version__)

@config_app.command("list", short_help='List application settings')
def print_config():
    nm = nmapper.Nmapper()
    nm.print_config()

@config_app.command("edit_attempts", short_help='Change number of discovery attempts')
def edit_attempts(attempts: int):
    nm = nmapper.Nmapper()
    nm.edit_config(attempts=attempts, base_ip=None)
    nm.print_config()

@config_app.command("edit_base_ip", short_help='Change base ip for network discovery')
def edit_base_ip(base_ip: str):
    nm = nmapper.Nmapper()
    nm.edit_config(attempts=None, base_ip=base_ip)
    nm.print_config()

@alias_app.command("list", short_help='List host alias')
def print_alias():
    nm = nmapper.Nmapper()
    nm.print_alias()

@alias_app.command("add", short_help='Add new host alias')
def add_alias(mac:str, alias: str):
    nm = nmapper.Nmapper()
    nm.add_alias(mac, alias)
    print_alias()

@alias_app.command("remove", short_help='Remove existing host alias')
def add_alias(index: int):
    nm = nmapper.Nmapper()
    nm.remove_alias(index)
    print_alias()

def main():
    app()

if __name__ == "__main__":
    main()
