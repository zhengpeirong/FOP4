# Packet Reflector

```
+----+       +----+
| h1 +-------+ s1 +
+----+       +----+
```

# Introduction

The program running in the switch simply reflects all the packets that receives
to the same port they arrived from.

# How to run

To start the topology with the P4 switches:
```bash
make run
```

```bash
sudo python3 network.py
```

Run the sending and receiving app at `h1`, every time you press return a
packet will be sent, if the packet gets bounced it will be printed:

```bash
h1 python3 send_receive.py
```