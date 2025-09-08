# Clean
catch {vdel -all}
vlib work

# Compile (표준 Verilog)
vlog +acc sync_adder.v tb_sync_adder.v

# Simulate top
vsim -onfinish stop -voptargs=+acc work.tb_sync_adder

# Wave/log
log -r sim:/*
# add wave -r sim:/*
do wave.do

# (원하면 VCD를 Tcl로도 생성 가능)
# vcd file sync_adder_from_tcl.vcd
# vcd add -r sim:/*

# Run
run -all

# open wave window
view wave
