"""
D Flip-Flop cocotb testbench
Tests the ff module using cocotb framework
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.result import TestFailure
import random


@cocotb.test()
async def test_ff_reset(dut):
    """Test asynchronous reset functionality"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    cocotb.start_soon(clock.start())

    # Test asynchronous reset
    dut.rst.value = 1
    dut.d.value = 1
    await Timer(20, units="ns")

    # Check that output is 0 regardless of input
    assert dut.q.value == 0, f"Reset failed: expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Asynchronous reset test passed")


@cocotb.test()
async def test_ff_basic_operation(dut):
    """Test basic D flip-flop operation"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    # Test case 1: d=0 -> q=0
    dut.d.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")  # Small delay for signal propagation
    assert dut.q.value == 0, f"Test 1 failed: d=0, expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Test 1 passed: d=0 -> q=0")

    # Test case 2: d=1 -> q=1
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, f"Test 2 failed: d=1, expected q=1, got q={dut.q.value}"
    dut._log.info("✓ Test 2 passed: d=1 -> q=1")

    # Test case 3: d=0 -> q=0 (again)
    dut.d.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 0, f"Test 3 failed: d=0, expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Test 3 passed: d=0 -> q=0")


@cocotb.test()
async def test_ff_random_data(dut):
    """Test D flip-flop with random data patterns"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    # Test with random data for multiple clock cycles
    test_vectors = []
    for i in range(20):
        test_data = random.randint(0, 1)
        test_vectors.append(test_data)

        dut.d.value = test_data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

        assert dut.q.value == test_data, \
            f"Random test {i} failed: d={test_data}, expected q={test_data}, got q={dut.q.value}"

    dut._log.info(f"✓ Random data test passed for {len(test_vectors)} test vectors")


@cocotb.test()
async def test_ff_reset_during_operation(dut):
    """Test reset assertion during normal operation"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset and start normal operation
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0

    # Set d=1 and wait for it to propagate
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, "Setup failed: q should be 1"

    # Assert reset while d=1
    dut.rst.value = 1
    await Timer(5, units="ns")  # Don't wait for clock edge
    assert dut.q.value == 0, f"Reset during operation failed: expected q=0, got q={dut.q.value}"

    # Release reset and verify normal operation resumes
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, f"Resume after reset failed: expected q=1, got q={dut.q.value}"

    dut._log.info("✓ Reset during operation test passed")


@cocotb.test()
async def test_ff_setup_hold_timing(dut):
    """Test setup and hold time requirements (basic timing test)"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    # Test data changes right before clock edge
    for test_value in [1, 0, 1, 0]:
        # Change data well before clock edge (good setup time)
        dut.d.value = test_value
        await Timer(8, units="ns")  # Wait 8ns before clock edge
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

        assert dut.q.value == test_value, \
            f"Timing test failed: d={test_value}, expected q={test_value}, got q={dut.q.value}"

    dut._log.info("✓ Basic timing test passed")


@cocotb.test()
async def test_ff_comprehensive(dut):
    """Comprehensive test combining all scenarios"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut._log.info("Starting comprehensive D flip-flop test")

    # Phase 1: Reset test
    dut._log.info("Phase 1: Testing reset functionality")
    dut.rst.value = 1
    dut.d.value = 1
    await Timer(15, units="ns")
    assert dut.q.value == 0, "Reset test failed"

    # Phase 2: Basic operation
    dut._log.info("Phase 2: Testing basic operation")
    dut.rst.value = 0
    test_sequence = [0, 1, 1, 0, 1, 0, 0, 1]

    for i, test_val in enumerate(test_sequence):
        dut.d.value = test_val
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.q.value == test_val, \
            f"Sequence test {i} failed: d={test_val}, q={dut.q.value}"

    # Phase 3: Reset during operation
    dut._log.info("Phase 3: Testing reset during operation")
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, "Pre-reset setup failed"

    dut.rst.value = 1
    await Timer(5, units="ns")
    assert dut.q.value == 0, "Reset during operation failed"

    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, "Recovery after reset failed"

    dut._log.info("✓ Comprehensive test completed successfully")


if __name__ == "__main__":
    import sys
    import os

    # Add cocotb to path if running standalone
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    print("D Flip-Flop cocotb testbench")
    print("Run with: make cocotb")
