#!/bin/bash

# 사용법: ./run.sh [sim|sim-gui]
# sim: 배치 모드 (quit 포함)
# sim-gui: GUI 모드 (quit 없음)

if [ "$1" = "sim-gui" ]; then
    echo "=== GUI 모드 시뮬레이션 실행 ==="
    vsim -do "do run.do"
elif [ "$1" = "sim" ] || [ -z "$1" ]; then
    echo "=== 배치 모드 시뮬레이션 실행 ==="
    vsim -c -do "do run.do; quit"
else
    echo "사용법: $0 [sim|sim-gui]"
    echo "  sim     : 배치 모드 시뮬레이션 (기본값)"
    echo "  sim-gui : GUI 모드 시뮬레이션"
    exit 1
fi
