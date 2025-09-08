# D Flip-Flop cocotb Simulation Makefile

# Cocotb configuration
export COCOTB_REDUCED_LOG_FMT = 1
export PYTHONPATH := $(PWD):$(PYTHONPATH)

# Design and testbench files
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../ff.v

# Top level module
TOPLEVEL = ff

# Test module
MODULE = test_ff

# Simulator selection (default: icarus, can be changed to questa, xsim, etc.)
SIM ?= icarus

# Waveform generation
WAVES = 1
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# Default waveform format for Icarus
ifeq ($(SIM),icarus)
    COCOTB_HDL_DUMP_FILE ?= dump.vcd
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

# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

# Custom targets
.PHONY: help clean-all install-deps view-waves test-all

help:
	@echo "D Flip-Flop cocotb Simulation Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make                    - Run cocotb tests (default: icarus)"
	@echo "  make SIM=questa         - Run tests with Questa/ModelSim"
	@echo "  make SIM=xsim           - Run tests with Vivado XSIM"
	@echo "  make SIM=icarus         - Run tests with Icarus Verilog"
	@echo "  make install-deps       - Install Python dependencies"
	@echo "  make view-waves         - View waveforms (if available)"
	@echo "  make test-all           - Run tests with all available simulators"
	@echo "  make clean              - Clean simulation files"
	@echo "  make clean-all          - Clean all generated files"
	@echo "  make help               - Show this help"
	@echo ""
	@echo "Environment variables:"
	@echo "  SIM=<simulator>         - Select simulator (icarus, questa, xsim)"
	@echo "  WAVES=1                 - Enable waveform generation"
	@echo "  GUI=1                   - Enable GUI mode (simulator dependent)"

# Install Python dependencies
install-deps:
	@echo "Installing cocotb and dependencies..."
	pip install -r requirements.txt

# View waveforms
view-waves:
	@if [ -f "dump.fst" ]; then \
		echo "Opening FST waveform with GTKWave..."; \
		gtkwave dump.fst &; \
	elif [ -f "dump.vcd" ]; then \
		echo "Opening VCD waveform with GTKWave..."; \
		gtkwave dump.vcd &; \
	elif [ -f "*.wlf" ]; then \
		echo "Questa waveforms available. Use: vsim -view *.wlf"; \
	else \
		echo "No waveform files found. Make sure WAVES=1 is set."; \
	fi

# Test with multiple simulators (if available)
test-all:
	@echo "Testing with available simulators..."
	@for sim in icarus questa xsim; do \
		if command -v $$sim >/dev/null 2>&1 || command -v vsim >/dev/null 2>&1; then \
			echo "Testing with $$sim..."; \
			$(MAKE) SIM=$$sim || echo "$$sim test failed"; \
		else \
			echo "$$sim not available, skipping..."; \
		fi; \
	done

# Enhanced clean target
clean-all: clean
	@echo "Cleaning all generated files..."
	-rm -f *.fst *.vcd *.wlf
	-rm -f *.jou *.log *.pb
	-rm -rf __pycache__
	-rm -rf .pytest_cache
	-rm -rf xsim.dir
	-rm -rf work
	-rm -f transcript
	-rm -f modelsim.ini

# Default target
all:
	@echo "Running cocotb tests for D Flip-Flop..."
	@$(MAKE) --no-print-directory

# Quick test target
test: all
