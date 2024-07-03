all: reflector
BUILD_DIR = build
PCAP_DIR = pcaps
LOG_DIR = logs
run: dirs reflector.p4
	p4c-bm2-ss --p4v 16 --p4runtime-files $(BUILD_DIR)/reflector.p4info.txtpb \
		-o $(BUILD_DIR)/reflector.json reflector.p4 \
		--arch v1model 
dirs:
	mkdir -p $(BUILD_DIR) $(PCAP_DIR) $(LOG_DIR)

stop:
	sudo mn -c

clean: stop
	rm -f *.pcap
	rm -rf $(BUILD_DIR) $(PCAP_DIR) $(LOG_DIR)
