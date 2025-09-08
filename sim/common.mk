# Common Makefile for FPGA Simulation
# This file contains shared variables and targets for both Questa and XSIM simulators
# Include this file in your project-specific Makefiles

# =============================================================================
# Simulator Variables (override in your Makefile if needed)
# =============================================================================

# Vivado/XSIM paths
VIVADO ?= vivado
XVLOG ?= xvlog
XELAB ?= xelab
XSIM ?= xsim

# Questa/ModelSim paths
QUESTA_VSIM ?= vsim
QUESTA_VLOG ?= vlog
QUESTA_VCOM ?= vcom

# =============================================================================
# Common Variables (define these in your project Makefile)
# =============================================================================

# Project-specific variables (must be defined in including Makefile)
# PROJECT_NAME ?= your_project_name
# TOP_MODULE ?= your_top_module
# DESIGN_FILES ?= design1.v design2.v
# TB_FILES ?= tb_design.v
# TCL_SCRIPT ?= run_sim.tcl

# =============================================================================
# Common Flags and Options
# =============================================================================

# XSIM compilation flags
XVLOG_FLAGS ?= -sv
XELAB_FLAGS ?= -debug typical -relax
XSIM_FLAGS ?= -runall

# Questa compilation flags
VLOG_FLAGS ?= -sv
VSIM_FLAGS ?= -c -do "run -all; quit"

# =============================================================================
# Common Targets
# =============================================================================

.PHONY: all clean help check-syntax xsim questa

# Default target
all: xsim

# =============================================================================
# XSIM Targets (Vivado Simulator)
# =============================================================================

# Compile design and testbench for XSIM
xsim-compile:
	@echo "=== Compiling with XSIM ==="
	@echo "1. Compiling Verilog files..."
	$(XVLOG) $(XVLOG_FLAGS) $(DESIGN_FILES) $(TB_FILES)
	@echo "2. Elaborating design..."
	$(XELAB) $(XELAB_FLAGS) $(TOP_MODULE) -s $(PROJECT_NAME)

# Run XSIM simulation (batch mode)
xsim: xsim-compile
	@echo "3. Running simulation..."
	$(XSIM) $(PROJECT_NAME) $(XSIM_FLAGS)

# Run XSIM simulation with GUI
xsim-gui: xsim-compile
	@echo "3. Running simulation with GUI..."
	$(XSIM) $(PROJECT_NAME) -gui

# =============================================================================
# Questa Targets (ModelSim)
# =============================================================================

# Compile design and testbench for Questa
questa-compile:
	@echo "=== Compiling with Questa ==="
	@echo "1. Compiling Verilog files..."
	$(QUESTA_VLOG) $(VLOG_FLAGS) $(DESIGN_FILES) $(TB_FILES)

# Run Questa simulation (batch mode)
questa: questa-compile
	@echo "2. Running simulation..."
	$(QUESTA_VSIM) $(VSIM_FLAGS) $(TOP_MODULE)

# Run Questa simulation with GUI
questa-gui: questa-compile
	@echo "2. Running simulation with GUI..."
	$(QUESTA_VSIM) -gui $(TOP_MODULE)

# =============================================================================
# Utility Targets
# =============================================================================

# Syntax check only
check-syntax:
	@echo "=== Syntax Check ==="
	$(XVLOG) --nolog $(DESIGN_FILES) $(TB_FILES)

# Clean generated files
clean:
	@echo "=== Cleaning generated files ==="
	# XSIM cleanup
	rm -rf xsim.dir/
	rm -rf .Xil/
	rm -f *.jou
	rm -f *.log
	rm -f *.vcd
	rm -f *.wdb
	rm -f xvlog.pb
	rm -f xelab.pb
	rm -f vivado*.jou
	rm -f vivado*.log
	# Questa cleanup
	rm -rf work/
	rm -f transcript
	rm -f *.wlf
	rm -f modelsim.ini
	# Common cleanup
	rm -f *.pb

# Show help
help:
	@echo "Common FPGA Simulation Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make xsim         - Run simulation with XSIM (default)"
	@echo "  make xsim-gui     - Run simulation with XSIM GUI"
	@echo "  make questa       - Run simulation with Questa"
	@echo "  make questa-gui   - Run simulation with Questa GUI"
	@echo "  make check-syntax - Check syntax only"
	@echo "  make clean        - Clean generated files"
	@echo "  make help         - Show this help"
	@echo ""
	@echo "Define these variables in your project Makefile:"
	@echo "  PROJECT_NAME   - Name of your simulation project"
	@echo "  TOP_MODULE     - Top-level module name"
	@echo "  DESIGN_FILES   - Space-separated list of design files"
	@echo "  TB_FILES       - Space-separated list of testbench files"
	@echo "  TCL_SCRIPT     - TCL script for Vivado (optional)"

# =============================================================================
# Include guards and utilities
# =============================================================================

# Prevent multiple inclusion
ifndef COMMON_MK_INCLUDED
COMMON_MK_INCLUDED := 1
endif
