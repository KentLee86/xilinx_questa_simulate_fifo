onerror {resume}
quietly virtual function -install /tb_axis_fifo_example/dut/u_src -env /tb_axis_fifo_example { &{/tb_axis_fifo_example/dut/u_src/m_axis_tdata[31], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[30], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[29], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[28], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[27], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[26], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[25], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[24], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[23], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[22], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[21], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[20], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[19], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[18], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[17], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[16] }} frameId
quietly virtual function -install /tb_axis_fifo_example/dut/u_src -env /tb_axis_fifo_example { &{/tb_axis_fifo_example/dut/u_src/m_axis_tdata[15], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[14], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[13], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[12], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[11], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[10], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[9], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[8], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[7], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[6], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[5], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[4], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[3], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[2], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[1], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[0] }} Count
quietly virtual function -install /tb_axis_fifo_example/dut/u_src -env /tb_axis_fifo_example/#INITIAL#29 { &{/tb_axis_fifo_example/dut/u_src/m_axis_tdata[31], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[30], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[29], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[28], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[27], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[26], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[25], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[24], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[23], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[22], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[21], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[20], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[19], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[18], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[17], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[16], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[15], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[14], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[13], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[12], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[11], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[10], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[9], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[8] }} FrameId
quietly virtual function -install /tb_axis_fifo_example/dut/u_src -env /tb_axis_fifo_example/#INITIAL#29 { &{/tb_axis_fifo_example/dut/u_src/m_axis_tdata[7], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[6], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[5], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[4], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[3], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[2], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[1], /tb_axis_fifo_example/dut/u_src/m_axis_tdata[0] }} FrameCount
quietly WaveActivateNextPane {} 0
add wave -noupdate /tb_axis_fifo_example/aclk
add wave -noupdate /tb_axis_fifo_example/aresetn
add wave -noupdate /glbl/GSR
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tvalid
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tready
add wave -noupdate -expand -group Source -label FrameId -radix unsigned /tb_axis_fifo_example/dut/u_src/FrameId
add wave -noupdate -expand -group Source -label FrameCount -radix unsigned /tb_axis_fifo_example/dut/u_src/FrameCount
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tdata
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tkeep
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tlast
add wave -noupdate -expand -group Source /tb_axis_fifo_example/dut/u_src/m_axis_tuser
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tvalid
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tready
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tdata
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tkeep
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tlast
add wave -noupdate -expand -group Sink /tb_axis_fifo_example/dut/u_sink/s_axis_tuser
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {915000 ps} 0}
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
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {2199750 ps}
