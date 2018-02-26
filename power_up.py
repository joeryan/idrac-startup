#!/usr/bin/env python

import os
import paramiko
import sys
import time
import getpass

#TODO use config file with hosts if available
idracs = [{'idrac': '192.168.100.93', 'host': '192.168.100.30'},
          {'idrac': '192.168.100.94', 'host': '192.168.100.40'},
          {'idrac': '192.168.100.95', 'host': '192.168.100.50'}]

idracUN = os.getenv('IDRAC_USER', 'root')
idracPW = os.getenv('IDRAC_PASSWORD', getpass.getpass("enter password: "))

def ping(host):
  return os.system("ping -c 1 {host} ".format(host=host))

for server in idracs:
  # check response of server standard address
  if ping(server['host']) == 0:  # host is up
    print("Host: {host} online".format(host=server['host']))
  else:  # if host can't be pinged
    if ping(server['idrac']) == 0: # idrac is reachable
        # ssh into idrac
      try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            server['idrac'],
            port=22,
            username=idracUN,
            password=idracPW,
            look_for_keys=False
            )
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            'racadm serveraction powerup'
            )
        print("Starting host {idrac}".format(idrac=server['idrac']))
      finally:
        if ssh:
          ssh.close()
    else:  # if idrac is down
        print("iDrac on host {idrac} down!".format(idrac=server['idrac']))

