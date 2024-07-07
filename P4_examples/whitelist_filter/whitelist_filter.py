#!/usr/bin/python
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.bmv2 import ONOSBmv2Switch, P4DockerHost
setLogLevel('info')


class NormalP4Switch(ONOSBmv2Switch):
    def __init__(self, name, **kwargs):
        ONOSBmv2Switch.__init__(self, name, **kwargs)
        self.netcfg = False


net = Containernet(controller=Controller, switch=NormalP4Switch)

info('*** Adding controller\n')
net.addController('c0')

info('*** Adding docker containers\n')


# Docker HOST
d1 = net.addDocker('d1', cls=P4DockerHost, ip='192.168.1.100',
                   dimage="ubuntu:22.04", mac="00:00:00:00:00:01")
d1.start()

# DNS server
d2 = net.addDocker('d2', cls=P4DockerHost, ip='192.168.1.200',
                   dimage="ubuntu:22.04", mac="00:00:00:00:00:A0")
d2.start()


info('*** Adding switches\n')

s1 = net.addSwitch('s1', json="./tutorial.json", loglevel="debug", pktdump=True)
#s1 = net.addSwitch('s1')

info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d2, s1)
info('*** Starting network\n')

net.start()
net.staticArp()

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()