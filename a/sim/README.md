# D Flip-Flop cocotb Testing

이 디렉토리는 `ff.v` 모듈에 대한 cocotb 기반 Python 테스트를 포함합니다.

## 파일 구조

- `test_ff.py` - cocotb 테스트 케이스들
- `Makefile` - cocotb 시뮬레이션 실행을 위한 Makefile
- `requirements.txt` - Python 의존성 패키지 목록
- `README.md` - 이 문서

## 설치 및 설정

### 1. Python 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 시뮬레이터 설치
다음 중 하나 이상의 시뮬레이터가 필요합니다:
- **Icarus Verilog** (기본값, 오픈소스)
- **Questa/ModelSim** (상용)
- **Vivado XSIM** (Xilinx)

#### Ubuntu/Debian에서 Icarus Verilog 설치:
```bash
sudo apt-get install iverilog gtkwave
```

## 테스트 실행

### 기본 테스트 실행 (Icarus Verilog)
```bash
make
```

### 특정 시뮬레이터로 테스트 실행
```bash
# Questa/ModelSim 사용
make SIM=questa

# Vivado XSIM 사용
make SIM=xsim

# Icarus Verilog 사용 (기본값)
make SIM=icarus
```

### 파형 보기
```bash
# 테스트 실행 후 파형 보기
make view-waves
```

### 모든 사용 가능한 시뮬레이터로 테스트
```bash
make test-all
```

### 도움말 보기
```bash
make help
```

## 테스트 케이스

`test_ff.py`에 포함된 테스트 케이스들:

1. **`test_ff_reset`** - 비동기 리셋 기능 테스트
2. **`test_ff_basic_operation`** - 기본 D 플립플롭 동작 테스트
3. **`test_ff_random_data`** - 랜덤 데이터 패턴 테스트
4. **`test_ff_reset_during_operation`** - 동작 중 리셋 테스트
5. **`test_ff_setup_hold_timing`** - 기본 타이밍 테스트
6. **`test_ff_comprehensive`** - 종합 테스트

## 테스트 결과

테스트 실행 후 다음과 같은 출력을 확인할 수 있습니다:
- 각 테스트 케이스의 통과/실패 상태
- 상세한 로그 메시지
- 파형 파일 (dump.fst, dump.vcd 등)

## 파형 분석

생성된 파형 파일을 GTKWave로 분석할 수 있습니다:
```bash
# FST 형식 (Icarus)
gtkwave dump.fst

# VCD 형식
gtkwave dump.vcd

# 또는 make 타겟 사용
make view-waves
```

## 문제 해결

### 일반적인 문제들

1. **cocotb를 찾을 수 없음**
   ```bash
   pip install cocotb
   ```

2. **시뮬레이터를 찾을 수 없음**
   - PATH에 시뮬레이터가 있는지 확인
   - 라이센스 설정 확인 (상용 시뮬레이터의 경우)

3. **파형 파일이 생성되지 않음**
   ```bash
   make WAVES=1
   ```

## 추가 정보

- cocotb 공식 문서: https://docs.cocotb.org/
- 테스트 추가나 수정 시 `test_ff.py` 파일을 편집하세요
- 새로운 시뮬레이터 지원이 필요하면 `Makefile`을 수정하세요
