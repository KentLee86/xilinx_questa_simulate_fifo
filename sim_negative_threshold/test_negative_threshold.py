"""
Negative Threshold Dataover cocotb testbench
Tests the negative_threshold_dataover module using cocotb framework
Tests signed 32-bit comparisons with negative thresholds -100 and -50
"""

import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random


@cocotb.test()
async def test_negative_threshold_basic(dut):
    """Test basic negative threshold functionality"""

    dut._log.info("Starting basic negative threshold test")

    # Test case 1: Very negative input (both outputs should be 0)
    dut.data_in.value = -200
    await Timer(10, units="ns")

    expected_neg100 = 0  # -200 < -100
    expected_neg50 = 0   # -200 < -50
    actual_neg100 = int(dut.data_over_neg100.value)
    actual_neg50 = int(dut.data_over_neg50.value)

    assert actual_neg100 == expected_neg100, f"Test 1a failed: data_in=-200, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
    assert actual_neg50 == expected_neg50, f"Test 1b failed: data_in=-200, expected data_over_neg50={expected_neg50}, got={actual_neg50}"
    dut._log.info("✓ Test 1 passed: -200 < -100 and -200 < -50 -> both outputs = 0")

    # Test case 2: Between thresholds (-100 < data_in < -50)
    dut.data_in.value = -75
    await Timer(10, units="ns")

    expected_neg100 = 1  # -75 > -100
    expected_neg50 = 0   # -75 < -50
    actual_neg100 = int(dut.data_over_neg100.value)
    actual_neg50 = int(dut.data_over_neg50.value)

    assert actual_neg100 == expected_neg100, f"Test 2a failed: data_in=-75, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
    assert actual_neg50 == expected_neg50, f"Test 2b failed: data_in=-75, expected data_over_neg50={expected_neg50}, got={actual_neg50}"
    dut._log.info("✓ Test 2 passed: -75 > -100 and -75 < -50 -> data_over_neg100=1, data_over_neg50=0")

    # Test case 3: Above both thresholds (negative but > -50)
    dut.data_in.value = -25
    await Timer(10, units="ns")

    expected_neg100 = 1  # -25 > -100
    expected_neg50 = 1   # -25 > -50
    actual_neg100 = int(dut.data_over_neg100.value)
    actual_neg50 = int(dut.data_over_neg50.value)

    assert actual_neg100 == expected_neg100, f"Test 3a failed: data_in=-25, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
    assert actual_neg50 == expected_neg50, f"Test 3b failed: data_in=-25, expected data_over_neg50={expected_neg50}, got={actual_neg50}"
    dut._log.info("✓ Test 3 passed: -25 > -100 and -25 > -50 -> both outputs = 1")

    # Test case 4: Positive input (both outputs should be 1)
    dut.data_in.value = 50
    await Timer(10, units="ns")

    expected_neg100 = 1  # 50 > -100
    expected_neg50 = 1   # 50 > -50
    actual_neg100 = int(dut.data_over_neg100.value)
    actual_neg50 = int(dut.data_over_neg50.value)

    assert actual_neg100 == expected_neg100, f"Test 4a failed: data_in=50, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
    assert actual_neg50 == expected_neg50, f"Test 4b failed: data_in=50, expected data_over_neg50={expected_neg50}, got={actual_neg50}"
    dut._log.info("✓ Test 4 passed: 50 > -100 and 50 > -50 -> both outputs = 1")


@cocotb.test()
async def test_negative_threshold_boundary(dut):
    """Test boundary conditions around negative thresholds"""

    dut._log.info("Starting boundary conditions test")

    # Test values around -100 threshold
    boundary_tests_neg100 = [
        (-101, 0, 0),  # Just below -100
        (-100, 0, 0),  # Equal to -100
        (-99, 1, 0),   # Just above -100
    ]

    for data_in, expected_neg100, expected_neg50 in boundary_tests_neg100:
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_neg100 = int(dut.data_over_neg100.value)
        actual_neg50 = int(dut.data_over_neg50.value)

        assert actual_neg100 == expected_neg100, \
            f"Boundary -100 test failed: data_in={data_in}, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
        assert actual_neg50 == expected_neg50, \
            f"Boundary -100 test failed: data_in={data_in}, expected data_over_neg50={expected_neg50}, got={actual_neg50}"

        dut._log.info(f"✓ Boundary test: {data_in} -> data_over_neg100={actual_neg100}, data_over_neg50={actual_neg50}")

    # Test values around -50 threshold
    boundary_tests_neg50 = [
        (-51, 1, 0),   # Just below -50
        (-50, 1, 0),   # Equal to -50
        (-49, 1, 1),   # Just above -50
    ]

    for data_in, expected_neg100, expected_neg50 in boundary_tests_neg50:
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_neg100 = int(dut.data_over_neg100.value)
        actual_neg50 = int(dut.data_over_neg50.value)

        assert actual_neg100 == expected_neg100, \
            f"Boundary -50 test failed: data_in={data_in}, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
        assert actual_neg50 == expected_neg50, \
            f"Boundary -50 test failed: data_in={data_in}, expected data_over_neg50={expected_neg50}, got={actual_neg50}"

        dut._log.info(f"✓ Boundary test: {data_in} -> data_over_neg100={actual_neg100}, data_over_neg50={actual_neg50}")


