#!/bin/bash --
# Install salt minion in Raspberry Pi for Python3
if id -u | grep -v ^0$ > /dev/null; then
  echo "[EE] This script must be run as root" 1>&2;
  exit 1
fi

wget -O - https://repo.saltstack.com/py3/debian/9/armhf/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo "deb http://repo.saltstack.com/py3/debian/9/armhf/latest stretch main" > /etc/apt/sources.list.d/saltstack.list
apt-get update
apt-get install salt-minion salt-ssh

systemctl restart salt-minion
