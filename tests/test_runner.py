import unittest
import pytest
import os
import sys
import coverage
import shutil

class TestRunner(unittest.TestCase):
    def setUp(self):
        """Create a temporary test directory with some test files"""
        self.test_dir = "temp_test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a simple test file that will pass
        self.passing_test = """
def test_that_passes():
    assert True
"""
        # Create a simple test file that will fail
        self.failing_test = """
def test_that_fails():
    assert False
"""
        with open(os.path.join(self.test_dir, "test_passing.py"), "w") as f:
            f.write(self.passing_test)
            
    def tearDown(self):
        """Clean up temporary test files"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"Warning: Could not clean up {self.test_dir}: {e}")

    def test_run_passing_tests(self):
        """Test that passing tests are correctly identified"""
        result = pytest.main([self.test_dir])
        self.assertEqual(result, pytest.ExitCode.OK)

    def test_run_failing_tests(self):
        """Test that failing tests are correctly identified"""
        # Write the failing test
        with open(os.path.join(self.test_dir, "test_failing.py"), "w") as f:
            f.write(self.failing_test)
            
        result = pytest.main([self.test_dir])
        self.assertEqual(result, pytest.ExitCode.TESTS_FAILED)

    def test_with_coverage(self):
        """Test that coverage reporting works"""
        cov = coverage.Coverage()
        with cov.collect():
            pytest.main([self.test_dir])
        
        cov.save()
        
        # Verify coverage file was created
        self.assertTrue(os.path.exists(".coverage"))
        
        # Clean up coverage file
        try:
            if os.path.exists(".coverage"):
                os.remove(".coverage")
        except Exception as e:
            print(f"Warning: Could not remove .coverage file: {e}")

    def test_no_tests_found(self):
        """Test behavior when no tests are found"""
        empty_dir = "empty_test_dir"
        os.makedirs(empty_dir, exist_ok=True)
        
        result = pytest.main([empty_dir])
        
        try:
            shutil.rmtree(empty_dir)
        except Exception as e:
            print(f"Warning: Could not clean up {empty_dir}: {e}")
            
        self.assertEqual(result, pytest.ExitCode.NO_TESTS_COLLECTED)
