onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /tb_sync_adder/clk
add wave -noupdate /tb_sync_adder/rst_n
add wave -noupdate /tb_sync_adder/enable
add wave -noupdate -radix unsigned /tb_sync_adder/a
add wave -noupdate -radix unsigned /tb_sync_adder/b
add wave -noupdate -radix unsigned /tb_sync_adder/sum
add wave -noupdate /tb_sync_adder/valid
add wave -noupdate /tb_sync_adder/clk_enable
add wave -noupdate /tb_sync_adder/dut/clk
add wave -noupdate /tb_sync_adder/dut/rst_n
add wave -noupdate /tb_sync_adder/dut/enable
add wave -noupdate /tb_sync_adder/dut/a
add wave -noupdate /tb_sync_adder/dut/b
add wave -noupdate /tb_sync_adder/dut/sum
add wave -noupdate /tb_sync_adder/dut/valid
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {103910 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {190050 ps}
