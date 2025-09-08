"""
Two Dataover cocotb testbench
Tests the two_dataover module using cocotb framework
Now supports signed 32-bit comparisons with thresholds 100 and 200
"""

import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random


@cocotb.test()
async def test_two_dataover_basic(dut):
    """Test basic two_dataover functionality"""

    dut._log.info("Starting basic two_dataover test")

    # Test case 1: data_in < 100 (both outputs should be 0)
    dut.data_in.value = 50
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Test 1a failed: data_in=50, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Test 1b failed: data_in=50, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Test 1 passed: 50 < 100 and 50 < 200 -> both outputs = 0")

    # Test case 2: data_in = 100 (both outputs should be 0)
    dut.data_in.value = 100
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Test 2a failed: data_in=100, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Test 2b failed: data_in=100, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Test 2 passed: 100 = 100 and 100 < 200 -> both outputs = 0")

    # Test case 3: 100 < data_in < 200 (data_over_100=1, data_over_200=0)
    dut.data_in.value = 150
    await Timer(10, units="ns")

    expected_100 = 1
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Test 3a failed: data_in=150, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Test 3b failed: data_in=150, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Test 3 passed: 150 > 100 and 150 < 200 -> data_over_100=1, data_over_200=0")

    # Test case 4: data_in = 200 (data_over_100=1, data_over_200=0)
    dut.data_in.value = 200
    await Timer(10, units="ns")

    expected_100 = 1
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Test 4a failed: data_in=200, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Test 4b failed: data_in=200, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Test 4 passed: 200 > 100 and 200 = 200 -> data_over_100=1, data_over_200=0")

    # Test case 5: data_in > 200 (both outputs should be 1)
    dut.data_in.value = 300
    await Timer(10, units="ns")

    expected_100 = 1
    expected_200 = 1
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Test 5a failed: data_in=300, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Test 5b failed: data_in=300, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Test 5 passed: 300 > 100 and 300 > 200 -> both outputs = 1")


@cocotb.test()
async def test_two_dataover_boundary_conditions(dut):
    """Test boundary conditions around thresholds 100 and 200"""

    dut._log.info("Starting boundary conditions test")

    # Test values around 100 threshold
    boundary_tests_100 = [
        (99, 0, 0),   # Just below 100
        (100, 0, 0),  # Equal to 100
        (101, 1, 0),  # Just above 100
    ]

    for data_in, expected_100, expected_200 in boundary_tests_100:
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, \
            f"Boundary 100 test failed: data_in={data_in}, expected data_over_100={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, \
            f"Boundary 100 test failed: data_in={data_in}, expected data_over_200={expected_200}, got={actual_200}"

        dut._log.info(f"✓ Boundary test: {data_in} -> data_over_100={actual_100}, data_over_200={actual_200}")

    # Test values around 200 threshold
    boundary_tests_200 = [
        (199, 1, 0),  # Just below 200
        (200, 1, 0),  # Equal to 200
        (201, 1, 1),  # Just above 200
    ]

    for data_in, expected_100, expected_200 in boundary_tests_200:
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, \
            f"Boundary 200 test failed: data_in={data_in}, expected data_over_100={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, \
            f"Boundary 200 test failed: data_in={data_in}, expected data_over_200={expected_200}, got={actual_200}"

        dut._log.info(f"✓ Boundary test: {data_in} -> data_over_100={actual_100}, data_over_200={actual_200}")


@cocotb.test()
async def test_two_dataover_edge_cases(dut):
    """Test edge cases with extreme values"""

    dut._log.info("Starting edge cases test")

    # Test case 1: Zero input
    dut.data_in.value = 0
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Zero test failed: expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Zero test failed: expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Zero test passed")

    # Test case 2: Maximum signed 32-bit value
    dut.data_in.value = 0x7FFFFFFF  # 2147483647
    await Timer(10, units="ns")

    expected_100 = 1
    expected_200 = 1
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Max signed value test failed: expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Max signed value test failed: expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Maximum signed value test passed")

    # Test case 3: Large values
    large_values = [1000, 10000, 100000, 1000000]

    for value in large_values:
        dut.data_in.value = value
        await Timer(10, units="ns")

        expected_100 = 1
        expected_200 = 1
        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, f"Large value test failed: data_in={value}, expected data_over_100={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, f"Large value test failed: data_in={value}, expected data_over_200={expected_200}, got={actual_200}"

        dut._log.info(f"✓ Large value test passed: {value} -> both outputs = 1")


