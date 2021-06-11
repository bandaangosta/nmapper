# nmapper

A tool to scan and list local network hosts. Useful for quick network discovery of new connected devices.

### Installation:

    pip install nmapper

### Requirements:

This tool requires `nmap` to be available in the system. On Debian/Ubuntu:

    apt install nmap

### Usage:

    nmapper hosts
    nmapper hosts 1       # for 1 scan pass, instead of 3 (default)
    nmapper config list   # to show all configuration options
    nmapper config --help # for more configuration commands, including edition of defaults
    nmapper alias list    # to show all MAC address aliases
    nmapper alias --help  # for more alias commands, including adding and removing aliases

Retrieving MAC addresses can only be done when application is run with elevated privileges

#### Getting your IP address to scan for hosts on the same network

    $ hostname -I

### Examples
#### Scan for hosts including MAC addresses
    $ sudo nmapper hosts
    Getting hosts in 192.168.1.0/24, 3 passes...
    Number of hosts found: 8
    
    +---------------+----------------------+-------------------+-------------------+--------+
    |          Host |             Hostname |               MAC |             Alias | Status |
    +---------------+----------------------+-------------------+-------------------+--------+
    |   192.168.1.1 |             _gateway | 00:07:4F:C5:1E:72 |            router |   up   |
    |  192.168.1.64 |                      | 50:31:D4:8A:10:D6 |       quicksilver |   up   |
    |  192.168.1.66 |                      | 19:5B:2D:3C:44:74 |       black-widow |   up   |
    | 192.168.1.148 |                      | 18:C9:A2:F9:1E:9A |           ant-man |   up   |
    | 192.168.1.175 |                      | F9:73:75:DB:63:82 |         wolverine |   up   |
    | 192.168.1.177 |   foobar-ragnar-5490 | 9C:ED:6B:4C:08:60 |            vision |   up   |
    | 192.168.1.182 |                      | 5D:21:F0:15:68:1D |         iron-fist |   up   |
    | 192.168.1.235 |                      | A5:7E:B1:15:04:28 |      juan-tastico |   up   |
    +---------------+----------------------+-------------------+-------------------+--------+
    
    New hosts since last scan:
    192.168.1.148
    
    Removed hosts since last scan:
    192.168.1.150

#### Scan for hosts no MAC addresses
    $ nmapper hosts
    Getting hosts in 192.168.1.0/24, 3 passes...
    Number of hosts found: 8
    
    +---------------+----------------------+------+-------+--------+
    |          Host |             Hostname |  MAC | Alias | Status |
    +---------------+----------------------+------+-------+--------+
    |   192.168.1.1 |             _gateway | None |  None |   up   |
    |  192.168.1.64 |                      | None |  None |   up   |
    |  192.168.1.66 |                      | None |  None |   up   |
    | 192.168.1.148 |                      | None |  None |   up   |
    | 192.168.1.175 |                      | None |  None |   up   |
    | 192.168.1.177 |   foobar-ragnar-5490 | None |  None |   up   |
    | 192.168.1.182 |                      | None |  None |   up   |
    | 192.168.1.235 |                      | None |  None |   up   |
    +---------------+----------------------+------+-------+--------+
    
    New hosts since last scan:
    192.168.1.175
    
    Removed hosts since last scan:
    192.168.1.133

#### Scan for hosts, 5 passes, on 172.17.0.xxx network
    $ nmapper hosts 5 172.17.0.0/24
    ...
    
#### Show configuration parameters
    $ nmapper config list

    +--------------+-------------+
    |          Key |       Value |
    +--------------+-------------+
    | NUM_ATTEMPTS |           3 |
    | BASE_IP_NMAP | 192.168.1.0 |
    +--------------+-------------+

#### Show MAC addresses alias list
    $ nmapper alias list
    
    +-------+-------------------+--------------------+
    | Index |               Key |              Value |
    +-------+-------------------+--------------------+
    |     0 | 50:31:D4:8A:10:D6 |        quicksilver |
    |     1 | F9:73:75:DB:63:82 |          wolverine |
    |     2 | 19:5B:2D:3C:44:74 |        black-widow |
    |     3 | 00:07:4F:C5:1E:72 |             router |
    |     4 | 18:C9:A2:F9:1E:9A |            ant-man |
    |     5 | 5D:21:F0:15:68:1D |          iron-fist |
    |     6 | A5:7E:B1:15:04:28 |       juan-tastico |
    |     7 | 9C:ED:6B:4C:08:60 |             vision |
    +-------+-------------------+--------------------+

#### Add new MAC address alias 
    $ nmapper alias add D0:32:87:B1:73:86 loki
    
    +-------+-------------------+--------------------+
    | Index |               Key |              Value |
    +-------+-------------------+--------------------+
    |     0 | 50:31:D4:8A:10:D6 |        quicksilver |
    |     1 | F9:73:75:DB:63:82 |          wolverine |
    |     2 | 19:5B:2D:3C:44:74 |        black-widow |
    |     3 | 00:07:4F:C5:1E:72 |             router |
    |     4 | 18:C9:A2:F9:1E:9A |            ant-man |
    |     5 | 5D:21:F0:15:68:1D |          iron-fist |
    |     6 | A5:7E:B1:15:04:28 |       juan-tastico |
    |     7 | 9C:ED:6B:4C:08:60 |             vision |
    |     8 | D0:32:87:B1:73:86 |               loki |
    +-------+-------------------+--------------------+
