# D Flip-Flop Questa 시뮬레이션 Makefile

# 기본 변수 설정
TOP_MODULE = tb_ff
SRC_FILES = ff.v tb_ff.v
VCD_FILE = ff_sim.vcd
WORK_DIR = work

# 기본 타겟
.PHONY: all clean sim compile gui gui-interactive view_wave help

all: sim

# 도움말
help:
	@echo "사용 가능한 명령어:"
	@echo "  make sim            - 시뮬레이션 실행 (배치 모드)"
	@echo "  make gui            - GUI 모드로 시뮬레이션 실행"
	@echo "  make gui-interactive - 대화형 GUI 모드 (파형 최적화)"
	@echo "  make compile        - 소스 파일만 컴파일"
	@echo "  make view_wave      - GTKWave로 파형 보기"
	@echo "  make clean          - 생성된 파일 정리"
	@echo "  make help           - 이 도움말 보기"

# 소스 파일 컴파일 (디버그 정보 포함)
compile: $(WORK_DIR)
	@echo "=== 소스 파일 컴파일 중 ==="
	vlog -64 +define+DEBUG -work $(WORK_DIR) +incdir+. $(SRC_FILES)

# 작업 라이브러리 생성
$(WORK_DIR):
	@echo "=== 작업 라이브러리 생성 ==="
	vlib $(WORK_DIR)
	vmap work $(WORK_DIR)

# 배치 모드 시뮬레이션
sim: compile
	@echo "=== 배치 모드 시뮬레이션 실행 ==="
	vsim -c -do "run -all; quit" $(TOP_MODULE)
	@if [ -f $(VCD_FILE) ]; then \
		echo "VCD 파일이 생성되었습니다: $(VCD_FILE)"; \
		echo "GTKWave로 보려면: make view_wave"; \
	fi

# GUI 모드 시뮬레이션 (디버그 모드)
gui: compile
	@echo "=== GUI 모드 시뮬레이션 실행 ==="
	@echo "디버그 정보와 브레이크포인트를 사용할 수 있습니다."
	vsim -onfinish stop -do run_ff_questa.tcl

# 대화형 GUI 모드 시뮬레이션 (파형 최적화)
gui-interactive: compile
	@echo "=== 대화형 GUI 모드 시뮬레이션 실행 ==="
	@echo "파형이 자동으로 표시됩니다."
	vsim -do run_ff_interactive.tcl

# GTKWave로 파형 보기
view_wave:
	@if [ -f $(VCD_FILE) ]; then \
		echo "GTKWave로 파형을 엽니다..."; \
		gtkwave $(VCD_FILE) &; \
	else \
		echo "VCD 파일이 없습니다. 먼저 시뮬레이션을 실행하세요: make sim"; \
	fi

# 정리
clean:
	@echo "=== 생성된 파일 정리 ==="
	-rm -rf $(WORK_DIR)
	-rm -f transcript
	-rm -f *.vcd
	-rm -f *.wlf
	-rm -f modelsim.ini
	-rm -f vsim.wlf
	@echo "정리 완료!"

# 파일 의존성
ff.v:
tb_ff.v: ff.v
