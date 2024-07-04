import nnpy
import struct

from mininet.bmv2 import bmv2Thrift
from scapy.all import Ether, sniff, Packet, BitField, raw


class L2Controller(object):

    def __init__(self, sw_name):
        self.sw_name = sw_name
        self.thrift_port = self.topo.get_thrift_port(sw_name)
        self.controller = bmv2Thrift(self.thrift_port)
        self.init()

    def init(self):
        self.controller.reset_state()
        self.add_boadcast_groups()
        self.add_mirror()
        #self.fill_table_test()

    def add_boadcast_groups(self):
        interfaces_to_port = self.topo.get_node_intfs(fields=['port'])[self.sw_name].copy()

        mc_grp_id = 1
        rid = 0
        for ingress_port in interfaces_to_port.values():
            port_list = list(interfaces_to_port.values())
            del(port_list[port_list.index(ingress_port)])
            #add multicast group
            self.controller.mc_mgrp_create(mc_grp_id)
            #add multicast node group
            handle = self.controller.mc_node_create(rid, port_list)
            #associate with mc grp
            self.controller.mc_node_associate(mc_grp_id, handle)
            #fill broadcast table
            self.controller.table_add("broadcast", "set_mcast_grp", [str(ingress_port)], [str(mc_grp_id)])
            mc_grp_id +=1
            rid +=1

    def fill_table_test(self):
        self.controller.table_add("dmac", "forward", ['00:00:0a:00:00:01'], ['1'])
        self.controller.table_add("dmac", "forward", ['00:00:0a:00:00:02'], ['2'])
        self.controller.table_add("dmac", "forward", ['00:00:0a:00:00:03'], ['3'])
        self.controller.table_add("dmac", "forward", ['00:00:0a:00:00:04'], ['4'])

    def learn(self, learning_data):
        for mac_addr, ingress_port in  learning_data:
            print("mac: %012X ingress_port: %s " % (mac_addr, ingress_port))
            self.controller.table_add("smac", "NoAction", [str(mac_addr)])
            self.controller.table_add("dmac", "forward", [str(mac_addr)], [str(ingress_port)])

    def unpack_digest(self, msg, num_samples):
        digest = []
        starting_index = 32
        for sample in range(num_samples):
            mac0, mac1, ingress_port = struct.unpack(">LHH", msg[starting_index:starting_index+8])
            starting_index +=8
            mac_addr = (mac0 << 16) + mac1
            digest.append((mac_addr, ingress_port))
        return digest

    def recv_msg_digest(self, msg):
        topic, device_id, ctx_id, list_id, buffer_id, num = struct.unpack("<iQiiQi",
                                                                          msg[:32])
        digest = self.unpack_digest(msg, num)
        self.learn(digest)
        #Acknowledge digest
        self.controller.client.bm_learning_ack_buffer(ctx_id, list_id, buffer_id)

    def run_digest_loop(self):
        sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        notifications_socket = self.controller.client.bm_mgmt_get_info().notifications_socket
        sub.connect(notifications_socket)
        sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')
        while True:
            msg = sub.recv()
            self.recv_msg_digest(msg)

if __name__ == "__main__":
    import sys
    sw_name = sys.argv[1]
    controller = L2Controller(sw_name).run_digest_loop()
