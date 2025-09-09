#!/usr/bin/env python3
"""
Generate test data for axis_dataover test
Creates CSV file with numbers above and below 1,000,000 threshold
"""

import random
import csv

def generate_test_data():
    """Generate test data with various values around 1,000,000 threshold"""

    test_data = []

    # Test cases around threshold (1,000,000)
    threshold = 1000000

    # Values below threshold
    below_threshold = [
        threshold - 1,      # Just below
        threshold - 100,    # Slightly below
        threshold - 1000,   # Moderately below
        threshold - 10000,  # Significantly below
        threshold // 2,     # Half of threshold
        threshold // 10,    # Tenth of threshold
        0,                  # Zero
        -100000,           # Negative value
        -1000000,          # Negative threshold
    ]

    # Values above threshold
    above_threshold = [
        threshold + 1,      # Just above
        threshold + 100,    # Slightly above
        threshold + 1000,   # Moderately above
        threshold + 10000,  # Significantly above
        threshold * 2,      # Double threshold
        threshold * 10,     # Ten times threshold
        2000000,           # 2 million
        10000000,          # 10 million
        50000000,          # 50 million
        100000000,         # 100 million
        2000000000,        # 2 billion (within 32-bit signed range)
    ]

    # Combine all test data
    test_data.extend(below_threshold)
    test_data.extend(above_threshold)

    # Add some random values for comprehensive testing
    for _ in range(50):
        # Random values in various ranges
        rand_values = [
            random.randint(-1000000, 1000000),      # Around threshold
            random.randint(-10000000, 10000000),    # Larger range
            random.randint(0, 2000000),             # Positive around threshold
            random.randint(1000001, 5000000),       # Above threshold
        ]
        test_data.extend(rand_values)

    # Add edge cases for 32-bit signed integers
    edge_cases = [
        -2147483648,  # Minimum signed 32-bit
        -1,           # Negative one
        0,            # Zero
        1,            # Positive one
        2147483647,   # Maximum signed 32-bit
        999999,       # Just below threshold
        1000000,      # Exactly threshold
        1000001,      # Just above threshold
    ]

    test_data.extend(edge_cases)

    # Remove duplicates and sort
    unique_data = list(set(test_data))

    # Filter to valid 32-bit signed range
    valid_data = [x for x in unique_data if -2147483648 <= x <= 2147483647]

    # Sort for predictable order
    valid_data.sort()

    return valid_data

def main():
    """Main function to generate CSV file"""

    print("Generating test data for axis_dataover test...")

    # Generate test data
    test_values = generate_test_data()

    print(f"Generated {len(test_values)} test values")

    # Write to CSV file
    with open('test_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for value in test_values:
            writer.writerow([value])

    print("Test data written to test_data.csv")

    # Print summary statistics
    threshold = 1000000
    above_count = sum(1 for x in test_values if x > threshold)
    below_count = sum(1 for x in test_values if x <= threshold)

    print(f"\nSummary:")
    print(f"  Total values: {len(test_values)}")
    print(f"  Values > {threshold}: {above_count}")
    print(f"  Values <= {threshold}: {below_count}")
    print(f"  Range: {min(test_values)} to {max(test_values)}")

    # Show first and last few values
    print(f"\nFirst 10 values: {test_values[:10]}")
    print(f"Last 10 values: {test_values[-10:]}")

if __name__ == "__main__":
    main()
