onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /axis_master_file_v2/aclk
add wave -noupdate /axis_master_file_v2/aresetn
add wave -noupdate /axis_master_file_v2/i_start
add wave -noupdate /axis_master_file_v2/i_loop
add wave -noupdate /axis_master_file_v2/i_restart
add wave -noupdate /axis_master_file_v2/i_pause
add wave -noupdate /axis_master_file_v2/i_gap_cycles
add wave -noupdate /axis_master_file_v2/i_reload
add wave -noupdate /axis_master_file_v2/o_busy
add wave -noupdate /axis_master_file_v2/o_done_pulse
add wave -noupdate /axis_master_file_v2/o_sent_count
add wave -noupdate -radix decimal /axis_master_file_v2/m_axis_tdata
add wave -noupdate -divider {New Divider}
add wave -noupdate -format Analog-Step -height 84 -max 2069116274.0 -min -2069116274.0 -radix decimal /axis_master_file_v2/m_axis_tdata
add wave -noupdate /axis_master_file_v2/m_axis_tvalid
add wave -noupdate /axis_master_file_v2/m_axis_tready
add wave -noupdate /axis_master_file_v2/m_axis_tkeep
add wave -noupdate /axis_master_file_v2/m_axis_tlast
add wave -noupdate /axis_master_file_v2/idx
add wave -noupdate /axis_master_file_v2/gap_cnt
add wave -noupdate /axis_master_file_v2/state
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {1530000 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 222
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
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {4916832 ps}
