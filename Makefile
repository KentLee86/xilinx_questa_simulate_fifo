# Xilinx Vivado 시뮬레이션 Makefile
# 동기 가산기 예제용

# 변수 설정
VIVADO = vivado
XVLOG = xvlog
XELAB = xelab
XSIM = xsim

PROJECT_NAME = sync_adder_sim
TOP_MODULE = tb_sync_adder
DESIGN_FILES = sync_adder.v
TB_FILES = tb_sync_adder.v
TCL_SCRIPT = run_sim.tcl

# 기본 타겟
.PHONY: all clean sim gui batch help

all: sim

# GUI 모드로 시뮬레이션 실행
gui:
	@echo "=== Vivado GUI 모드로 시뮬레이션 실행 ==="
	$(VIVADO) -source $(TCL_SCRIPT)

# 배치 모드로 시뮬레이션 실행
batch:
	@echo "=== Vivado 배치 모드로 시뮬레이션 실행 ==="
	$(VIVADO) -mode batch -source $(TCL_SCRIPT)

# xsim을 직접 사용한 시뮬레이션 (더 빠름)
sim:
	@echo "=== xsim을 이용한 직접 시뮬레이션 ==="
	@echo "1. Verilog 파일 컴파일..."
	$(XVLOG) $(DESIGN_FILES) $(TB_FILES)
	@echo "2. 디자인 엘라보레이션..."
	$(XELAB) -debug typical $(TOP_MODULE) -s $(TOP_MODULE)_sim
	@echo "3. 시뮬레이션 실행..."
	$(XSIM) $(TOP_MODULE)_sim -runall -testplusarg finish

# 파형 뷰어로 시뮬레이션 (GUI)
wave:
	@echo "=== 파형 뷰어와 함께 시뮬레이션 실행 ==="
	$(XVLOG) $(DESIGN_FILES) $(TB_FILES)
	$(XELAB) -debug typical $(TOP_MODULE) -s $(TOP_MODULE)_sim
	$(XSIM) $(TOP_MODULE)_sim -gui

# GTKWave로 VCD 파일 보기 (GTKWave가 설치된 경우)
gtkwave:
	@echo "=== GTKWave로 파형 보기 ==="
	@if command -v gtkwave >/dev/null 2>&1; then \
		if [ -f sync_adder.vcd ]; then \
			gtkwave sync_adder.vcd; \
		else \
			echo "VCD 파일이 없습니다. 먼저 'make sim'을 실행하세요."; \
		fi; \
	else \
		echo "GTKWave가 설치되지 않았습니다."; \
	fi

# 대안 테스트벤치로 시뮬레이션 (더 안전한 종료)
sim-alt:
	@echo "=== 대안 테스트벤치로 시뮬레이션 실행 ==="
	@echo "1. Verilog 파일 컴파일..."
	$(XVLOG) $(DESIGN_FILES) tb_sync_adder_alt.v
	@echo "2. 디자인 엘라보레이션..."
	$(XELAB) -debug typical tb_sync_adder_alt -s tb_sync_adder_alt_sim
	@echo "3. 시뮬레이션 실행..."
	$(XSIM) tb_sync_adder_alt_sim -runall

# 문법 체크만 수행
check:
	@echo "=== Verilog 문법 체크 ==="
	$(XVLOG) --nolog $(DESIGN_FILES) $(TB_FILES)

# 정리
clean:
	@echo "=== 생성된 파일들 정리 ==="
	rm -rf vivado_project/
	rm -rf xsim.dir/
	rm -rf .Xil/
	rm -f *.jou
	rm -f *.log
	rm -f *.vcd
	rm -f *.wdb
	rm -f vivado*.jou
	rm -f vivado*.log
	rm -f xvlog.pb
	rm -f xelab.pb

# 도움말
help:
	@echo "사용 가능한 명령어:"
	@echo "  make sim     - xsim을 이용한 빠른 시뮬레이션 (기본)"
	@echo "  make sim-alt - 대안 테스트벤치로 시뮬레이션 (더 안전한 종료)"
	@echo "  make gui     - Vivado GUI 모드로 시뮬레이션"
	@echo "  make batch   - Vivado 배치 모드로 시뮬레이션"
	@echo "  make wave    - 파형 뷰어와 함께 시뮬레이션"
	@echo "  make gtkwave - GTKWave로 VCD 파일 보기"
	@echo "  make check   - Verilog 문법 체크만 수행"
	@echo "  make clean   - 생성된 파일들 정리"
	@echo "  make help    - 이 도움말 표시"
