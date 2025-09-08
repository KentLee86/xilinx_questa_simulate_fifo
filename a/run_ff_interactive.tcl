# QuestaSim 대화형 GUI 모드 TCL 스크립트
# D 플립플롭 시뮬레이션 - 파형 보기 최적화

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

# Wave 창 열기 (GUI 모드에서 필수)
echo "=== Wave 창 열기 ==="
view wave

# 파형 창에 신호 추가
echo "=== 신호 추가 중 ==="
add wave -noupdate -divider "클록 및 제어 신호"
add wave -noupdate -format Logic -radix binary /tb_ff/clk
add wave -noupdate -format Logic -radix binary /tb_ff/rst
add wave -noupdate -divider "데이터 신호" 
add wave -noupdate -format Logic -radix binary /tb_ff/d
add wave -noupdate -format Logic -radix binary /tb_ff/q
add wave -noupdate -divider "DUT 내부 신호"
add wave -noupdate -format Logic -radix binary /tb_ff/dut/clk
add wave -noupdate -format Logic -radix binary /tb_ff/dut/rst
add wave -noupdate -format Logic -radix binary /tb_ff/dut/d
add wave -noupdate -format Logic -radix binary /tb_ff/dut/q

# 파형 창 설정
configure wave -namecolwidth 200
configure wave -valuecolwidth 80
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2

# 시뮬레이션 실행
echo "=== 시뮬레이션 실행 중 ==="
run -all

# 파형 확대/축소 자동 조정
echo "=== 파형 표시 최적화 ==="
wave zoom full
wave refresh
update

echo "=== 시뮬레이션 완료 ==="
echo ""
echo "파형 확인 방법:"
echo "1. Wave 창이 자동으로 열렸습니다"
echo "2. 신호들이 추가되어 파형을 볼 수 있습니다"
echo "3. 파형이 보이지 않으면 다음을 시도하세요:"
echo "   - 메뉴: View -> Wave"
echo "   - 콘솔에서: wave zoom full"
echo "   - 콘솔에서: wave refresh"
echo ""
echo "시뮬레이션을 다시 실행하려면: run -all"
echo "시뮬레이션 종료하려면: quit"
echo ""
echo "대화형 모드입니다. GUI가 열린 상태로 유지됩니다."
