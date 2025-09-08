# Dataover Module Cocotb Testbench

32비트 입력 데이터가 threshold보다 큰지 비교하는 dataover 모듈의 cocotb 테스트벤치입니다.

## Module Description

`dataover` 모듈은 다음과 같은 기능을 제공합니다:
- 32비트 입력 데이터 (`data_in`)와 32비트 threshold (`threshold`) 비교
- `data_in > threshold`이면 `data_over = 1`, 그렇지 않으면 `data_over = 0`

## File Structure

```
sim_dataover/
├── Makefile              # Cocotb simulation makefile
├── test_dataover.py      # Cocotb testbench
├── requirements.txt      # Python dependencies
└── README.md            # This file
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
   - `data_in < threshold` → `data_over = 0`
   - `data_in = threshold` → `data_over = 0`
   - `data_in > threshold` → `data_over = 1`

2. **Edge Cases**: 극한값 테스트
   - 최대 32비트 값들
   - 0 값들
   - 큰 숫자들

3. **Random Test**: 무작위 값들로 50회 테스트

4. **Boundary Conditions**: 경계값 조건 테스트

5. **Comprehensive Test**: 모든 시나리오를 포함한 종합 테스트

## Waveform Viewing

시뮬레이션 실행 후 `dataover_sim.vcd` 파일이 생성됩니다. GTKWave로 파형을 확인할 수 있습니다:

```bash
gtkwave dataover_sim.vcd
```

## Expected Output

성공적인 테스트 실행 시 다음과 같은 출력을 볼 수 있습니다:

```
✓ Test 1 passed: 100 < 200 -> data_over=0
✓ Test 2 passed: 200 = 200 -> data_over=0  
✓ Test 3 passed: 300 > 200 -> data_over=1
✓ Maximum value test passed
✓ Zero values test passed
✓ One > zero test passed
✓ Large number test passed
✓ Random test passed: 50/50 tests
✓ Comprehensive test completed successfully
```
