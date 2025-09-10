"""
axis_master_file_v2.sv를 위한 cocotb 테스트
이 모듈은 파일에서 데이터를 읽어 AXI4-Stream으로 전송하는 마스터 모듈을 테스트합니다.
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.binary import BinaryValue
import random
import os

class AxisMasterTester:
    """AXI4-Stream Master 테스터 클래스"""

    def __init__(self, dut):
        self.dut = dut
        self.received_data = []
        self.expected_data = []

    def to_signed_32bit(self, value):
        """Convert 32-bit unsigned value to signed 32-bit integer"""
        # Handle negative values for 32-bit signed integers
        if isinstance(value, str):
            # Handle hex strings
            if value.startswith('0x') or value.startswith('0X'):
                unsigned_val = int(value, 16)
            else:
                unsigned_val = int(value)
        else:
            unsigned_val = int(value)

        # Convert to signed 32-bit (2's complement)
        if unsigned_val & 0x80000000:  # MSB is set (negative in 2's complement)
            return (unsigned_val - 0x100000000)
        else:
            return unsigned_val

    async def reset_dut(self):
        """DUT 리셋"""
        self.dut.aresetn.value = 0
        self.dut.i_start.value = 0
        self.dut.i_loop.value = 0
        self.dut.i_restart.value = 0
        self.dut.i_pause.value = 0
        self.dut.i_gap_cycles.value = 0
        self.dut.i_reload.value = 0
        self.dut.m_axis_tready.value = 1

        await ClockCycles(self.dut.aclk, 5)
        self.dut.aresetn.value = 1
        await ClockCycles(self.dut.aclk, 5)

    def load_expected_data(self, filename="data.csv"):
        """예상 데이터 로드"""
        self.expected_data = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            # Parse as hex or decimal, then convert to signed 32-bit
                            if line.startswith('0x') or line.startswith('0X'):
                                unsigned_val = int(line, 16)
                            else:
                                unsigned_val = int(line)

                            # Convert to signed 32-bit integer
                            value = unsigned_val
                            self.expected_data.append(value)
                        except ValueError:
                            continue

    def reset_monitor(self):
        """모니터 데이터 초기화"""
        self.received_data = []

    async def axis_monitor(self):
        """AXI4-Stream 모니터 - 수신된 데이터 기록"""
        self.reset_monitor()
        while True:
            await RisingEdge(self.dut.aclk)
            try:
                # 'x' 값 처리를 위한 안전한 비교
                tvalid = self.dut.m_axis_tvalid.value
                tready = self.dut.m_axis_tready.value

                if str(tvalid) == '1' and str(tready) == '1':
                    # Convert DUT output to signed 32-bit integer
                    raw_data = int(self.dut.m_axis_tdata.value)
                    data = self.to_signed_32bit(raw_data)
                    tlast = int(self.dut.m_axis_tlast.value)
                    self.received_data.append((data, tlast))
            except (ValueError, TypeError):
                # 'x' 또는 'z' 값이 있을 때 무시
                continue

    async def apply_backpressure(self, pattern=None):
        """백프레셔 적용"""
        if pattern is None:
            # 랜덤 백프레셔
            while True:
                await RisingEdge(self.dut.aclk)
                if random.random() < 0.3:  # 30% 확률로 백프레셔
                    self.dut.m_axis_tready.value = 0
                    await ClockCycles(self.dut.aclk, random.randint(1, 5))
                    self.dut.m_axis_tready.value = 1
        else:
            # 패턴 기반 백프레셔
            for ready in pattern:
                await RisingEdge(self.dut.aclk)
                self.dut.m_axis_tready.value = ready

@cocotb.test()
async def test_basic_oneshot_transmission(dut):
    """Basic one-shot transmission test"""
    tester = AxisMasterTester(dut)

    # Start clock
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize and start monitor
    tester.reset_monitor()
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # Reset DUT
    await tester.reset_dut()

    # Load expected data
    tester.load_expected_data()

    # 파일 리로드 (안전하게)
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 원샷 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # busy 신호 확인
    await RisingEdge(dut.o_busy)
    dut._log.info("Transmission started - busy signal detected")

    # done 펄스 대기
    while True:
        await RisingEdge(dut.aclk)
        if dut.o_done_pulse.value == 1:
            dut._log.info("Transmission completed - done_pulse detected")
            break

    # 추가로 몇 사이클 대기
    await ClockCycles(dut.aclk, 10)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert len(tester.received_data) > 0, "Data not transmitted"

    # 마지막 데이터의 tlast 확인
    last_data, last_tlast = tester.received_data[-1]
    assert last_tlast == 1, f"Last data's tlast is not 1: {last_tlast}"

    # 데이터 내용 검증 (처음 몇 개만)
    if len(tester.expected_data) > 0:
        for i, (received, _) in enumerate(tester.received_data[:min(10, len(tester.expected_data))]):
            expected = tester.expected_data[i]
            # Verify data matches (both values are already converted to signed 32-bit)
            assert received == expected, f"Data mismatch at index {i}: received={received:12d}, expected={expected:12d}"

    dut._log.info(f"One-shot transmission test completed: {len(tester.received_data)} words transmitted")

@cocotb.test()
async def test_loop_mode(dut):
    """Loop mode test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 리셋
    await tester.reset_dut()

    # 예상 데이터 로드
    tester.load_expected_data()

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 루프 모드 활성화
    dut.i_loop.value = 1
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # busy 신호 확인
    await RisingEdge(dut.o_busy)
    dut._log.info("Loop mode transmission started")

    # 여러 루프 사이클 대기 (데이터 크기의 2배 정도)
    expected_cycles = len(tester.expected_data) * 2 if len(tester.expected_data) > 0 else 200
    await ClockCycles(dut.aclk, expected_cycles)

    # 루프 모드 비활성화
    dut.i_loop.value = 0

    # 현재 전송이 완료될 때까지 대기
    await ClockCycles(dut.aclk, 50)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert len(tester.received_data) > len(tester.expected_data), "루프 모드에서 데이터가 반복 전송되지 않았습니다"

    dut._log.info(f"Loop mode test completed: {len(tester.received_data)} words transmitted")

