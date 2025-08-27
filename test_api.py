#!/usr/bin/env python3
"""
Test script for the OCR-Tech API
"""

import requests
import json
import time
import os
from pathlib import Path

# Test configuration
API_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "demo_image.png"  # Use the existing demo image


def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


def test_image_processing():
    """Test image processing endpoint"""
    print("Testing image processing...")

    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"✗ Test image not found: {TEST_IMAGE_PATH}")
        return False

    try:
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'file': (os.path.basename(
                TEST_IMAGE_PATH), f, 'image/png')}
            response = requests.post(f"{API_URL}/process/image", files=files)

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Image processing successful")
            print(f"  - Filename: {result['filename']}")
            print(f"  - Pages: {result['total_pages']}")
            print(f"  - Success: {result['success']}")

            # Print first result if available
            if result['results'] and len(result['results']) > 0:
                first_result = result['results'][0]
                print(
                    f"  - Text samples: {len(first_result.get('texts', []))} text elements")
                print(
                    f"  - Arranged text preview: {first_result.get('arranged_text', '')[:100]}...")

            return True
        else:
            print(f"✗ Image processing failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"✗ Image processing error: {e}")
        return False


def test_multiple_files():
    """Test multiple files processing"""
    print("Testing multiple files processing...")

    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"✗ Test image not found: {TEST_IMAGE_PATH}")
        return False

    try:
        with open(TEST_IMAGE_PATH, 'rb') as f1, open(TEST_IMAGE_PATH, 'rb') as f2:
            files = [
                ('files', (f'test1.png', f1, 'image/png')),
                ('files', (f'test2.png', f2, 'image/png'))
            ]
            response = requests.post(
                f"{API_URL}/process/multiple", files=files)

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Multiple files processing successful")
            print(f"  - Total files: {result['total_files']}")
            print(f"  - Results: {len(result['results'])}")

            for file_result in result['results']:
                status = "✓" if file_result.get('success') else "✗"
                print(
                    f"  {status} {file_result['filename']}: {file_result.get('type', 'unknown')}")

            return True
        else:
            print(
                f"✗ Multiple files processing failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"✗ Multiple files processing error: {e}")
        return False


def main():
    """Run all tests"""
    print("Starting OCR-Tech API tests...")
    print("=" * 50)

    # Wait a moment for the API to start
    time.sleep(2)

    tests = [
        test_health_check,
        test_image_processing,
        test_multiple_files
    ]

    results = []
    for test in tests:
        results.append(test())
        print()

    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests passed! API is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Check the API implementation.")
        return 1


if __name__ == "__main__":
    exit(main())
