#!/bin/bash
# Xilinx Vivado 환경 설정 스크립트

echo "=== Xilinx Vivado 환경 설정 ==="

# Vivado 환경 설정
if [ -f "/tools/Xilinx/2025.1/Vivado/settings64.sh" ]; then
    echo "Vivado settings64.sh 로딩 중..."
    source /tools/Xilinx/2025.1/Vivado/settings64.sh
    echo "✓ Vivado 환경 설정 완료"
else
    echo "❌ Vivado settings64.sh 파일을 찾을 수 없습니다."
    echo "경로를 확인하세요: /tools/Xilinx/2025.1/Vivado/settings64.sh"
    exit 1
fi

# DISPLAY 환경 변수 설정
export DISPLAY=localhost:11
echo "✓ DISPLAY 설정: $DISPLAY"

# 환경 확인
echo ""
echo "=== 환경 확인 ==="
echo "Vivado 경로: $(which vivado 2>/dev/null || echo '❌ 찾을 수 없음')"
echo "xvlog 경로:  $(which xvlog 2>/dev/null || echo '❌ 찾을 수 없음')"
echo "xsim 경로:   $(which xsim 2>/dev/null || echo '❌ 찾을 수 없음')"
echo "xelab 경로:  $(which xelab 2>/dev/null || echo '❌ 찾을 수 없음')"
echo "DISPLAY:     $DISPLAY"

# 추가 명령어가 있으면 실행
if [ $# -gt 0 ]; then
    echo ""
    echo "=== 명령어 실행: $@ ==="
    exec "$@"
fi
