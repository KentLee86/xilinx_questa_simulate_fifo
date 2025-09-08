# Two Dataover Module Cocotb Testbench

하나의 32비트 입력을 100과 200 두 개의 고정된 threshold와 비교하는 two_dataover 모듈의 cocotb 테스트벤치입니다.

## Module Description

`two_dataover` 모듈은 다음과 같은 기능을 제공합니다:
- 32비트 입력 데이터 (`data_in`) 하나를 받습니다
- 내부적으로 두 개의 `dataover` 인스턴스를 사용합니다
- `data_over_100`: `data_in > 100`이면 1, 그렇지 않으면 0
- `data_over_200`: `data_in > 200`이면 1, 그렇지 않으면 0

## Module Hierarchy

```
two_dataover
├── dataover_inst_100 (dataover module instance)
└── dataover_inst_200 (dataover module instance)
```

## Input/Output Behavior

| data_in 범위 | data_over_100 | data_over_200 |
|--------------|---------------|---------------|
| ≤ 100        | 0             | 0             |
| 101 ~ 200    | 1             | 0             |
| > 200        | 1             | 1             |

## File Structure

```
sim_two_dataover/
├── Makefile                 # Cocotb simulation makefile
├── test_two_dataover.py     # Cocotb testbench
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

1. Python 3.7 이상
2. Cocotb 설치
3. Verilog 시뮬레이터 (Icarus Verilog, Questa, 또는 Vivado Simulator)

## Installation

1. 필요한 Python 패키지 설치:
```bash
pip install -r requirements.txt
```

2. Icarus Verilog 설치 (Ubuntu/Debian):
```bash
sudo apt-get install iverilog
```

## Running Tests

### Default (Icarus Verilog)
```bash
make
```

### Specific Simulator
```bash
# Icarus Verilog
make SIM=icarus

# Questa/ModelSim
make SIM=questa

# Xilinx Vivado Simulator
make SIM=xsim
```

### Clean Up
```bash
make clean
```

## Test Cases

테스트벤치는 다음과 같은 테스트 케이스들을 포함합니다:

1. **Basic Test**: 기본적인 비교 연산 테스트
   - `data_in ≤ 100`: 두 출력 모두 0
   - `100 < data_in ≤ 200`: data_over_100=1, data_over_200=0
   - `data_in > 200`: 두 출력 모두 1

2. **Boundary Conditions**: 경계값 조건 테스트
   - 99, 100, 101 (100 주변)
   - 199, 200, 201 (200 주변)

3. **Edge Cases**: 극한값 테스트
   - 0 값
   - 최대 32비트 값
   - 큰 숫자들

4. **Random Test**: 무작위 값들로 30회 테스트

5. **Comprehensive Test**: 모든 시나리오를 포함한 종합 테스트

## Waveform Viewing

시뮬레이션 실행 후 `two_dataover_sim.vcd` 파일이 생성됩니다. GTKWave로 파형을 확인할 수 있습니다:

```bash
gtkwave two_dataover_sim.vcd
```

## Expected Output

성공적인 테스트 실행 시 다음과 같은 출력을 볼 수 있습니다:

```
✓ Test 1 passed: 50 < 100 and 50 < 200 -> both outputs = 0
✓ Test 2 passed: 100 = 100 and 100 < 200 -> both outputs = 0
✓ Test 3 passed: 150 > 100 and 150 < 200 -> data_over_100=1, data_over_200=0
✓ Test 4 passed: 200 > 100 and 200 = 200 -> data_over_100=1, data_over_200=0
✓ Test 5 passed: 300 > 100 and 300 > 200 -> both outputs = 1
```
