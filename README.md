# Xilinx Vivado CLI 시뮬레이션 예제 - 동기 가산기

이 프로젝트는 CLI에서 Xilinx Vivado를 이용하여 Verilog 시뮬레이션을 실행하는 기본 예제입니다. 8비트 동기 가산기를 구현하고 테스트합니다.

## 파일 구조

```
fpga_vsim_cli_test/
├── sync_adder.v      # 동기 가산기 메인 모듈
├── tb_sync_adder.v   # 테스트벤치
├── run_sim.tcl       # Vivado TCL 스크립트
├── Makefile          # 빌드 자동화
└── README.md         # 이 파일
```

## 필요 조건

- Xilinx Vivado (2019.1 이상 권장)
- Linux 환경
- Make 유틸리티
- Bash shell

## 환경 설정

시뮬레이션 실행 전에 Xilinx 환경을 설정해야 합니다:

```bash
source /tools/Xilinx/2025.1/Vivado/settings64.sh
export DISPLAY=localhost:11
```

또는 제공된 스크립트를 사용:
```bash
./setup_env.sh
```

## 동기 가산기 모듈 설명

`sync_adder.v`는 다음 기능을 가진 8비트 동기 가산기입니다:

### 포트 설명
- `clk`: 클럭 신호
- `rst_n`: 리셋 신호 (active low)
- `enable`: 인에이블 신호
- `a[7:0]`: 첫 번째 8비트 입력
- `b[7:0]`: 두 번째 8비트 입력
- `sum[8:0]`: 9비트 출력 (캐리 포함)
- `valid`: 출력 유효 신호

### 동작 특성
- 클럭의 상승 에지에 동기화
- `enable`이 1일 때만 덧셈 수행
- `rst_n`이 0일 때 출력 초기화
- 오버플로우 검출 가능 (9번째 비트)

## 사용법

### 1. 기본 시뮬레이션 (가장 빠름)
```bash
make sim
```
또는
```bash
make
```

### 2. 파형 뷰어와 함께 시뮬레이션
```bash
make wave
```

### 3. Vivado GUI 모드
```bash
make gui
```

### 4. Vivado 배치 모드
```bash
make batch
```

### 5. 문법 체크만 수행
```bash
make check
```

### 6. GTKWave로 VCD 파일 보기
```bash
make gtkwave
```

### 7. 생성된 파일 정리
```bash
make clean
```

### 8. 도움말 보기
```bash
make help
```

## VSCode 사용법

이 프로젝트는 VSCode에서 편리하게 사용할 수 있도록 설정되어 있습니다.

### 키보드 단축키
- `Ctrl+F5`: 기본 시뮬레이션 실행
- `Ctrl+Shift+F5`: 안전한 시뮬레이션 실행
- `Ctrl+F6`: 파형 뷰어로 시뮬레이션
- `Ctrl+Shift+C`: 문법 체크
- `Ctrl+Shift+Delete`: 정리

### 명령 팔레트 사용
1. `Ctrl+Shift+P`로 명령 팔레트 열기
2. "Tasks: Run Task" 선택
3. 원하는 작업 선택

### 빌드 작업 실행
- `Ctrl+Shift+B`: 기본 빌드 작업 (시뮬레이션) 실행

### 사용 가능한 VSCode 작업들
- **Verilog: 시뮬레이션 실행** - 기본 시뮬레이션
- **Verilog: 안전한 시뮬레이션 실행** - 더 안전한 종료 방식
- **Verilog: 파형 뷰어로 시뮬레이션** - GUI 파형 뷰어
- **Verilog: Vivado GUI 시뮬레이션** - Vivado GUI 모드
- **Verilog: 문법 체크** - 코드 문법 검사
- **Verilog: GTKWave 파형 보기** - GTKWave로 VCD 파일 열기
- **Verilog: 정리** - 생성된 파일 정리
- **Xilinx: 환경 설정 확인** - Xilinx 환경 상태 확인

## 시뮬레이션 결과

테스트벤치는 다음 테스트 케이스들을 실행합니다:

1. **기본 덧셈**: 15 + 25 = 40
2. **오버플로우**: 200 + 100 = 300 (캐리 발생)
3. **Enable 비활성화**: 덧셈 수행하지 않음
4. **Enable 재활성화**: 50 + 50 = 100
5. **영 덧셈**: 0 + 0 = 0
6. **최대값**: 255 + 255 = 510 (캐리 발생)
7. **리셋 테스트**: 모든 출력이 0으로 초기화

## 출력 파일

시뮬레이션 실행 후 다음 파일들이 생성됩니다:

- `sync_adder.vcd`: GTKWave에서 볼 수 있는 파형 파일
- `vivado_project/`: Vivado 프로젝트 디렉토리 (GUI 모드 사용 시)
- `xsim.dir/`: xsim 시뮬레이터 작업 디렉토리
- 각종 로그 파일들

## 문제 해결

### Vivado 경로 문제
Vivado가 PATH에 없는 경우:
```bash
source /opt/Xilinx/Vivado/2023.1/settings64.sh  # 버전에 맞게 조정
make sim
```

### 권한 문제
```bash
chmod +x Makefile
```

### 파일 정리가 필요한 경우
```bash
make clean
```

## 고급 사용법

### 파라미터 변경
`sync_adder.v`에서 WIDTH 파라미터를 변경하여 다른 비트 폭의 가산기를 테스트할 수 있습니다:

```verilog
parameter WIDTH = 16  // 16비트 가산기로 변경
```

### 클럭 주파수 변경
`tb_sync_adder.v`에서 CLK_PERIOD를 변경:

```verilog
parameter CLK_PERIOD = 5; // 200MHz (5ns 주기)
```

### 추가 테스트 케이스
테스트벤치에 새로운 테스트 케이스를 추가하여 더 많은 시나리오를 검증할 수 있습니다.

## 참고사항

- 이 예제는 교육 목적으로 작성되었습니다
- 실제 FPGA 구현 시에는 타이밍 제약과 최적화를 고려해야 합니다
- 더 복잡한 디자인의 경우 별도의 제약 파일(.xdc)이 필요할 수 있습니다
