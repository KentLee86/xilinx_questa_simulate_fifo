# Questa/ModelSim D Flip-Flop 시뮬레이션 TCL 스크립트
# D 플립플롭 시뮬레이션 자동화

# 작업 라이브러리 생성 및 매핑
if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work

# 소스 파일 컴파일
echo "=== 소스 파일 컴파일 중 ==="
vlog -work work +incdir+. ff.v
if {[file exists tb_ff.v]} {
    vlog -work work +incdir+. tb_ff.v
} else {
    echo "오류: tb_ff.v 파일을 찾을 수 없습니다."
    exit 1
}

# 시뮬레이션 시작
echo "=== 시뮬레이션 시작 ==="
vsim -t 1ps -lib work tb_ff

# 파형 창에 신호 추가
add wave -noupdate -divider "클록 및 제어 신호"
add wave -noupdate -format Logic /tb_ff/clk
add wave -noupdate -format Logic /tb_ff/rst
add wave -noupdate -divider "데이터 신호"
add wave -noupdate -format Logic /tb_ff/d
add wave -noupdate -format Logic /tb_ff/q
add wave -noupdate -divider "DUT 내부 신호"
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

echo "=== 시뮬레이션 완료 ==="
echo "파형을 확인하려면:"
echo "1. Questa GUI에서 Wave 창을 확인하세요"
echo "2. 또는 생성된 ff_sim.vcd 파일을 GTKWave로 여세요:"
echo "   gtkwave ff_sim.vcd"
echo ""
echo "GUI가 열린 상태에서 수동으로 파형을 보려면:"
echo "  - 메뉴: View -> Wave"
echo "  - 또는 콘솔에서: view wave"
echo ""
echo "시뮬레이션 종료하려면 'quit' 명령을 사용하세요."
