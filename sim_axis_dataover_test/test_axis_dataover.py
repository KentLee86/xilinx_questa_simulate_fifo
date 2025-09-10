#!/usr/bin/env python3
"""
Axis Dataover cocotb testbench
Tests the axis_master_file_v2 + dataover integration
Verifies that numbers > 1,000,000 are correctly detected
"""

import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.result import TestFailure
import csv
import os

# Test configuration
THRESHOLD = 1000000

class AxisDataoverTester:
    """Helper class for testing axis_dataover functionality"""

    def __init__(self, dut):
        self.dut = dut
        self.test_data = []
        self.expected_results = []

    def load_test_data(self, filename="test_data.csv"):
        """Load test data from CSV file"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Test data file {filename} not found")

        self.test_data = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Skip empty rows
                    value = int(row[0])
                    self.test_data.append(value)

        # Calculate expected results
        self.expected_results = [1 if x > THRESHOLD else 0 for x in self.test_data]

        self.dut._log.info(f"Loaded {len(self.test_data)} test values from {filename}")
        self.dut._log.info(f"Values > {THRESHOLD}: {sum(self.expected_results)}")
        self.dut._log.info(f"Values <= {THRESHOLD}: {len(self.expected_results) - sum(self.expected_results)}")

    async def reset_dut(self):
        """Reset the DUT"""
        self.dut.aclk.value = 0
        self.dut.aresetn.value = 0

        # Set default control inputs
        self.dut.i_start.value = 0
        self.dut.i_loop.value = 0
        self.dut.i_restart.value = 0
        self.dut.i_pause.value = 0
        self.dut.i_gap_cycles.value = 0
        self.dut.i_reload.value = 0

        # Wait a few cycles
        for _ in range(10):
            await RisingEdge(self.dut.aclk)

        # Release reset
        self.dut.aresetn.value = 1
        await RisingEdge(self.dut.aclk)

    async def start_data_transmission(self):
        """Start data transmission from axis_master_file_v2"""
        self.dut.i_start.value = 1
        await RisingEdge(self.dut.aclk)
        self.dut.i_start.value = 0

    def clock_gen(self):
        """Clock generator"""
        return cocotb.start_soon(self._clock_gen())

    async def _clock_gen(self):
        """Internal clock generator"""
        while True:
            self.dut.aclk.value = 0
            await Timer(5, units="ns")
            self.dut.aclk.value = 1
            await Timer(5, units="ns")


@cocotb.test()
async def test_axis_dataover_basic(dut):
    """Basic test for axis_dataover functionality"""

    dut._log.info("Starting axis_dataover basic test")

    # Initialize tester
    tester = AxisDataoverTester(dut)
    tester.load_test_data()

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Start data transmission
    await tester.start_data_transmission()

    # Monitor data transmission and verify results
    received_count = 0
    correct_count = 0

    # Wait for transmission to start
    while not dut.o_busy.value:
        await RisingEdge(dut.aclk)

    dut._log.info("Data transmission started")

    # Monitor each data transmission
    for i, (expected_data, expected_over) in enumerate(zip(tester.test_data, tester.expected_results)):
        # Wait for valid data
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        # Get actual values
        actual_data = int(dut.m_axis_tdata.value)
        actual_over = int(dut.data_over.value)

        # Verify data integrity
        if actual_data != expected_data:
            raise TestFailure(f"Data mismatch at index {i}: expected {expected_data}, got {actual_data}")

        # Verify data_over output
        if actual_over != expected_over:
            raise TestFailure(f"Data_over mismatch at index {i}: data={actual_data}, expected_over={expected_over}, got {actual_over}")

        received_count += 1
        correct_count += 1

        dut._log.info(f"✓ Index {i}: data={actual_data}, data_over={actual_over} (expected {expected_over})")

        # Wait for next data or end of transmission
        await RisingEdge(dut.aclk)

        # Check if this is the last data
        if dut.m_axis_tlast.value:
            break

    # Wait for transmission to complete
    while dut.o_busy.value:
        await RisingEdge(dut.aclk)

    dut._log.info(f"Test completed: {correct_count}/{len(tester.test_data)} values verified correctly")


@cocotb.test()
async def test_axis_dataover_threshold_boundary(dut):
    """Test boundary conditions around the 1,000,000 threshold"""

    dut._log.info("Starting threshold boundary test")

    # Initialize tester
    tester = AxisDataoverTester(dut)

    # Create specific boundary test data
    boundary_data = [
        999999,    # Just below threshold
        1000000,   # Exactly threshold
        1000001,   # Just above threshold
        999998,    # Two below
        1000002,   # Two above
    ]

    tester.test_data = boundary_data
    tester.expected_results = [1 if x > THRESHOLD else 0 for x in boundary_data]

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Start data transmission
    await tester.start_data_transmission()

    # Monitor and verify
    correct_count = 0

    for i, (expected_data, expected_over) in enumerate(zip(tester.test_data, tester.expected_results)):
        # Wait for valid data
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        actual_data = int(dut.m_axis_tdata.value)
        actual_over = int(dut.data_over.value)

        # Verify
        assert actual_data == expected_data, f"Data mismatch: expected {expected_data}, got {actual_data}"
        assert actual_over == expected_over, f"Boundary test failed: data={actual_data}, expected {expected_over}, got {actual_over}"

        correct_count += 1
        dut._log.info(f"✓ Boundary test {i}: {actual_data} -> data_over={actual_over}")

        await RisingEdge(dut.aclk)

    dut._log.info(f"Boundary test passed: {correct_count} values verified")


@cocotb.test()
async def test_axis_dataover_large_numbers(dut):
    """Test with large numbers above threshold"""

    dut._log.info("Starting large numbers test")

    # Initialize tester
    tester = AxisDataoverTester(dut)

    # Large numbers above threshold
    large_data = [
        2000000,      # 2M
        10000000,     # 10M
        50000000,     # 50M
        100000000,    # 100M
        1000000000,   # 1B
        2000000000,   # 2B (max 32-bit signed)
    ]

    tester.test_data = large_data
    tester.expected_results = [1] * len(large_data)  # All should be above threshold

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Start data transmission
    await tester.start_data_transmission()

    # Monitor and verify
    correct_count = 0

    for i, (expected_data, expected_over) in enumerate(zip(tester.test_data, tester.expected_results)):
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        actual_data = int(dut.m_axis_tdata.value)
        actual_over = int(dut.data_over.value)

        assert actual_data == expected_data
        assert actual_over == expected_over, f"Large number test failed: {actual_data} should have data_over=1, got {actual_over}"

        correct_count += 1
        dut._log.info(f"✓ Large number test {i}: {actual_data} -> data_over={actual_over}")

        await RisingEdge(dut.aclk)

    dut._log.info(f"Large numbers test passed: {correct_count} values verified")


@cocotb.test()
async def test_axis_dataover_negative_numbers(dut):
    """Test with negative numbers (all should be below threshold)"""

    dut._log.info("Starting negative numbers test")

    # Initialize tester
    tester = AxisDataoverTester(dut)

    # Negative numbers (all below threshold)
    negative_data = [
        -1000000,     # Negative threshold
        -100,         # Small negative
        -100000,      # Large negative
        -2000000000,  # Very large negative
    ]

    tester.test_data = negative_data
    tester.expected_results = [0] * len(negative_data)  # All should be below threshold

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Start data transmission
    await tester.start_data_transmission()

    # Monitor and verify
    correct_count = 0

    for i, (expected_data, expected_over) in enumerate(zip(tester.test_data, tester.expected_results)):
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        actual_data = int(dut.m_axis_tdata.value)
        actual_over = int(dut.data_over.value)

        assert actual_data == expected_data
        assert actual_over == expected_over, f"Negative number test failed: {actual_data} should have data_over=0, got {actual_over}"

        correct_count += 1
        dut._log.info(f"✓ Negative number test {i}: {actual_data} -> data_over={actual_over}")

        await RisingEdge(dut.aclk)

    dut._log.info(f"Negative numbers test passed: {correct_count} values verified")


@cocotb.test()
async def test_axis_dataover_control_signals(dut):
    """Test control signals (pause, restart, etc.)"""

    dut._log.info("Starting control signals test")

    # Initialize tester
    tester = AxisDataoverTester(dut)

    # Simple test data
    test_data = [500000, 1500000, 2000000]  # Below, above, above
    tester.test_data = test_data
    tester.expected_results = [0, 1, 1]

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Test pause functionality
    dut._log.info("Testing pause functionality...")

    await tester.start_data_transmission()

    # Wait for first data
    while not dut.m_axis_tvalid.value:
        await RisingEdge(dut.aclk)

    # Pause transmission
    dut.i_pause.value = 1
    dut._log.info("Paused transmission")

    # Wait a few cycles while paused
    for _ in range(5):
        await RisingEdge(dut.aclk)
        assert dut.m_axis_tvalid.value == 0, "Data should not be valid while paused"

    # Resume transmission
    dut.i_pause.value = 0
    dut._log.info("Resumed transmission")

    # Continue monitoring remaining data
    for i in range(len(test_data)):
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        actual_data = int(dut.m_axis_tdata.value)
        actual_over = int(dut.data_over.value)
        expected_over = tester.expected_results[i]

        assert actual_over == expected_over, f"Control test failed at index {i}"

        dut._log.info(f"✓ Control test {i}: {actual_data} -> data_over={actual_over}")
        await RisingEdge(dut.aclk)

    dut._log.info("Control signals test passed")


@cocotb.test()
async def test_axis_dataover_csv_direct_comparison(dut):
    """Test that directly compares DUT output with CSV file contents"""
    """DUT에서 출력되는 데이터가 CSV 파일의 데이터와 정확히 일치하는지 확인"""

    dut._log.info("Starting CSV direct comparison test")

    # Initialize tester
    tester = AxisDataoverTester(dut)

    # Load CSV file data directly for comparison
    csv_filename = "test_data.csv"
    csv_data = []

    if not os.path.exists(csv_filename):
        raise TestFailure(f"CSV file {csv_filename} not found")

    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Skip empty rows
                try:
                    value = int(row[0])
                    csv_data.append(value)
                except ValueError as e:
                    dut._log.warning(f"Skipping invalid data in CSV: {row[0]} ({e})")

    if not csv_data:
        raise TestFailure("No valid data found in CSV file")

    dut._log.info(f"Loaded {len(csv_data)} reference values from {csv_filename}")
    dut._log.info(f"First 5 values: {csv_data[:5]}")
    dut._log.info(f"Last 5 values: {csv_data[-5:]}")

    # Start clock
    tester.clock_gen()

    # Reset DUT
    await tester.reset_dut()

    # Start data transmission
    await tester.start_data_transmission()

    # Wait for transmission to start
    while not dut.o_busy.value:
        await RisingEdge(dut.aclk)

    dut._log.info("Data transmission started - comparing with CSV data")

    # Compare each received data with CSV data
    comparison_count = 0
    match_count = 0

    for expected_data in csv_data:
        # Wait for valid data from DUT
        while not dut.m_axis_tvalid.value:
            await RisingEdge(dut.aclk)

        # Get actual data from DUT
        actual_data = int(dut.m_axis_tdata.value)

        # Compare with CSV data
        if actual_data != expected_data:
            raise TestFailure(f"CSV comparison failed at index {comparison_count}: "
                            f"expected {expected_data}, got {actual_data}")

        comparison_count += 1
        match_count += 1

        # Log progress for large files (every 50 values)
        if comparison_count % 50 == 0:
            dut._log.info(f"✓ Verified {comparison_count}/{len(csv_data)} values")

        # Wait for next data
        await RisingEdge(dut.aclk)

        # Check if transmission is complete (TLAST)
        if dut.m_axis_tlast.value:
            break

    # Wait for transmission to complete
    while dut.o_busy.value:
        await RisingEdge(dut.aclk)

    # Verify we received all expected data
    if comparison_count != len(csv_data):
        raise TestFailure(f"Incomplete transmission: received {comparison_count}/{len(csv_data)} values")

    dut._log.info(f"CSV direct comparison test PASSED: {match_count}/{len(csv_data)} values matched perfectly")
    dut._log.info("All DUT output values match the input CSV file contents exactly")


if __name__ == "__main__":
    print("Axis Dataover cocotb testbench")
    print("Run with: make cocotb")