@cocotb.test()
async def test_pause_resume(dut):
    """Pause/resume test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 리셋
    await tester.reset_dut()

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 몇 개 데이터 전송 대기
    await ClockCycles(dut.aclk, 50)

    # 일시정지
    dut.i_pause.value = 1
    await RisingEdge(dut.aclk)  # pause 신호가 적용될 때까지 대기
    dut._log.info("Transmission paused")
    pause_data_count = len(tester.received_data)

    # 정지 상태에서 대기
    await ClockCycles(dut.aclk, 50)

    # 정지 중에는 새로운 데이터가 전송되지 않아야 함 (약간의 여유 허용)
    current_count = len(tester.received_data)
    assert current_count <= pause_data_count + 1, f"일시정지 중에 너무 많은 데이터가 전송되었습니다: {current_count} vs {pause_data_count}"

    # 재개
    dut.i_pause.value = 0
    dut._log.info("Transmission resumed")

    # 전송 완료 대기
    while True:
        await RisingEdge(dut.aclk)
        if dut.o_done_pulse.value == 1:
            break

    await ClockCycles(dut.aclk, 10)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert len(tester.received_data) > pause_data_count, "재개 후 데이터 전송이 계속되지 않았습니다"

    dut._log.info(f"Pause/resume test completed: {len(tester.received_data)} words transmitted")

@cocotb.test()
async def test_restart_functionality(dut):
    """Restart functionality test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 리셋
    await tester.reset_dut()

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 몇 개 데이터 전송 후 재시작
    await ClockCycles(dut.aclk, 20)

    dut.i_restart.value = 1
    await RisingEdge(dut.aclk)
    dut.i_restart.value = 0
    dut._log.info("Restart signal applied")

    # 재시작 후 다시 시작
    await ClockCycles(dut.aclk, 5)
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 전송 완료 대기
    while True:
        await RisingEdge(dut.aclk)
        if dut.o_done_pulse.value == 1:
            break

    await ClockCycles(dut.aclk, 10)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert len(tester.received_data) > 0, "재시작 후 데이터 전송이 되지 않았습니다"

    dut._log.info(f"Restart functionality test completed: {len(tester.received_data)} words transmitted")