@cocotb.test()
async def test_two_dataover_random(dut):
    """Test with random values"""

    dut._log.info("Starting random test")

    test_count = 30
    passed_tests = 0

    for i in range(test_count):
        # Generate random signed 32-bit value
        data_in = random.randint(-2147483648, 2147483647)

        dut.data_in.value = data_in
        await Timer(10, units="ns")

        expected_100 = 1 if data_in > 100 else 0
        expected_200 = 1 if data_in > 200 else 0
        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, \
            f"Random test {i} failed: data_in={data_in}, expected data_over_100={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, \
            f"Random test {i} failed: data_in={data_in}, expected data_over_200={expected_200}, got={actual_200}"

        passed_tests += 1

    dut._log.info(f"✓ Random test passed: {passed_tests}/{test_count} tests")


@cocotb.test()
async def test_two_dataover_signed_values(dut):
    """Test with signed values including negative numbers"""

    dut._log.info("Starting signed values test")

    # Test case 1: Negative input (both outputs should be 0)
    dut.data_in.value = -50
    await Timer(10, units="ns")

    expected_100 = 0  # -50 < 100
    expected_200 = 0  # -50 < 200
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Negative test failed: data_in=-50, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Negative test failed: data_in=-50, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Negative input test passed: -50 < 100 and -50 < 200 -> both outputs = 0")

    # Test case 2: Very negative input
    dut.data_in.value = -1000
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Very negative test failed: data_in=-1000, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Very negative test failed: data_in=-1000, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Very negative input test passed: -1000 < 100 and -1000 < 200 -> both outputs = 0")

    # Test case 3: Minimum signed 32-bit value
    dut.data_in.value = 0x80000000  # -2147483648
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Minimum signed test failed: data_in=-2147483648, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Minimum signed test failed: data_in=-2147483648, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Minimum signed value test passed: -2147483648 < 100 and -2147483648 < 200 -> both outputs = 0")

    # Test case 4: Maximum signed 32-bit value
    dut.data_in.value = 0x7FFFFFFF  # 2147483647
    await Timer(10, units="ns")

    expected_100 = 1
    expected_200 = 1
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Maximum signed test failed: data_in=2147483647, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Maximum signed test failed: data_in=2147483647, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Maximum signed value test passed: 2147483647 > 100 and 2147483647 > 200 -> both outputs = 1")

    # Test case 5: Zero crossing
    dut.data_in.value = 0
    await Timer(10, units="ns")

    expected_100 = 0
    expected_200 = 0
    actual_100 = int(dut.data_over_100.value)
    actual_200 = int(dut.data_over_200.value)

    assert actual_100 == expected_100, f"Zero test failed: data_in=0, expected data_over_100={expected_100}, got={actual_100}"
    assert actual_200 == expected_200, f"Zero test failed: data_in=0, expected data_over_200={expected_200}, got={actual_200}"
    dut._log.info("✓ Zero crossing test passed: 0 < 100 and 0 < 200 -> both outputs = 0")


