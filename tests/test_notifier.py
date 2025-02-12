import os
import unittest
import sys
from unittest.mock import patch, MagicMock

# Import the function to test from the util module.
sys.path.append('app/lib')
from util import update_commit_status

class TestUpdateCommitStatus(unittest.TestCase):
    def setUp(self):
        # Set environment variables for testing purposes.
        os.environ["CI_SERVER_AUTH_TOKEN"] = "dummy_token"
        os.environ["REPO_OWNER"] = "dummy_owner"
        os.environ["REPO_NAME"] = "dummy_repo"

    @patch("util.Github")
    def test_successful_update(self, mock_github_class):
        """
        Test that update_commit_status returns the correct data when the GitHub API call succeeds.
        """
        # Create a dummy commit object with a dummy create_status method.
        dummy_commit = MagicMock()
        dummy_status = MagicMock()
        dummy_status.raw_data = {
            "state": "success",
            "description": "Build passed",
            "context": "CI Notification",
            "commit": "dummy_commit",
            "url": "https://api.github.com/repos/dummy_owner/dummy_repo/statuses/dummy_commit"
        }
        dummy_commit.create_status.return_value = dummy_status
        
        # Create a dummy repository that returns our dummy commit.
        dummy_repo = MagicMock()
        dummy_repo.get_commit.return_value = dummy_commit
        
        # Configure the dummy Github instance to return our dummy repository.
        instance = mock_github_class.return_value
        instance.get_repo.return_value = dummy_repo

        commit_sha = "dummy_commit"
        state = "success"
        description = "Build passed"
        
        # Call the function under test.
        result = update_commit_status(commit_sha, state, description)
        
        # Verify that the dummy functions were called with expected parameters.
        dummy_repo.get_commit.assert_called_once_with(commit_sha)
        dummy_commit.create_status.assert_called_once_with(
            state=state,
            target_url="",
            description=description,
            context="CI Notification"
        )
        # Assert that the result matches the dummy status's raw_data.
        self.assertEqual(result, dummy_status.raw_data)

    @patch("util.Github")
    def test_missing_configuration(self, mock_github_class):
        """
        Test that update_commit_status raises an exception when required environment variables are missing.
        """
        # Remove the environment variables.
        os.environ.pop("CI_SERVER_AUTH_TOKEN", None)
        os.environ.pop("REPO_OWNER", None)
        os.environ.pop("REPO_NAME", None)
        
        with self.assertRaises(Exception) as context:
            update_commit_status("dummy_commit", "success", "Build passed")
        self.assertIn("Missing GitHub configuration", str(context.exception))

    @patch("util.Github")
    def test_error_accessing_repository(self, mock_github_class):
        """
        Test that update_commit_status raises an exception if the repository cannot be accessed.
        """
        # Ensure environment variables are set.
        os.environ["CI_SERVER_AUTH_TOKEN"] = "dummy_token"
        os.environ["REPO_OWNER"] = "dummy_owner"
        os.environ["REPO_NAME"] = "dummy_repo"
        
        # Simulate an error when calling get_repo.
        instance = mock_github_class.return_value
        instance.get_repo.side_effect = Exception("Repository not found")
        
        with self.assertRaises(Exception) as context:
            update_commit_status("dummy_commit", "success", "Build passed")
        self.assertIn("Error accessing repository: Repository not found", str(context.exception))