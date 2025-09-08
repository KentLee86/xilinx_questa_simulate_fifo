# Makefile for sync_adder simulation
# This Makefile includes common.mk and defines project-specific variables

# Include common makefile
include ../sim/common.mk

# =============================================================================
# Project-specific Variables
# =============================================================================

PROJECT_NAME = sync_adder_sim
TOP_MODULE = tb_sync_adder
DESIGN_FILES = ../sync_adder.v
TB_FILES = tb/tb_sync_adder.v
TCL_SCRIPT = ../../run_sim.tcl

# Alternative testbench
TOP_MODULE_ALT = tb_sync_adder_alt
TB_FILES_ALT = tb/tb_sync_adder_alt.v

# =============================================================================
# Project-specific Targets
# =============================================================================

.PHONY: sim-alt wave gtkwave

# Default target (uses XSIM)
sim: xsim

# Alternative testbench simulation
sim-alt:
	@echo "=== Running alternative testbench ==="
	$(MAKE) TOP_MODULE=$(TOP_MODULE_ALT) TB_FILES="$(TB_FILES_ALT)" xsim

# Run with waveform viewer
wave:
	@echo "=== Running with waveform viewer ==="
	$(MAKE) xsim-gui

# GTKWave support (if VCD file is generated)
gtkwave:
	@echo "=== Opening waveform with GTKWave ==="
	@if command -v gtkwave >/dev/null 2>&1; then \
		if [ -f *.vcd ]; then \
			gtkwave *.vcd; \
		else \
			echo "VCD file not found. Run simulation first."; \
		fi; \
	else \
		echo "GTKWave not installed."; \
	fi

# Questa simulation
questa-sim:
	@echo "=== Running with Questa ==="
	$(MAKE) questa

questa-sim-gui:
	@echo "=== Running with Questa GUI ==="
	$(MAKE) questa-gui

# =============================================================================
# Help override
# =============================================================================

help:
	@echo "Sync Adder Simulation Makefile"
	@echo ""
	@echo "Project-specific targets:"
	@echo "  make sim          - Run simulation with XSIM (default)"
	@echo "  make sim-alt      - Run with alternative testbench"
	@echo "  make wave         - Run with waveform viewer"
	@echo "  make gtkwave      - Open VCD file with GTKWave"
	@echo "  make questa-sim   - Run with Questa (batch)"
	@echo "  make questa-sim-gui - Run with Questa (GUI)"
	@echo ""
	$(MAKE) -f ../sim/common.mk help
