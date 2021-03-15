#!env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(dest='host',         help="Router's hostname/IP")
parser.add_argument(dest='username',     help="Username for SSH session")
parser.add_argument(dest='password',     help="Password for SSH session")
parser.add_argument(dest='aliases_file', help="Path to CSV file with aliases")
args = parser.parse_args()

import paramiko, time
cli = paramiko.client.SSHClient()
cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
cli.connect(hostname=args.host, username=args.username, password=args.password)
stdin_, stdout_, stderr_ = cli.exec_command("cat /proc/net/arp")
time.sleep(1)
stdout_.channel.recv_exit_status()
arp_entries_raw = stdout_.readlines()
cli.close()

import csv
aliases=dict()
with open(args.aliases_file, newline='') as aliases_file_handle:
  aliases_reader = csv.reader(aliases_file_handle, delimiter=',')
  for alias in aliases_reader:
    if len(alias)!=2 or alias[0][0]=='#':
      continue
    aliases.update({alias[0]:alias[1]})

discovered=[]
for arp_entry_raw in arp_entries_raw:
  arp_entry=arp_entry_raw.split()
  if arp_entry[0]=="IP" or arp_entry[3]=="00:00:00:00:00:00":
    continue
  discovered.append(arp_entry[3])

for mac in discovered:
  descr=aliases.get(mac, 'UNKNOWN_DEVICE')
  status=1
  if descr=="UNKNOWN_DEVICE":
    status=0
  print("archer_connected_host{mac=\"%s\",alias=\"%s\"} %d"%(mac,descr,status))


