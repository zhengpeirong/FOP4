/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */

const bit<16> TYPE_IPV4 = 0x800;

#define BLOOM_FILTER_ENTRIES 4096
#define BLOOM_FILTER_BIT_WIDTH 1

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

//DNSレスポンスパケットを格納
//Headerセクション12バイト
stract header {
    bit <16> id;
    bit <1>  qr;
    bit <4>  opcode;
    bit <1>  aa;
    bit <1>  tc;
    bit <1>  rd;
    bit <1>  ra;
    bit <1>  z;
    bit <1>  ad;
    bit <1>  cd;
    bit <1>  rcode; //NOERROE or NXDOMAIN
    bit <16> qdcount;
    bit <16> ancount;
    bit <16> nscount;
    bit <16> arcount;
    

}
//Questionセクション
struct question {
    bit<2024>    name; //253*8
    bit<16>      type;
    bit<16>      class;
}

//Answerセクション
struct answer {
    bit<16>  name; //圧縮されている。
    bit<16>  type;
    bit<16>  class;
    bit<32>  ttl;
    bit<16>  len;
    bit<32>  ip;
}

struct metadata {
    /* empty */
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/
parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

}
/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    register<bit<BLOOM_FILTER_BIT_WIDTH>>(BLOOM_FILTER_ENTRIES) bloom_filter_1;
    register<bit<BLOOM_FILTER_BIT_WIDTH>>(BLOOM_FILTER_ENTRIES) bloom_filter_2;
    bit<32> reg_pos_one; bit<32> reg_pos_two;
    bit<1> reg_val_one; bit<1> reg_val_two;
    bit<1> direction;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    if(answer.ip != 0){
       action compute_hashes(bit<32> question1,bit<32> question2, bit<16> port1, bit<16> port2){
        hash (reg_pos_one, HashAlgorithm.crc16, (bit<32>)0,{
            question1,
            question2,
            port1,
            port2},
            (bit<32>)BLOOM_FILTER_ENTRIES);
        }
    }
}
/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;