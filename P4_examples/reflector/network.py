#!/usr/bin/python
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
from mininet.bmv2 import Bmv2Switch, P4DockerHost
setLogLevel('info')

net = Containernet(controller=Controller, switch=Bmv2Switch)
# Network general options
info('*** Adding controller\n')
net.addController('c0')
# Network definition
s1 = net.addSwitch('s1', json="./build/reflector.json", loglevel="debug", pktdump=True)
h1 = net.addHost('h1')

net.addLink(s1, h1)

info('*** Starting network\n')
net.start()
net.staticArp()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()