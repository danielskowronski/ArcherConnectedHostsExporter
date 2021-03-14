# Archer Connected Hosts Exporter

Simple Python script to check hosts connected to router, in current itertion basing on ARP table obtained via SSH. Future development made with Archer routers in mind.

Outputs data in format acceptable by Prometheus that include MAC address, friendly alias based on data from CSV file and 0/1 status (0=unknown host, 1=known host).

## Setup
```
python3 -m pip install -r requirements.txt
```

## Usage
```
usage: ArcherConnectedHostsExporter.py [-h] host username password aliases_file

positional arguments:
  host          Router's hostname/IP
  username      Username for SSH session
  password      Password for SSH session
  aliases_file  Path to CSV file with aliases

optional arguments:
  -h, --help    show this help message and exit
```

### Typical application
It was created with cron execution (every minute) in mind that stores files consumed by `collector.textfile` in *prometheus_nodexporter*.

### Example output
```
% ./ArcherConnectedHostsExporter.py 192.168.0.1 admin XXXXXXXXXXXXX ./aliases.csv
archer_connected_host{mac="12:34:56:78:90:ab",alias="friendly_alias"} 1
archer_connected_host{mac="cc:dd:ee:ff:00:11",alias="UNKNOWN_DEVICE"} 0
```
