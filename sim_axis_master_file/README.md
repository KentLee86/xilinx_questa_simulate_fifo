# axis_master_file_v2 테스트

이 디렉토리는 `axis_master_file_v2.sv` 모듈을 위한 cocotb 테스트를 포함합니다.

## 모듈 개요

`axis_master_file_v2`는 파일에서 데이터를 읽어 AXI4-Stream 인터페이스로 전송하는 마스터 모듈입니다.

### 주요 기능
- CSV 또는 바이너리 파일에서 데이터 로드
- 원샷 또는 루프 모드 전송
- 런타임 제어 (시작, 일시정지, 재시작, 리로드)
- 갭 사이클 삽입
- 백프레셔 핸들링
- 전송 상태 모니터링

## 테스트 구조

### 테스트 케이스
1. **test_basic_oneshot_transmission**: 기본 원샷 전송 테스트
2. **test_loop_mode**: 루프 모드 동작 테스트
3. **test_pause_resume**: 일시정지/재개 기능 테스트
4. **test_restart_functionality**: 재시작 기능 테스트
5. **test_gap_cycles**: 갭 사이클 기능 테스트
6. **test_backpressure_handling**: 백프레셔 핸들링 테스트
7. **test_sent_count_monitoring**: 전송 카운트 모니터링 테스트

### 파일 구조
```
sim_axis_master_file/
├── axis_master_file_v2.sv    # DUT 모듈
├── test_master_file.py       # cocotb 테스트
├── data.csv                  # 테스트 데이터 파일
├── generate_data.py          # 데이터 생성 스크립트
├── Makefile                  # 빌드/시뮬레이션 설정
├── requirements.txt          # Python 의존성
└── README.md                 # 이 파일
```

## 사용법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 시뮬레이션 실행

#### 모든 테스트 실행
```bash
make sim
```

#### 특정 시뮬레이터 사용
```bash
make sim SIM=questa    # QuestaSim/ModelSim
make sim SIM=icarus    # Icarus Verilog
make sim SIM=verilator # Verilator
```

#### 특정 테스트만 실행
```bash
make test_basic_oneshot_transmission
make test_loop_mode
make test_pause_resume
```

#### 웨이브폼 활성화
```bash
make sim WAVES=1
```

#### 디버그 로그 활성화
```bash
make sim COCOTB_LOG_LEVEL=DEBUG
```

### 3. 정리
```bash
make clean
```

## 테스트 데이터

`data.csv` 파일은 사인파 데이터를 포함하며, `generate_data.py`로 생성됩니다:

```bash
python generate_data.py
```

## 시뮬레이션 결과

테스트가 성공적으로 실행되면 다음과 같은 출력을 볼 수 있습니다:

```
INFO     cocotb                         원샷 전송 테스트 완료: 5002개 워드 전송
INFO     cocotb                         루프 모드 테스트 완료: 10004개 워드 전송
INFO     cocotb                         일시정지/재개 테스트 완료: 5002개 워드 전송
...
```

## 문제 해결

### 일반적인 문제들

1. **시뮬레이터 찾을 수 없음**
   - PATH에 시뮬레이터가 있는지 확인
   - 라이선스가 유효한지 확인

2. **파일 권한 오류**
   ```bash
   chmod +x generate_data.py
   ```

3. **Python 모듈 오류**
   ```bash
   pip install --upgrade cocotb
   ```

### 로그 확인
- `sim_build/sim.log`: 시뮬레이션 로그
- `results.xml`: 테스트 결과 (JUnit 형식)

## 확장

새로운 테스트를 추가하려면:

1. `test_master_file.py`에 `@cocotb.test()` 데코레이터를 사용한 함수 추가
2. `AxisMasterTester` 클래스에 필요한 헬퍼 메소드 추가
3. `Makefile`에서 필요시 새로운 타겟 추가
