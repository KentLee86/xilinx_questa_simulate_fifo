# Questa/ModelSim D Flip-Flop 시뮬레이션 TCL 스크립트
# D 플립플롭 시뮬레이션 자동화

# 작업 라이브러리 생성 및 매핑
if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work

# 소스 파일 컴파일 (디버그 정보 포함)
echo "=== 소스 파일 컴파일 중 ==="
vlog -64 +define+DEBUG -work work +incdir+. ff.v
if {[file exists tb_ff.v]} {
    vlog -64 +define+DEBUG -work work +incdir+. tb_ff.v
} else {
    echo "오류: tb_ff.v 파일을 찾을 수 없습니다."
    exit 1
}

# Start simulation with debug options
echo "=== Starting simulation ==="
vsim -t 1ns -debugDB -voptargs="+acc" -lib work tb_ff

# Add signals to waveform window
add wave -noupdate -divider "Clock and Control Signals"
add wave -noupdate -format Logic /tb_ff/clk
add wave -noupdate -format Logic /tb_ff/rst
add wave -noupdate -divider "Data Signals"
add wave -noupdate -format Logic /tb_ff/d
add wave -noupdate -format Logic /tb_ff/q
add wave -noupdate -divider "DUT Internal Signals"
add wave -noupdate -format Logic /tb_ff/dut/clk
add wave -noupdate -format Logic /tb_ff/dut/rst
add wave -noupdate -format Logic /tb_ff/dut/d
add wave -noupdate -format Logic /tb_ff/dut/q

# 파형 창 설정
configure wave -namecolwidth 200
configure wave -valuecolwidth 80
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2

# Wave 창 먼저 열기
echo "=== Wave 창 열기 ==="
view wave

# 시뮬레이션 실행
echo "=== 시뮬레이션 실행 중 ==="
run -all

# 파형 확대/축소 자동 조정
wave zoom full

# Wave 창 새로고침 및 업데이트
wave refresh
update

# VCD 파일 생성 (GTKWave 호환)
echo "=== VCD 파일 생성 중 ==="
# Questa에서는 테스트벤치에서 $dumpfile과 $dumpvars로 VCD를 생성

echo "=== Simulation Complete ==="
echo "To view waveforms:"
echo "1. Check Wave window in Questa GUI"
echo "2. Or open generated ff_sim.vcd file with GTKWave:"
echo "   gtkwave ff_sim.vcd"
echo ""
echo "Debug and Breakpoint Commands:"
echo "1. View source code: view source"
echo "2. Set breakpoint: bp <filename> <line_number>"
echo "   Example: bp tb_ff.v 25"
echo "3. List breakpoints: info breakpoints"
echo "4. Delete breakpoint: delete <number>"
echo "5. Step execution: step, next"
echo "6. Continue execution: continue"
echo "7. Run until time: run <time>"
echo "8. Examine signals: examine <signal_name>"
echo ""
echo "To manually view waveforms in GUI:"
echo "  - Menu: View -> Wave"
echo "  - Or in console: view wave"
echo ""
echo "To exit simulation, use 'quit' command."