@cocotb.test()
async def test_negative_threshold_comprehensive(dut):
    """Comprehensive test with various input values against negative thresholds"""

    dut._log.info("Starting comprehensive negative threshold test")

    # Test vectors: (data_in, expected_data_over_neg100, expected_data_over_neg50, description)
    test_vectors = [
        # Very negative values
        (-2147483648, 0, 0, "Most negative 32-bit value"),
        (-2147483647, 0, 0, "Second most negative 32-bit value"),
        (-1000000000, 0, 0, "Large negative value"),
        (-1000000, 0, 0, "Medium negative value"),
        (-1000, 0, 0, "Small negative value"),
        (-500, 0, 0, "Below both thresholds"),
        (-200, 0, 0, "Below both thresholds"),
        (-150, 0, 0, "Below both thresholds"),

        # Around -100 threshold
        (-101, 0, 0, "Just below -100"),
        (-100, 0, 0, "Equal to -100"),
        (-99, 1, 0, "Just above -100"),
        (-90, 1, 0, "Above -100, below -50"),
        (-80, 1, 0, "Above -100, below -50"),
        (-70, 1, 0, "Above -100, below -50"),
        (-60, 1, 0, "Above -100, below -50"),

        # Around -50 threshold
        (-51, 1, 0, "Just below -50"),
        (-50, 1, 0, "Equal to -50"),
        (-49, 1, 1, "Just above -50"),
        (-40, 1, 1, "Above both thresholds"),
        (-30, 1, 1, "Above both thresholds"),
        (-20, 1, 1, "Above both thresholds"),
        (-10, 1, 1, "Above both thresholds"),
        (-5, 1, 1, "Above both thresholds"),
        (-1, 1, 1, "Above both thresholds"),

        # Zero and positive values
        (0, 1, 1, "Zero - above both thresholds"),
        (1, 1, 1, "Small positive"),
        (10, 1, 1, "Medium positive"),
        (100, 1, 1, "Large positive"),
        (1000, 1, 1, "Very large positive"),
        (2147483647, 1, 1, "Most positive 32-bit value"),

        # Hex representations to verify signed interpretation
        (0x80000000, 0, 0, "0x80000000 (-2147483648)"),
        (0x80000001, 0, 0, "0x80000001 (-2147483647)"),
        (0xFFFFFF9C, 0, 0, "0xFFFFFF9C (-100)"),
        (0xFFFFFFCE, 1, 0, "0xFFFFFFCE (-50)"),
        (0xFFFFFFFF, 1, 1, "0xFFFFFFFF (-1)"),
    ]

    for i, (data_in, expected_neg100, expected_neg50, description) in enumerate(test_vectors):
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_neg100 = int(dut.data_over_neg100.value)
        actual_neg50 = int(dut.data_over_neg50.value)

        assert actual_neg100 == expected_neg100, \
            f"Comprehensive test {i} failed for data_over_neg100: {description}, expected={expected_neg100}, got={actual_neg100}"
        assert actual_neg50 == expected_neg50, \
            f"Comprehensive test {i} failed for data_over_neg50: {description}, expected={expected_neg50}, got={actual_neg50}"

        dut._log.info(f"✓ Vector {i}: {description} -> outputs=({actual_neg100},{actual_neg50})")

    dut._log.info("✓ Comprehensive negative threshold test completed successfully")


@cocotb.test()
async def test_negative_threshold_random(dut):
    """Test with random signed values"""

    dut._log.info("Starting random test with negative thresholds")

    test_count = 50
    passed_tests = 0

    for i in range(test_count):
        # Generate random signed 32-bit value
        data_in = random.randint(-2147483648, 2147483647)

        dut.data_in.value = data_in
        await Timer(10, units="ns")

        expected_neg100 = 1 if data_in > -100 else 0
        expected_neg50 = 1 if data_in > -50 else 0
        actual_neg100 = int(dut.data_over_neg100.value)
        actual_neg50 = int(dut.data_over_neg50.value)

        assert actual_neg100 == expected_neg100, \
            f"Random test {i} failed: data_in={data_in}, expected data_over_neg100={expected_neg100}, got={actual_neg100}"
        assert actual_neg50 == expected_neg50, \
            f"Random test {i} failed: data_in={data_in}, expected data_over_neg50={expected_neg50}, got={actual_neg50}"

        passed_tests += 1

    dut._log.info(f"✓ Random test with negative thresholds passed: {passed_tests}/{test_count} tests")


if __name__ == "__main__":
    import sys
    import os

    # Add cocotb to path if running standalone
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    print("Negative Threshold Dataover cocotb testbench")
    print("Run with: make")
