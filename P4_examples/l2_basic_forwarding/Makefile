all: l2_basic_forwarding
BUILD_DIR = build
PCAP_DIR = pcaps
LOG_DIR = logs
run: dirs l2_basic_forwarding.p4
	p4c-bm2-ss --arch v1model --p4v 16 \
		--p4runtime-file ./l2_basic_forwarding.p4info --p4runtime-format text \
		-o ./l2_basic_forwarding.json l2_basic_forwarding.p4 \
		
dirs:
	mkdir -p $(BUILD_DIR) $(PCAP_DIR) $(LOG_DIR)

stop:
	sudo mn -c

clean: stop
	rm -f *.pcap
	rm -rf $(BUILD_DIR) $(PCAP_DIR) $(LOG_DIR)
