# Dataover cocotb Simulation Makefile

# Cocotb configuration
export COCOTB_REDUCED_LOG_FMT = 1
export PYTHONPATH := $(PWD):$(PYTHONPATH)

# Design and testbench files
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../dataover.v

# Top level module
TOPLEVEL = dataover

# Test module
MODULE = test_dataover

# Simulator selection (default: icarus, can be changed to questa, xsim, etc.)
SIM ?= icarus

# Waveform generation
WAVES = 1
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

# Default waveform format for Icarus
ifeq ($(SIM),icarus)
    COCOTB_HDL_DUMP_FILE ?= dataover_sim.vcd
endif

# Additional simulator arguments
ifeq ($(SIM),icarus)
    COMPILE_ARGS += -g2012
    # Remove problematic -fst argument that causes vvp error
endif

ifeq ($(SIM),questa)
    COMPILE_ARGS += -work work +incdir+$(PWD)/..
    SIM_ARGS += -t 1ns -voptargs="+acc"
endif

ifeq ($(SIM),xsim)
    COMPILE_ARGS += --include $(PWD)/..
    SIM_ARGS += --log xsim.log
endif


# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim
