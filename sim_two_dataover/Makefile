# Two Dataover cocotb Simulation Makefile

# Cocotb configuration
export COCOTB_REDUCED_LOG_FMT = 1
export PYTHONPATH := $(PWD):$(PYTHONPATH)

# Design and testbench files
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../dataover.v $(PWD)/../two_dataover.v

# Top level module
TOPLEVEL = two_dataover

# Test module
MODULE = test_two_dataover

# Simulator selection (default: icarus, can be changed to questa, xsim, etc.)
SIM ?= icarus

# Waveform generation
WAVES = 1
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# Default waveform format for Icarus
ifeq ($(SIM),icarus)
    COCOTB_HDL_DUMP_FILE ?= two_dataover_sim.vcd
endif

# Additional simulator arguments
ifeq ($(SIM),icarus)
    COMPILE_ARGS += -g2012
    # Remove problematic -fst argument that causes vvp error
endif

ifeq ($(SIM),questa)
    COMPILE_ARGS += -work work +incdir+$(PWD)/..
    SIM_ARGS += -t 1ps -voptargs="+acc"
endif

ifeq ($(SIM),xsim)
    COMPILE_ARGS += --include $(PWD)/..
    SIM_ARGS += --log xsim.log
endif

# Default target
all: sim

# Help target
help:
	@echo "Available targets:"
	@echo "  make              - Run simulation with default simulator ($(SIM))"
	@echo "  make SIM=icarus   - Run with Icarus Verilog"
	@echo "  make SIM=questa   - Run with Questa/ModelSim"
	@echo "  make SIM=xsim     - Run with Xilinx Vivado Simulator"
	@echo "  make clean        - Clean simulation files"
	@echo "  make help         - Show this help"

.PHONY: all help

# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

# Override clean target after including cocotb makefiles
clean::
	@echo "Cleaning up simulation files..."
	rm -rf __pycache__/
	rm -f *.vcd *.fst *.wlf *.ghw
	rm -f results.xml
	rm -f *.log
	rm -f dump.vcd
