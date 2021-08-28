#!/bin/bash
# M. Szychowiak 2020-09-03
zypper -n update
# general:
zypper -n in vim nano wget ncat mc man man-pages
mandb
# KDE
zypper -n in -t pattern kde 
zypper -n in MozillaFirefox 
# lab sudo:
zypper in gcc gdb systemd-coredump
# lab SSO:
zypper -n in xinetd tcpd
rpm --quiet -i https://www.cs.put.poznan.pl/mszychowiak/download/rsh-server-0.17-736.1.x86_64.rpm 
rpm --quiet -i https://www.cs.put.poznan.pl/mszychowiak/download/rsh-0.17-736.1.x86_64.rpm
wget https://www.cs.put.poznan.pl/mszychowiak/security/tools/lab_tcpd/xinetd.conf.tgz
tar -zxvf xinetd.conf.tgz -C /
rm xinetd.conf.tgz
systemctl disable firewalld
# lab poczta:
zypper -n in MozillaThunderbird
# lab POSIX ACL:
zypper -n in acl
# lab iptables:
zypper -n in iptables squid
# lab VPN:
zypper -n in openvpn
##########################
PASS="3edcvfr4"
printf "$PASS\n$PASS\n" | passwd root 2> /dev/null
useradd -m -g users student
PASS="student"
printf "$PASS\n$PASS\n" | passwd student 2> /dev/null
ln -sf /usr/lib/systemd/system/graphical.target /etc/systemd/system/default.target
echo DISPLAYMANAGER_AUTOLOGIN="student" >> /etc/sysconfig/displaymanager
#chmod a+w /etc/sudoers
#cp -f /vagrant/hosts* /vagrant/sudoers /etc/
#chmod u=r,g=r,o= /etc/sudoers
#rm -f /etc/sudoers.d/student
reboot