@cocotb.test()
async def test_gap_cycles(dut):
    """Gap cycles test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 리셋
    await tester.reset_dut()

    # 갭 사이클 설정 (5 사이클)
    dut.i_gap_cycles.value = 5

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 전송 완료까지 대기 (갭 때문에 더 오래 걸림)
    start_time = 0
    while True:
        await RisingEdge(dut.aclk)
        start_time += 1
        if dut.o_done_pulse.value == 1:
            break
        if start_time > 10000:  # 타임아웃
            break

    await ClockCycles(dut.aclk, 10)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert len(tester.received_data) > 0, "갭 사이클 설정 시 데이터 전송이 되지 않았습니다"

    dut._log.info(f"Gap cycles test completed: {len(tester.received_data)} words transmitted, {start_time} cycles taken")

@cocotb.test()
async def test_backpressure_handling(dut):
    """Backpressure handling test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 백프레셔 적용
    backpressure_task = cocotb.start_soon(tester.apply_backpressure())

    # 리셋
    await tester.reset_dut()

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 전송 완료까지 대기 (백프레셔 때문에 더 오래 걸림)
    start_time = 0
    while True:
        await RisingEdge(dut.aclk)
        start_time += 1
        if dut.o_done_pulse.value == 1:
            break
        if start_time > 20000:  # 타임아웃
            break

    await ClockCycles(dut.aclk, 10)

    # 백프레셔 태스크 종료
    backpressure_task.kill()

    # 모니터 종료
    monitor_task.kill()

    # tready를 다시 1로 설정
    dut.m_axis_tready.value = 1

    # 결과 검증
    assert len(tester.received_data) > 0, "백프레셔 상황에서 데이터 전송이 되지 않았습니다"

    dut._log.info(f"Backpressure handling test completed: {len(tester.received_data)} words transmitted, {start_time} cycles taken")

@cocotb.test()
async def test_sent_count_monitoring(dut):
    """Transmission count monitoring test"""
    tester = AxisMasterTester(dut)

    # 클럭 시작
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # 모니터 시작
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # 리셋
    await tester.reset_dut()

    # 파일 리로드
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # 초기 카운트 확인
    initial_count = int(dut.o_sent_count.value)

    # 전송 시작
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # 전송 완료 대기하면서 카운트 모니터링
    while True:
        await RisingEdge(dut.aclk)
        current_count = int(dut.o_sent_count.value)
        if dut.o_done_pulse.value == 1:
            final_count = current_count
            break

    await ClockCycles(dut.aclk, 10)

    # 모니터 종료
    monitor_task.kill()

    # 결과 검증
    assert final_count == len(tester.received_data), f"전송 카운트 불일치: 카운트={final_count}, 실제수신={len(tester.received_data)}"

    dut._log.info(f"Transmission count monitoring test completed: {final_count} words counted")


