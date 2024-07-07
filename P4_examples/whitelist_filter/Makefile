all: whitelist

whitelist: tutorial.p4
	p4c-bm2-ss --arch v1model -o tutorial.json \
		--p4runtime-file tutoriale.p4info --p4runtime-format text \
		tutorial.p4
