# Multicast

```
+--+      +--+     ++-+
|h1+------+  +-----+h2+
+--+      +  +     +--+
          +s1+
+--+      +  +     ++-+
|h3+------+  +-----+h4+
+--+      +-++     +--+

```

## Introduction

In this example we show how to use the multicasting engine to broadcast
packets to all the ports of the switch.

In this very simple example we create a multicast group that sends packets
to all the four ports. Thus, the packet to broadcast will be sent back to
the port it came in. To avoid that, you can create a multicast group for
each ingress port, and then use it accordingly.

Note: Only packets with an ethernet type of `0x1234` get multicasted
to all the ports.

You can find more information about how to create multicast groups in
the following [documentation section](https://github.com/nsg-ethz/p4-learning/wiki/BMv2-Simple-Switch#creating-multicast-groups).

## How to run

Run the topology:

```bash
sudo python3 network.py
```
In the `containernet>`
```bash
sh simple_switch_CLI --thrift-port $(cat /tmp/bmv2-s1-thrift-port) < command.txt
```
## Start
Send traffic with the special ethernet type using the `send.py` script.

```bash
h1 python3 send.py
```

Monitor all the interfaces and see that for each packet that is sent from `h1`
four packets get replicated.
```bash
sudo tcpdump -i s1-eth2_out.pcap
sudo tcpdump -i s1-eth3_out.pcap
sudo tcpdump -i s1-eth4_out.pcap
```

### Check
(Optional:) Check if the table is right:
In another terminal:
```bash
simple_switch_CLI --thrift-port $(cat /tmp/bmv2-s1-thrift-port)

mc_dump
```
It should be:
- mgrp: multicast group
- L1h: Logical Node Handle
- rid: router ID of the Multicast node
- ports: router ports
- lags: link aggregation
```sh
==========
MC ENTRIES
**********
mgrp(1)
  -> (L1h=0, rid=0) -> (ports=[1], lags=[])
  -> (L1h=1, rid=1) -> (ports=[2], lags=[])
  -> (L1h=2, rid=2) -> (ports=[3], lags=[])
  -> (L1h=3, rid=3) -> (ports=[4], lags=[])
==========
LAGS
==========
```