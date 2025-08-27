#!/usr/bin/env python3
"""
Simple test to check if output directory exists and is writable.
"""

import os
import tempfile


def test_output_directory():
    """Test if output directory exists and is writable."""
    output_dir = "output"

    print(f"Testing output directory: {output_dir}")

    # Check if directory exists
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    # Test if directory is writable
    test_file = os.path.join(output_dir, "test_write.txt")
    try:
        with open(test_file, 'w') as f:
            f.write("Test write successful\n")
        print(f"✓ Output directory is writable")
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"✗ Output directory not writable: {e}")
        return False


def test_temp_directory():
    """Test if we can write to temp directory as fallback."""
    try:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"Test temp write successful\n")
        print("✓ Temp directory is writable")
        os.unlink(f.name)
        return True
    except Exception as e:
        print(f"✗ Temp directory not writable: {e}")
        return False


if __name__ == "__main__":
    print("Testing file system access...")
    output_ok = test_output_directory()
    temp_ok = test_temp_directory()

    if output_ok:
        print("\nOutput directory is ready for use!")
    else:
        print("\nWarning: Output directory has issues, using temp directory as fallback")
