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

# Network definition
s1 = net.addSwitch('s1', json="./multicast.json", loglevel="debug", pktdump=True)
# , switch_config="command.txt"
h1 = net.addHost('h1')
h2 = net.addHost('h2')
h3 = net.addHost('h3')
h4 = net.addHost('h4')
net.addLink(s1, h1)
net.addLink(s1, h2)
net.addLink(s1, h3)
net.addLink(s1, h4)

info('*** Starting network\n')

net.start()
net.staticArp()

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()