"""
Dataover cocotb testbench
Tests the dataover module using cocotb framework
"""

import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random


@cocotb.test()
async def test_dataover_basic(dut):
    """Test basic dataover functionality"""

    dut._log.info("Starting basic dataover test")

    # Test case 1: data_in < threshold (should output 0)
    dut.data_in.value = 100
    dut.threshold.value = 200
    await Timer(10, units="ns")

    expected = 0
    actual = int(dut.data_over.value)
    assert actual == expected, f"Test 1 failed: data_in=100, threshold=200, expected={expected}, got={actual}"
    dut._log.info("✓ Test 1 passed: 100 < 200 -> data_over=0")

    # Test case 2: data_in = threshold (should output 0)
    dut.data_in.value = 200
    dut.threshold.value = 200
    await Timer(10, units="ns")

    expected = 0
    actual = int(dut.data_over.value)
    assert actual == expected, f"Test 2 failed: data_in=200, threshold=200, expected={expected}, got={actual}"
    dut._log.info("✓ Test 2 passed: 200 = 200 -> data_over=0")

    # Test case 3: data_in > threshold (should output 1)
    dut.data_in.value = 300
    dut.threshold.value = 200
    await Timer(10, units="ns")

    expected = 1
    actual = int(dut.data_over.value)
    assert actual == expected, f"Test 3 failed: data_in=300, threshold=200, expected={expected}, got={actual}"
    dut._log.info("✓ Test 3 passed: 300 > 200 -> data_over=1")


@cocotb.test()
async def test_dataover_edge_cases(dut):
    """Test edge cases with extreme values"""

    dut._log.info("Starting edge cases test")

    # Test case 1: Maximum 32-bit values
    dut.data_in.value = 0xFFFFFFFF  # Maximum 32-bit unsigned
    dut.threshold.value = 0xFFFFFFFE
    await Timer(10, units="ns")

    expected = 1
    actual = int(dut.data_over.value)
    assert actual == expected, f"Max value test failed: data_in=0xFFFFFFFF, threshold=0xFFFFFFFE, expected={expected}, got={actual}"
    dut._log.info("✓ Maximum value test passed")

    # Test case 2: Zero values
    dut.data_in.value = 0
    dut.threshold.value = 0
    await Timer(10, units="ns")

    expected = 0
    actual = int(dut.data_over.value)
    assert actual == expected, f"Zero test failed: data_in=0, threshold=0, expected={expected}, got={actual}"
    dut._log.info("✓ Zero values test passed")

    # Test case 3: One greater than zero
    dut.data_in.value = 1
    dut.threshold.value = 0
    await Timer(10, units="ns")

    expected = 1
    actual = int(dut.data_over.value)
    assert actual == expected, f"One > zero test failed: data_in=1, threshold=0, expected={expected}, got={actual}"
    dut._log.info("✓ One > zero test passed")

    # Test case 4: Large numbers close to each other
    dut.data_in.value = 1000000
    dut.threshold.value = 999999
    await Timer(10, units="ns")

    expected = 1
    actual = int(dut.data_over.value)
    assert actual == expected, f"Large number test failed: data_in=1000000, threshold=999999, expected={expected}, got={actual}"
    dut._log.info("✓ Large number test passed")


@cocotb.test()
async def test_dataover_random(dut):
    """Test with random values"""

    dut._log.info("Starting random test")

    test_count = 50
    passed_tests = 0

    for i in range(test_count):
        # Generate random 32-bit values
        data_in = random.randint(0, 0xFFFFFFFF)
        threshold = random.randint(0, 0xFFFFFFFF)

        dut.data_in.value = data_in
        dut.threshold.value = threshold
        await Timer(10, units="ns")

        expected = 1 if data_in > threshold else 0
        actual = int(dut.data_over.value)

        assert actual == expected, \
            f"Random test {i} failed: data_in={data_in}, threshold={threshold}, expected={expected}, got={actual}"

        passed_tests += 1

    dut._log.info(f"✓ Random test passed: {passed_tests}/{test_count} tests")


@cocotb.test()
async def test_dataover_boundary_conditions(dut):
    """Test boundary conditions around specific thresholds"""

    dut._log.info("Starting boundary conditions test")

    # Test around common threshold values
    thresholds = [100, 1000, 10000, 100000, 1000000]

    for threshold in thresholds:
        # Test threshold - 1, threshold, threshold + 1
        test_values = [threshold - 1, threshold, threshold + 1]

        for data_in in test_values:
            if data_in >= 0:  # Ensure non-negative values
                dut.data_in.value = data_in
                dut.threshold.value = threshold
                await Timer(10, units="ns")

                expected = 1 if data_in > threshold else 0
                actual = int(dut.data_over.value)

                assert actual == expected, \
                    f"Boundary test failed: data_in={data_in}, threshold={threshold}, expected={expected}, got={actual}"

                dut._log.info(f"✓ Boundary test passed: {data_in} vs {threshold} -> {actual}")


@cocotb.test()
async def test_dataover_comprehensive(dut):
    """Comprehensive test combining all scenarios"""

    dut._log.info("Starting comprehensive dataover test")

    # Define comprehensive test vectors
    test_vectors = [
        # (data_in, threshold, expected_output)
        (0, 0, 0),           # Equal at zero
        (1, 0, 1),           # Just above zero
        (0, 1, 0),           # Just below one
        (100, 100, 0),       # Equal values
        (101, 100, 1),       # Just above threshold
        (99, 100, 0),        # Just below threshold
        (0xFFFFFFFF, 0xFFFFFFFE, 1),  # Maximum values
        (0xFFFFFFFE, 0xFFFFFFFF, 0),  # Maximum values reversed
        (1000000, 999999, 1), # Large numbers
        (999999, 1000000, 0), # Large numbers reversed
        (2147483647, 2147483646, 1),  # Near 2^31
        (2147483646, 2147483647, 0),  # Near 2^31 reversed
    ]

    for i, (data_in, threshold, expected) in enumerate(test_vectors):
        dut.data_in.value = data_in
        dut.threshold.value = threshold
        await Timer(10, units="ns")

        actual = int(dut.data_over.value)
        assert actual == expected, \
            f"Comprehensive test {i} failed: data_in={data_in}, threshold={threshold}, expected={expected}, got={actual}"

        dut._log.info(f"✓ Vector {i}: {data_in} vs {threshold} -> {actual}")

    dut._log.info("✓ Comprehensive test completed successfully")


if __name__ == "__main__":
    import sys
    import os

    # Add cocotb to path if running standalone
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    print("Dataover cocotb testbench")
    print("Run with: make cocotb")
