import unittest
import os
import sys
import shutil
import subprocess
from fastapi.testclient import TestClient
sys.path.append('app')
from main import app

class TestCITestExecution(unittest.TestCase):
    def setUp(self):
        """Set up test environment with a mock repository"""
        self.client = TestClient(app)
        self.test_dir = "mock_repo"
        os.makedirs(os.path.join(self.test_dir, "tests"), exist_ok=True)
        
        # Create a mock repository with test files
        self.create_mock_repository()
        
        # Store original environment variables
        self.original_env = {
            'CI_SERVER_AUTH_TOKEN': os.getenv('CI_SERVER_AUTH_TOKEN'),
            'REPO_OWNER': os.getenv('REPO_OWNER'),
            'REPO_NAME': os.getenv('REPO_NAME')
        }
        
        # Set test environment variables
        os.environ['CI_SERVER_AUTH_TOKEN'] = 'test_token'
        os.environ['REPO_OWNER'] = 'test_owner'
        os.environ['REPO_NAME'] = 'test_repo'

    def tearDown(self):
        """Clean up test environment"""
        try:
            shutil.rmtree(self.test_dir)
            if os.path.exists("cloned_repo"):
                shutil.rmtree("cloned_repo")
        except Exception as e:
            print(f"Warning: Cleanup failed: {e}")
            
        # Restore original environment variables
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

    def create_mock_repository(self):
        """Create a mock repository with test files"""
        # Create a passing test
        with open(os.path.join(self.test_dir, "tests", "test_passing.py"), "w") as f:
            f.write("""
def test_that_passes():
    assert True
""")
        
        # Create a failing test
        with open(os.path.join(self.test_dir, "tests", "test_failing.py"), "w") as f:
            f.write("""
def test_that_fails():
    assert False
""")
        
        # Create an invalid syntax test
        with open(os.path.join(self.test_dir, "tests", "test_syntax_error.py"), "w") as f:
            f.write("""
def test_with_syntax_error()
    this is not valid python
""")

    def test_webhook_with_passing_tests(self):
        """Test webhook handling when all tests pass"""
        payload = {
            "ref": "refs/heads/main",
            "repository": {
                "clone_url": "https://github.com/test/repo.git",
                "full_name": "test/repo",
                "pushed_at": "test123"
            },
            "head_commit": {
                "id": "testsha123"
            }
        }
        
        # Mock the clone_repo function to use our test directory
        import app.lib.util as util
        original_clone = util.clone_repo
        util.clone_repo = lambda *args: True
        
        try:
            response = self.client.post("/webhook", json=payload)
            self.assertEqual(response.status_code, 200)
            # Add more specific assertions based on your response format
        finally:
            util.clone_repo = original_clone

    def test_webhook_with_failing_tests(self):
        """Test webhook handling when tests fail"""
        payload = {
            "ref": "refs/heads/main",
            "repository": {
                "clone_url": "https://github.com/test/repo.git",
                "full_name": "test/repo",
                "pushed_at": "test123"
            },
            "head_commit": {
                "id": "testsha123"
            }
        }
        
        # Mock the clone_repo function and ensure failing tests are run
        import app.lib.util as util
        original_clone = util.clone_repo
        util.clone_repo = lambda *args: True
        
        try:
            response = self.client.post("/webhook", json=payload)
            self.assertEqual(response.status_code, 200)
            # Add assertions to verify failure is properly handled
        finally:
            util.clone_repo = original_clone

    def test_test_execution_error_handling(self):
        """Test proper handling of test execution errors"""
        payload = {
            "ref": "refs/heads/main",
            "repository": {
                "clone_url": "https://github.com/test/repo.git",
                "full_name": "test/repo",
                "pushed_at": "test123"
            },
            "head_commit": {
                "id": "testsha123"
            }
        }
        
        # Mock clone_repo to simulate a failed clone
        import app.lib.util as util
        original_clone = util.clone_repo
        util.clone_repo = lambda *args: False
        
        try:
            response = self.client.post("/webhook", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Repository clone failed")
            self.assertEqual(response.json()["status"], "error")
        finally:
            # Restore original function
            util.clone_repo = original_clone

if __name__ == '__main__':
    unittest.main()
