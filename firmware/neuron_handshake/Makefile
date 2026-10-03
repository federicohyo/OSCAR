
#TOOLCHAIN_PATH=/usr/bin/
# TOOLCHAIN_PATH=/usr/local/bin/
# TOOLCHAIN_PATH=/opt/riscv32i/bin/
# TOOLCHAIN_PATH=/ef/apps/bin/
TOOLCHAIN_PATH=/usr/bin/

# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
# Ubuntu's gcc-riscv64-unknown-elf package (multilib) builds rv32i via -march/-mabi.
TOOLCHAIN_PREFIX=riscv64-unknown-elf
#TOOLCHAIN_PREFIX=riscv32-unknown-elf
#TOOLCHAIN_PREFIX=riscv32
#ARCH=rv32i
# Modern binutils split CSR ops out of base rv32i; crt0_vex.S uses csrw, so need zicsr.
ARCH=rv32i_zicsr

# Spike streaming mode: 1 (default) = deferred streaming (SRAM drain + ring
# buffer + deferred UART with raw 16-bit timestamps); 0 = fast reservoir (counts
# only, SRAM drain, for 0xDB timing). Override: make STREAM_SPIKES=0 hex
STREAM_SPIKES ?= 1

# Core clock in MHz the firmware is calibrated for. 50 = DLL engaged (fb=10, out
# div /2), 10 = crystal. Scales delay_loop() pulse widths and Timer0 tick
# constants. The DLL does NOT survive a power cycle, so whatever runs this image
# must engage it: run_neuron_test.py does (--clock, default 50) and so does
# neuron_bridge.py (CARAVAN_CLK_MHZ, default 50). Keep all three in step.
F_CPU_MHZ ?= 50

# ---- Test patterns for project raven ----

.SUFFIXES:

PATTERN = neuron_handshake

hex:  ${PATTERN:=.hex}

%.elf: %.c ../common/sections.lds ../common/crt0_vex.S
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-gcc -I../common/ -I../common/generated/ -O0 -mabi=ilp32 -march=$(ARCH) -D__vexriscv__ -DSTREAM_SPIKES=$(STREAM_SPIKES) -DF_CPU_MHZ=$(F_CPU_MHZ) $(EXTRA_CFLAGS) -Wl,-Bstatic,-T,../common/sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../common/crt0_vex.S ../common/isr.c ../common/stub.c $<
	${TOOLCHAIN_PATH}$(TOOLCHAIN_PREFIX)-objdump -D neuron_handshake.elf > neuron_handshake.lst

%.hex: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O verilog $< $@
	sed -i 's/@1000/@0000/g' $@

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

client: client.c
	python3 ./client.py

# LEGACY UPSTREAM TARGET. The upstream `../util/caravel_hkflash.py` resides
# outside this repo. Flash via the host tool instead:
#   python3 ../../host/run_neuron_test.py --clock 50
#   ../../host/bringup_50.sh
# See docs/BRINGUP.md and firmware/README.md.
flash: neuron_handshake.hex
	@echo "flash target is stale; use host/run_neuron_test.py (HKSPI in host/riscvprog.py)" >&2
	@exit 1

# ---- Clean ----

clean:
	rm -f *.elf *.hex *.bin *.vvp *.vcd *.lst

.PHONY: clean hex all flash
