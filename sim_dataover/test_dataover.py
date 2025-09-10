"""
Dataover cocotb testbench
Tests the dataover module using cocotb framework
Now supports signed 32-bit comparisons
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

    # Test case 1: Maximum positive signed value
    dut.data_in.value = 0x7FFFFFFF  # Maximum positive signed 32-bit
    dut.threshold.value = 0x7FFFFFFE
    await Timer(10, units="ns")

    expected = 1
    actual = int(dut.data_over.value)
    assert actual == expected, f"Max positive test failed: data_in=0x7FFFFFFF, threshold=0x7FFFFFFE, expected={expected}, got={actual}"
    dut._log.info("✓ Maximum positive value test passed")

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
        # Generate random signed 32-bit values
        data_in = random.randint(-2147483648, 2147483647)
        threshold = random.randint(-2147483648, 2147483647)

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
async def test_dataover_signed_values(dut):
    """Test with signed values including negative numbers"""

    dut._log.info("Starting signed values test")

    # Test case 1: Negative numbers
    dut.data_in.value = -50
    dut.threshold.value = -100
    await Timer(10, units="ns")

    expected = 1  # -50 > -100
    actual = int(dut.data_over.value)
    assert actual == expected, f"Negative test 1 failed: data_in=-50, threshold=-100, expected={expected}, got={actual}"
    dut._log.info("✓ Negative test 1 passed: -50 > -100 -> data_over=1")

    # Test case 2: Negative vs positive
    dut.data_in.value = -10
    dut.threshold.value = 10
    await Timer(10, units="ns")

    expected = 0  # -10 < 10
    actual = int(dut.data_over.value)
    assert actual == expected, f"Negative vs positive test failed: data_in=-10, threshold=10, expected={expected}, got={actual}"
    dut._log.info("✓ Negative vs positive test passed: -10 < 10 -> data_over=0")

    # Test case 3: Positive vs negative
    dut.data_in.value = 10
    dut.threshold.value = -10
    await Timer(10, units="ns")

    expected = 1  # 10 > -10
    actual = int(dut.data_over.value)
    assert actual == expected, f"Positive vs negative test failed: data_in=10, threshold=-10, expected={expected}, got={actual}"
    dut._log.info("✓ Positive vs negative test passed: 10 > -10 -> data_over=1")

    # Test case 4: Minimum signed value
    dut.data_in.value = 0x80000000  # Most negative signed 32-bit (-2147483648)
    dut.threshold.value = 0x80000001  # -2147483647
    await Timer(10, units="ns")

    expected = 0  # -2147483648 < -2147483647
    actual = int(dut.data_over.value)
    assert actual == expected, f"Minimum signed test failed: data_in=0x80000000, threshold=0x80000001, expected={expected}, got={actual}"
    dut._log.info("✓ Minimum signed value test passed")

    # Test case 5: Cross zero boundary
    dut.data_in.value = 1
    dut.threshold.value = -1
    await Timer(10, units="ns")

    expected = 1  # 1 > -1
    actual = int(dut.data_over.value)
    assert actual == expected, f"Cross zero test failed: data_in=1, threshold=-1, expected={expected}, got={actual}"
    dut._log.info("✓ Cross zero boundary test passed: 1 > -1 -> data_over=1")


@cocotb.test()
async def test_dataover_negative_comprehensive(dut):
    """Comprehensive test with various negative values"""

    dut._log.info("Starting comprehensive negative values test")

    # Test vectors: (data_in, threshold, expected_result, description)
    negative_test_vectors = [
        # Both negative, data_in > threshold
        (-10, -20, 1, "-10 > -20"),
        (-100, -200, 1, "-100 > -200"),
        (-1000, -2000, 1, "-1000 > -2000"),
        (-1, -2, 1, "-1 > -2"),

        # Both negative, data_in < threshold
        (-20, -10, 0, "-20 < -10"),
        (-200, -100, 0, "-200 < -100"),
        (-2000, -1000, 0, "-2000 < -1000"),
        (-2, -1, 0, "-2 < -1"),

        # Both negative, equal
        (-50, -50, 0, "-50 = -50"),
        (-1000, -1000, 0, "-1000 = -1000"),

        # Negative vs positive
        (-1, 1, 0, "-1 < 1"),
        (-100, 100, 0, "-100 < 100"),
        (-1000, 1000, 0, "-1000 < 1000"),

        # Positive vs negative
        (1, -1, 1, "1 > -1"),
        (100, -100, 1, "100 > -100"),
        (1000, -1000, 1, "1000 > -1000"),

        # Negative vs zero
        (-1, 0, 0, "-1 < 0"),
        (-100, 0, 0, "-100 < 0"),
        (-1000, 0, 0, "-1000 < 0"),

        # Zero vs negative
        (0, -1, 1, "0 > -1"),
        (0, -100, 1, "0 > -100"),
        (0, -1000, 1, "0 > -1000"),

        # Large negative values
        (-2147483647, -2147483648, 1, "-2147483647 > -2147483648"),
        (-2147483648, -2147483647, 0, "-2147483648 < -2147483647"),
        (-1000000000, -2000000000, 1, "-1000000000 > -2000000000"),

        # Mixed large values
        (2147483647, -2147483648, 1, "2147483647 > -2147483648"),
        (-2147483648, 2147483647, 0, "-2147483648 < 2147483647"),
    ]

    for i, (data_in, threshold, expected, description) in enumerate(negative_test_vectors):
        dut.data_in.value = data_in
        dut.threshold.value = threshold
        await Timer(10, units="ns")

        actual = int(dut.data_over.value)
        assert actual == expected, \
            f"Negative test {i} failed: {description}, expected={expected}, got={actual}"

        dut._log.info(f"✓ Test {i}: {description} -> data_over={actual}")

    dut._log.info("✓ Comprehensive negative values test completed successfully")


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
    from cocotb.runner import get_runner
    import os
    from pathlib import Path



    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "questa")

    proj_path = Path(__file__).resolve().parent



    verilog_sources = []
    vhdl_sources = []

    if hdl_toplevel_lang == "verilog":
        verilog_sources = [proj_path / "../dataover.v"]
    else:
        vhdl_sources = [proj_path / "dff.vhdl"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="dataover",
        always=True,
    )

    runner.test(
        hdl_toplevel="dataover", 
        test_module="test_dataover,",
        waves=True,
        gui=True,
    )