@cocotb.test()
async def test_two_dataover_negative_comprehensive(dut):
    """Comprehensive test with various negative input values"""

    dut._log.info("Starting comprehensive negative input test")

    # Test vectors: (data_in, expected_data_over_100, expected_data_over_200, description)
    negative_test_vectors = [
        # Small negative values
        (-1, 0, 0, "-1 < 100 and -1 < 200"),
        (-5, 0, 0, "-5 < 100 and -5 < 200"),
        (-10, 0, 0, "-10 < 100 and -10 < 200"),
        (-50, 0, 0, "-50 < 100 and -50 < 200"),
        (-99, 0, 0, "-99 < 100 and -99 < 200"),

        # Medium negative values
        (-100, 0, 0, "-100 < 100 and -100 < 200"),
        (-150, 0, 0, "-150 < 100 and -150 < 200"),
        (-200, 0, 0, "-200 < 100 and -200 < 200"),
        (-250, 0, 0, "-250 < 100 and -250 < 200"),
        (-500, 0, 0, "-500 < 100 and -500 < 200"),

        # Large negative values
        (-1000, 0, 0, "-1000 < 100 and -1000 < 200"),
        (-10000, 0, 0, "-10000 < 100 and -10000 < 200"),
        (-100000, 0, 0, "-100000 < 100 and -100000 < 200"),
        (-1000000, 0, 0, "-1000000 < 100 and -1000000 < 200"),

        # Very large negative values
        (-10000000, 0, 0, "-10000000 < 100 and -10000000 < 200"),
        (-100000000, 0, 0, "-100000000 < 100 and -100000000 < 200"),
        (-1000000000, 0, 0, "-1000000000 < 100 and -1000000000 < 200"),
        (-2000000000, 0, 0, "-2000000000 < 100 and -2000000000 < 200"),

        # Boundary negative values
        (-2147483647, 0, 0, "-2147483647 < 100 and -2147483647 < 200"),
        (-2147483648, 0, 0, "-2147483648 < 100 and -2147483648 < 200"),  # Most negative 32-bit

        # Hex representation negative values (to verify proper signed interpretation)
        (0x80000000, 0, 0, "0x80000000 (-2147483648) < 100 and < 200"),
        (0x80000001, 0, 0, "0x80000001 (-2147483647) < 100 and < 200"),
        (0xFFFFFFFF, 0, 0, "0xFFFFFFFF (-1) < 100 and < 200"),
        (0xFFFFFFFE, 0, 0, "0xFFFFFFFE (-2) < 100 and < 200"),
        (0xFFFFFF9C, 0, 0, "0xFFFFFF9C (-100) < 100 and < 200"),
        (0xFFFFFF38, 0, 0, "0xFFFFFF38 (-200) < 100 and < 200"),
    ]

    for i, (data_in, expected_100, expected_200, description) in enumerate(negative_test_vectors):
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, \
            f"Negative test {i} failed for data_over_100: {description}, expected={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, \
            f"Negative test {i} failed for data_over_200: {description}, expected={expected_200}, got={actual_200}"

        dut._log.info(f"✓ Test {i}: {description} -> outputs=({actual_100},{actual_200})")

    dut._log.info("✓ Comprehensive negative input test completed successfully")


@cocotb.test()
async def test_two_dataover_comprehensive(dut):
    """Comprehensive test combining all scenarios"""

    dut._log.info("Starting comprehensive two_dataover test")

    # Define comprehensive test vectors
    # (data_in, expected_data_over_100, expected_data_over_200)
    test_vectors = [
        # Negative values
        (-2147483648, 0, 0), # Minimum signed 32-bit
        (-1000, 0, 0),       # Large negative
        (-50, 0, 0),         # Negative value
        (-1, 0, 0),          # Just below zero
        # Zero and positive values
        (0, 0, 0),           # Zero
        (1, 0, 0),           # Small value
        (50, 0, 0),          # Below 100
        (99, 0, 0),          # Just below 100
        (100, 0, 0),         # Equal to 100
        (101, 1, 0),         # Just above 100
        (150, 1, 0),         # Between 100 and 200
        (199, 1, 0),         # Just below 200
        (200, 1, 0),         # Equal to 200
        (201, 1, 1),         # Just above 200
        (300, 1, 1),         # Above both thresholds
        (1000, 1, 1),        # Large value
        (2147483647, 1, 1),  # Maximum signed 32-bit
    ]

    for i, (data_in, expected_100, expected_200) in enumerate(test_vectors):
        dut.data_in.value = data_in
        await Timer(10, units="ns")

        actual_100 = int(dut.data_over_100.value)
        actual_200 = int(dut.data_over_200.value)

        assert actual_100 == expected_100, \
            f"Comprehensive test {i} failed: data_in={data_in}, expected data_over_100={expected_100}, got={actual_100}"
        assert actual_200 == expected_200, \
            f"Comprehensive test {i} failed: data_in={data_in}, expected data_over_200={expected_200}, got={actual_200}"

        dut._log.info(f"✓ Vector {i}: {data_in} -> data_over_100={actual_100}, data_over_200={actual_200}")

    dut._log.info("✓ Comprehensive test completed successfully")


if __name__ == "__main__":
    import sys
    import os

    # Add cocotb to path if running standalone
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    print("Two Dataover cocotb testbench")
    print("Run with: make")
