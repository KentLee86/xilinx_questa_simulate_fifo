
#!/bin/bash

# AXIS FIFO 예제 시뮬레이션 스크립트
# 사용법: ./run.sh [옵션]
#
# === QuestaSim 모드 (기본) ===
#   (없음)   - 배치 모드로 시뮬레이션 실행
#   gui      - GUI 모드로 시뮬레이션 실행
#   vcd      - VCD 파일 생성 후 시뮬레이션
#   wave     - 파형 뷰어로 시뮬레이션
#   check    - 문법 체크만 수행
#
# === xsim 모드 (Vivado 설치 시) ===
#   xsim     - xsim으로 배치 모드 실행
#   xsim-gui - xsim GUI 모드로 시뮬레이션 실행
#   xsim-vcd - xsim으로 VCD 파일 생성 후 시뮬레이션
#
# 예시:
#   ./run.sh              # QuestaSim 배치 모드
#   ./run.sh gui          # QuestaSim GUI 모드
#   ./run.sh xsim         # xsim 배치 모드 (Vivado 필요)
#   ./run.sh xsim-vcd     # xsim VCD 생성 모드

# 옵션 파싱
MODE="batch"
SIMULATOR="questa"  # 기본 시뮬레이터: questa 또는 xsim
if [ $# -gt 0 ]; then
    MODE="$1"
fi

# 시뮬레이터 종류 결정
case $MODE in
    "xsim"|"xsim-gui"|"xsim-vcd")
        SIMULATOR="xsim"
        ;;
    *)
        SIMULATOR="questa"
        ;;
esac

# 시뮬레이터별 변수 설정
if [ "$SIMULATOR" = "questa" ]; then
    VLOG="vlog"
    VSIM="vsim"
    VLIB="vlib"
elif [ "$SIMULATOR" = "xsim" ]; then
    # xsim 명령어 존재 확인
    if ! command -v xvlog &> /dev/null || ! command -v xelab &> /dev/null || ! command -v xsim &> /dev/null; then
        echo "오류: xsim (Xilinx 시뮬레이터)가 설치되어 있지 않습니다."
        echo "Vivado를 설치하거나, QuestaSim 모드를 사용하세요."
        echo "사용 가능한 모드: batch, gui, vcd, wave, check"
        exit 1
    fi
    VLOG="xvlog"
    VSIM="xsim"
    VLIB=""  # xsim은 라이브러리 생성이 필요 없음
    XELAB="xelab"

    # Xilinx XPM 라이브러리 경로 설정
    XPM_FIFO_PATH="/tools/Xilinx/2025.1/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv"
    XPM_CDC_PATH="/tools/Xilinx/2025.1/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv"
    XPM_MEMORY_PATH="/tools/Xilinx/2025.1/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv"
    GLBL_PATH="/tools/Xilinx/2025.1/data/verilog/src/glbl.v"
fi

# 파일 경로 설정
PROJECT_DIR="/home/wslee/repos/fpga_vsim_cli_test"
DESIGN_DIR="$PROJECT_DIR"
SIM_DIR="$PROJECT_DIR/sim_fifo_example"

# 디자인 파일들
DESIGN_FILES="\
    $SIM_DIR/axis_fifo_example_top.v \
    $DESIGN_DIR/axis_fifo_xpm.v \
    $SIM_DIR/axis_counter_src.v \
    $SIM_DIR/axis_sink_checker.v"

# 테스트벤치 파일
TB_FILE="$SIM_DIR/tb_axis_fifo_example.sv"

# 탑 모듈 이름
TOP_MODULE="tb_axis_fifo_example"

echo "=== AXIS FIFO 예제 시뮬레이션 시작 ==="
echo "모드: $MODE"
echo "시뮬레이터: $SIMULATOR"
echo "프로젝트 디렉토리: $PROJECT_DIR"
echo "시뮬레이션 디렉토리: $SIM_DIR"
echo ""

# 작업 디렉토리 이동
cd $SIM_DIR

# 라이브러리 생성 (QuestaSim만 필요)
if [ "$SIMULATOR" = "questa" ]; then
    echo "라이브러리 초기화..."
    $VLIB work
    if [ $? -ne 0 ]; then
        echo "라이브러리 생성 실패!"
        exit 1
    fi
