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
        dummy_repo = MagicMock()
        dummy_repo.get_commit.return_value = dummy_commit
        instance = mock_github_class.return_value
        instance.get_repo.return_value = dummy_repo

        commit_sha = "dummy_commit"
        state = "success"
        description = "Build passed"

        result = update_commit_status(commit_sha, state, description)

        dummy_repo.get_commit.assert_called_once_with(commit_sha)
        dummy_commit.create_status.assert_called_once_with(
            state=state,
            target_url="",
            description=description,
            context="CI Notification"
        )
        self.assertEqual(result, dummy_status.raw_data)

    @patch("util.Github")
    def test_missing_configuration(self, mock_github_class):
        """
        Test that update_commit_status raises an exception when required environment variables are missing.
        """
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
        os.environ["CI_SERVER_AUTH_TOKEN"] = "dummy_token"
        os.environ["REPO_OWNER"] = "dummy_owner"
        os.environ["REPO_NAME"] = "dummy_repo"
        
        instance = mock_github_class.return_value
        instance.get_repo.side_effect = Exception("Repository not found")
        
        with self.assertRaises(Exception) as context:
            update_commit_status("dummy_commit", "success", "Build passed")
        self.assertIn("Error accessing repository: Repository not found", str(context.exception))

    @patch("util.Github")
    def test_invalid_state(self, mock_github_class):
        """
        Test that update_commit_status does not send an update when given an invalid state.
        """
        os.environ["CI_SERVER_AUTH_TOKEN"] = "dummy_token"
        os.environ["REPO_OWNER"] = "dummy_owner"
        os.environ["REPO_NAME"] = "dummy_repo"

        commit_sha = "dummy_commit"
        invalid_state = "not_a_state"
        description = "Invalid state test"

        instance = mock_github_class.return_value
        dummy_repo = MagicMock()
        dummy_commit = MagicMock()
        instance.get_repo.return_value = dummy_repo
        dummy_repo.get_commit.return_value = dummy_commit

        with self.assertRaises(Exception) as context:
            update_commit_status(commit_sha, invalid_state, description)

        self.assertIn("Invalid commit status state", str(context.exception))
        dummy_commit.create_status.assert_not_called()