@cocotb.test()
async def test_csv_direct_comparison(dut):
    """Comprehensive test that directly compares CSV file data with DUT output"""
    tester = AxisMasterTester(dut)

    # Start clock
    clock = Clock(dut.aclk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Initialize and start monitor
    tester.reset_monitor()
    monitor_task = cocotb.start_soon(tester.axis_monitor())

    # Reset DUT
    await tester.reset_dut()

    # Load expected data from CSV file
    csv_filename = "data.csv"
    if not os.path.exists(csv_filename):
        dut._log.error(f"CSV file {csv_filename} does not exist")
        assert False, f"CSV file {csv_filename} not found"

    tester.load_expected_data(csv_filename)

    if len(tester.expected_data) == 0:
        dut._log.error(f"No valid data found in CSV file {csv_filename}")
        assert False, f"No valid data found in {csv_filename}"

    dut._log.info(f"Loaded {len(tester.expected_data)} data points from CSV file")
    dut._log.info(f"First 5 values (signed 32-bit): {[f'{val:12d}' for val in tester.expected_data[:5]]}")
    dut._log.info(f"Last 5 values (signed 32-bit): {[f'{val:12d}' for val in tester.expected_data[-5:]]}")

    # Show range information for signed values
    if tester.expected_data:
        min_val = min(tester.expected_data)
        max_val = max(tester.expected_data)
        dut._log.info(f"Value range: {min_val} to {max_val} (signed 32-bit)")

    # Reload file
    dut.i_reload.value = 1
    await RisingEdge(dut.aclk)
    dut.i_reload.value = 0
    await ClockCycles(dut.aclk, 5)

    # Start transmission
    dut.i_start.value = 1
    await RisingEdge(dut.aclk)
    dut.i_start.value = 0

    # Wait for busy signal
    await RisingEdge(dut.o_busy)
    dut._log.info("Data transmission started")

    # Receive and compare data
    comparison_count = 0
    match_count = 0
    mismatch_details = []

    # Compare all expected data
    for expected_idx, expected_value in enumerate(tester.expected_data):
        # Wait for valid data from DUT
        timeout_counter = 0
        while len(tester.received_data) <= expected_idx:
            await RisingEdge(dut.aclk)
            timeout_counter += 1
            if timeout_counter > 10000:  # Timeout setting
                dut._log.error(f"Timeout: Failed to receive data at index {expected_idx}")
                break

        if len(tester.received_data) <= expected_idx:
            dut._log.error(f"Failed to receive data from DUT at index {expected_idx}")
            break

        # Get received data
        actual_data, tlast = tester.received_data[expected_idx]

        # Compare data
        if actual_data != expected_value:
            error_msg = f"Data mismatch at index {expected_idx}: expected={expected_value:12d}, actual={actual_data:12d}"
            dut._log.error(error_msg)
            mismatch_details.append(error_msg)
        else:
            match_count += 1

        comparison_count += 1

        # Log progress (every 50 items or at the end)
        if comparison_count % 50 == 0 or comparison_count == len(tester.expected_data):
            progress_percent = (comparison_count / len(tester.expected_data)) * 100
            dut._log.info(f"✓ Verified {comparison_count}/{len(tester.expected_data)} data points ({progress_percent:.1f}%)")

    # Wait for transmission completion
    while True:
        await RisingEdge(dut.aclk)
        if dut.o_done_pulse.value == 1:
            break

    # Additional wait
    await ClockCycles(dut.aclk, 10)

    # Stop monitor
    monitor_task.kill()

    # Analyze results
    total_expected = len(tester.expected_data)
    total_received = len(tester.received_data)
    mismatch_count = len(mismatch_details)

    # Calculate success rates
    if total_expected > 0:
        match_percentage = (match_count / total_expected) * 100
        mismatch_percentage = (mismatch_count / total_expected) * 100
    else:
        match_percentage = 0
        mismatch_percentage = 0

    dut._log.info("=" * 70)
    dut._log.info("CSV Direct Comparison Test Results Summary")
    dut._log.info("=" * 70)
    dut._log.info(f"Data points loaded from CSV file: {total_expected}")
    dut._log.info(f"Data points received from DUT: {total_received}")
    dut._log.info(f"Data points successfully compared: {comparison_count}")
    dut._log.info("-" * 70)
    dut._log.info(f"✓ Matching data points: {match_count} ({match_percentage:.2f}%)")
    dut._log.info(f"✗ Mismatching data points: {mismatch_count} ({mismatch_percentage:.2f}%)")

    if mismatch_details:
        dut._log.error("Detected mismatches:")
        for detail in mismatch_details[:10]:  # Show first 10 only
            dut._log.error(f"  {detail}")
        if len(mismatch_details) > 10:
            dut._log.error(f"  ... and {len(mismatch_details) - 10} more")

    # Test pass/fail determination
    test_passed = True
    failure_reasons = []

    if total_received != total_expected:
        test_passed = False
        failure_reasons.append(f"Data count mismatch: expected {total_expected}, received {total_received}")

    if mismatch_count > 0:
        test_passed = False
        failure_reasons.append(f"Data mismatches detected: {mismatch_count} items")

    if match_count != total_expected:
        test_passed = False
        failure_reasons.append(f"Non-matching data: {total_expected - match_count} items")

    dut._log.info("-" * 70)

    # 수신 데이터 앞 50개 출력
    # tester.received_data

    display_num = 100
    dut._log.info(f"First {display_num} received data (showing signed 32-bit values): ")
    for idx, data in enumerate(tester.received_data[:display_num]):
        if idx < len(tester.expected_data):
            expected = tester.expected_data[idx]
            match_status = "T" if data[0] == expected else "F"
            dut._log.info(f"  {idx:5d}: {match_status} R={data[0]:12d} E={expected:12d}")
        else:
            dut._log.info(f"  {idx:5d}: R={data[0]:12d} (no expected data)")



    dut._log.info("-" * 70)
    if test_passed:
        dut._log.info("✓ Test Result: PASS")
        dut._log.info("✓ CSV Direct Comparison Test PASSED: All data matches perfectly!")
    else:
        dut._log.error("✗ Test Result: FAIL")
        for reason in failure_reasons:
            dut._log.error(f"  - {reason}")
        dut._log.info("=" * 70)
        assert False, f"Test failed: {'; '.join(failure_reasons)}"

    dut._log.info("=" * 70)
