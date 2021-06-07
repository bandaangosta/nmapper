# nmapper

A tool to scan and list local network hosts. Useful for quick network discovery of new connected devices.

### Installation:

    pip install nmapper

### Requirements:

This tool requires `nmap` to be available in the system. On Debian/Ubuntu:

    apt install nmap

### Usage:

    nmapper hosts
    nmapper hosts 1     # for 1 scan pass, instead of 3 (default)
    nmapper config list # to show all configuration options
    nmapper config --help # for more configuration commands, including edition of defaults
    nmapper alias list # to show all MAC address aliases
    nmapper alias --help # for more alias commands, including adding and removing aliases

    Retrieving MAC addresses can only be done when application is run with elevated privileges