else
    echo "xsim 시뮬레이터 준비..."
fi

# 문법 체크 모드
if [ "$MODE" = "check" ]; then
    echo "문법 체크만 수행합니다..."
    if [ "$SIMULATOR" = "xsim" ]; then
        # XPM 라이브러리 포함해서 체크
        $VLOG -sv -work xpm_lib --define SIMULATION $GLBL_PATH $XPM_CDC_PATH $XPM_MEMORY_PATH $XPM_FIFO_PATH $DESIGN_FILES $TB_FILE
    else
        $VLOG -sv $DESIGN_FILES $TB_FILE
    fi
    if [ $? -eq 0 ]; then
        echo "문법 체크 통과!"
    else
        echo "문법 오류 발견!"
        exit 1
    fi
    exit 0
fi

echo "1. SystemVerilog/Verilog 파일 컴파일..."
if [ "$SIMULATOR" = "questa" ]; then
    $VLOG -sv $DESIGN_FILES $TB_FILE
elif [ "$SIMULATOR" = "xsim" ]; then
    # XPM 라이브러리 파일들 먼저 컴파일
    echo "  - XPM 라이브러리 컴파일..."
    $VLOG -sv -work xpm_lib --define SIMULATION --relax $GLBL_PATH $XPM_CDC_PATH $XPM_MEMORY_PATH $XPM_FIFO_PATH
    if [ $? -ne 0 ]; then
        echo "XPM 라이브러리 컴파일 실패!"
        exit 1
    fi

    # 디자인 파일들 컴파일
    echo "  - 디자인 파일들 컴파일..."
    $VLOG -sv $DESIGN_FILES $TB_FILE
fi
if [ $? -ne 0 ]; then
    echo "컴파일 실패!"
    exit 1
fi

# xsim의 경우 엘라보레이션 단계 추가
if [ "$SIMULATOR" = "xsim" ]; then
    echo "2. 디자인 엘라보레이션..."
    $XELAB -debug typical -L xpm_lib --define SIMULATION --relax $TOP_MODULE xpm_lib.glbl -s ${TOP_MODULE}_sim
    if [ $? -ne 0 ]; then
        echo "엘라보레이션 실패!"
        exit 1
    fi
    echo "3. 시뮬레이션 실행..."
else
    echo "2. 시뮬레이션 실행..."
fi

# 모드에 따른 시뮬레이션 실행
case $MODE in
    "gui")
        echo "GUI 모드로 시뮬레이션 실행..."
        $VSIM -gui $TOP_MODULE
        ;;
    "wave")
        echo "파형 뷰어와 함께 시뮬레이션 실행..."
        $VSIM -gui $TOP_MODULE
        ;;
    "vcd")
        echo "VCD 파일 생성을 위해 시뮬레이션 실행..."
        $VSIM -c -do "vcd file ${TOP_MODULE}.vcd; vcd add -r *; run -all; quit" $TOP_MODULE
        echo ""
        echo "VCD 파일이 생성되었습니다. GTKWave 등으로 확인하세요."
        ;;
    "xsim")
        echo "xsim 배치 모드로 시뮬레이션 실행..."
        $VSIM ${TOP_MODULE}_sim -runall
        ;;
    "xsim-gui")
        echo "xsim GUI 모드로 시뮬레이션 실행..."
        $VSIM ${TOP_MODULE}_sim -gui
        ;;
    "xsim-vcd")
        echo "xsim으로 VCD 파일 생성을 위해 시뮬레이션 실행..."
        $VSIM ${TOP_MODULE}_sim -testplusarg dump_vcd -runall
        echo ""
        echo "VCD 파일이 생성되었습니다. GTKWave 등으로 확인하세요."
        ;;
    "batch"|*)
        echo "배치 모드로 시뮬레이션 실행..."
        $VSIM -c -do "run -all; quit" $TOP_MODULE
        ;;
esac

if [ $? -ne 0 ]; then
    echo "시뮬레이션 실패!"
    exit 1
fi

echo ""
echo "=== 시뮬레이션 완료 ==="
echo "=== 시뮬레이션 완료 ==="