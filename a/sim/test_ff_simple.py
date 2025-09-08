"""
D Flip-Flop cocotb testbench (Simplified version)
Tests the ff module using cocotb framework
"""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ClockCycles
import random


@cocotb.test()
async def test_ff_basic(dut):
    """Test basic D flip-flop functionality"""

    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")  # 100MHz clock
    cocotb.start_soon(clock.start())

    # Initialize signals
    dut.d.value = 0
    dut.rst.value = 1

    # Wait a few clock cycles
    await ClockCycles(dut.clk, 2)

    # Check reset functionality
    assert dut.q.value == 0, f"Reset failed: expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Reset test passed")

    # Release reset
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    # Test basic operation: d=1 -> q=1
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")  # Small delay for signal propagation
    assert dut.q.value == 1, f"Test failed: d=1, expected q=1, got q={dut.q.value}"
    dut._log.info("✓ Basic operation test (d=1->q=1) passed")

    # Test basic operation: d=0 -> q=0
    dut.d.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 0, f"Test failed: d=0, expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Basic operation test (d=0->q=0) passed")

    # Test a few random values
    for i in range(5):
        test_val = random.randint(0, 1)
        dut.d.value = test_val
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        assert dut.q.value == test_val, \
            f"Random test {i} failed: d={test_val}, expected q={test_val}, got q={dut.q.value}"

    dut._log.info("✓ Random data test passed")

    # Test reset during operation
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, "Setup failed before reset test"

    # Assert reset
    dut.rst.value = 1
    await Timer(5, units="ns")  # Don't wait for clock
    assert dut.q.value == 0, f"Reset during operation failed: expected q=0, got q={dut.q.value}"
    dut._log.info("✓ Reset during operation test passed")

    # Release reset and verify recovery
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")
    assert dut.q.value == 1, f"Recovery failed: expected q=1, got q={dut.q.value}"
    dut._log.info("✓ Recovery after reset test passed")

    dut._log.info("🎉 All tests passed successfully!")


if __name__ == "__main__":
    print("D Flip-Flop cocotb testbench (Simplified)")
    print("Run with: make MODULE=test_ff_simple")
