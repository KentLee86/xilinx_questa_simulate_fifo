
# Compile (표준 Verilog)
vlog +acc sync_adder.v tb_sync_adder.v

vsim work.tb_sync_adder
add wave -r sim:/*
run -all