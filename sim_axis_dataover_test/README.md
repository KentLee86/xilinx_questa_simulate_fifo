# Axis Dataover Test

이 프로젝트는 `axis_master_file_v2.sv`와 `dataover.v` 모듈을 통합하여 1,000,000보다 큰 숫자를 제대로 감지하는지 테스트합니다.

## 프로젝트 구조

- `top_axis_dataover.v`: axis_master_file_v2와 dataover를 연결한 top-level 모듈
- `test_axis_dataover.py`: cocotb 테스트벤치
- `generate_test_data.py`: 테스트 데이터 생성 스크립트
- `test_data.csv`: 생성된 테스트 데이터 파일
- `Makefile`: 빌드 및 테스트 실행

## 기능 설명

1. **데이터 전송**: `axis_master_file_v2.sv`가 CSV 파일에서 데이터를 읽어 AXI4-Stream으로 전송
2. **임계값 검사**: `dataover.v`가 각 데이터를 1,000,000과 비교
3. **결과 검증**: cocotb가 데이터 전송과 임계값 검사를 동시에 검증

## 사용 방법

### 1. 테스트 데이터 생성
```bash
make gen_data
```

### 2. 시뮬레이션 실행 (Icarus Verilog 기본)
```bash
make test
```

### 3. 다른 시뮬레이터 사용
```bash
# Questa 사용
make SIM=questa test

# XSIM 사용
make SIM=xsim test
```

### 4. 정리
```bash
# 테스트 데이터만 삭제
make clean_data

# 모든 파일 정리
make clean_all
```

## 테스트 내용

- **기본 테스트**: 모든 테스트 데이터를 전송하고 임계값 비교 검증
- **임계값 경계 테스트**: 999,999 ~ 1,000,001 주변 값들 검증
- **대형 숫자 테스트**: 수백만 ~ 수십억 범위의 큰 숫자들 검증
- **음수 테스트**: 음수 값들이 모두 임계값 이하인지 검증
- **제어 신호 테스트**: 일시정지, 재시작 등의 제어 기능 검증

## 테스트 데이터

`generate_test_data.py`가 생성하는 테스트 데이터는:
- 1,000,000보다 작은 값들 (결과: 0)
- 1,000,000보다 큰 값들 (결과: 1)
- 임계값 주변 값들
- 음수 값들
- 32비트 부호付き 정수 범위의 엣지 케이스들

## 출력 파일

- `axis_dataover_sim.vcd`: 파형 파일 (Icarus 사용시)
- 시뮬레이션 로그는 콘솔에 출력됩니다.

## 요구사항

- cocotb
- Icarus Verilog (또는 다른 지원 시뮬레이터)
- Python 3.6+

## 설치

```bash
pip install cocotb
```

Ubuntu/Debian에서는 추가 패키지 설치 필요:
```bash
sudo apt-get install iverilog
```
