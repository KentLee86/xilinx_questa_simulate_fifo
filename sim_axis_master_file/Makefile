# Makefile for axis_master_file_v2 cocotb simulation

# 시뮬레이션 설정
SIM ?= questa
TOPLEVEL_LANG ?= verilog

# DUT 설정
VERILOG_SOURCES += axis_master_file_v2.sv
TOPLEVEL = axis_master_file_v2

# 테스트 모듈
MODULE = test_master_file

# 파라미터 설정
PLUSARGS += +FILE_PATH=data.csv
PLUSARGS += +FILE_TYPE=csv
PLUSARGS += +LITTLE_ENDIAN=1
PLUSARGS += +DATA_BYTES=4

# 시뮬레이션 옵션
COMPILE_ARGS += -sv
COMPILE_ARGS += -timescale=1ns/1ps

# QuestaSim 특정 설정
ifeq ($(SIM),questa)
    # COMPILE_ARGS += -suppress 12110
    # SIM_ARGS += -suppress 12110
    # SIM_ARGS += -t 1ps
    # SIM_ARGS += -voptargs="+acc"
endif

# Icarus Verilog 설정
ifeq ($(SIM),icarus)
    COMPILE_ARGS += -g2012
endif

# 웨이브폼 설정
WAVES = 1
ifeq ($(SIM),questa)
    SIM_ARGS += -do "add wave -r /*; run -all"
endif

# 테스트 타임아웃
COCOTB_TEST_TIMEOUT_DURATION = 10000000
COCOTB_TEST_TIMEOUT_UNIT = ns

# 로그 레벨
COCOTB_LOG_LEVEL ?= INFO

# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim
