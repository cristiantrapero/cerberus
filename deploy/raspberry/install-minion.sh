#!/bin/bash --
# SCRIPT FOR INSTALL SALT IN RASPBERRY AND CONNECT IT TO SYNDIC MASTER

if id -u | grep -v ^0$ > /dev/null; then
  echo "[EE] This script must be run as root" 1>&2;
  exit 1
fi

# INSTALL SALT MINION IN RASPBERRY PI
wget -O - https://repo.saltstack.com/py3/debian/9/armhf/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo "deb http://repo.saltstack.com/py3/debian/9/armhf/latest stretch main" > /etc/apt/sources.list.d/saltstack.list
apt-get update
apt-get install salt-minion 

#CONFIGURING MINION TO WORK WITH SYNDIC MASTER
cat << EOF > /etc/salt/minion
master: 161.67.140.15
user: root
publish_port: 4507
master_port: 4508
EOF

#RESTART THE SALT MINION
systemctl restart salt-minion

##IPTABLES RULES TO WORKAROUND SALT PUBLISH_PORT BUG
apt-get install -q -y -o Dpkg::Options::="--force-confnew" iptables-persistent
cat << EOF > /etc/iptables/rules.v4
# Do not edit. This file is provisioned by salt
*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
-A OUTPUT -d 127.0.0.1/32 -p tcp -m tcp --dport 4506 -j DNAT --to-destination 161.67.140.15:4508
-A OUTPUT -d 127.0.0.1/32 -p tcp -m tcp --dport 4505 -j DNAT --to-destination 161.67.140.15:4507
COMMIT

*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
COMMIT
EOF

#APPLY THE IPTABLES RULES
iptables-restore < /etc/iptables/rules.v4

