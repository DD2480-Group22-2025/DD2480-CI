import unittest
import requests
from unittest.mock import patch, mock_open, Mock
import subprocess
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from update_readme import get_public_url, commit_readme, README_FILE

class TestUpdateReadme(unittest.TestCase):
    '''Unit test for get_ngrok_url(), update_readme, and commit_readme functions'''

    def test_get_public_url_success(self):
        '''Test successful retrieval of the ngrok URL'''
        public_url = get_public_url()
        self.assertEqual(public_url, "https://292e-193-46-242-26.ngrok-free.app")
    
    @patch("requests.get")
    def test_get_public_url_no_tunnels(self, mock_get):
        '''Test case when no tunnels are found in the response'''
        
        # Mock the response when no tunnels are present
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tunnels": []
        }
        
        # Call the function under test
        public_url = get_public_url()
        
        # Assert that the function returns None when no tunnels are found
        self.assertIsNone(public_url)

    @patch("requests.get")
    def test_get_public_url_no_public_url(self, mock_get):
        '''Test case when the tunnel does not have a public_url'''
        
        # Mock the response when tunnels are present but no public_url is found
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tunnels": [
                {
                    "name": "command_line",
                    "ID": "89389d4c9b8cabac791cf197ac2d9ae1",
                    "uri": "/api/tunnels/command_line",
                    "public_url": None,  # No public URL
                    "proto": "https",
                    "config": {"addr": "http://localhost:8022", "inspect": True},
                    "metrics": {}
                }
            ]
        }

        # Call the function under test
        public_url = get_public_url()

        # Assert that the function returns None when no public_url is found
        self.assertIsNone(public_url)

    @patch("requests.get")
    def test_get_public_url_error(self, mock_get):
        '''Test case when there is a request error (e.g., network failure)'''
        
        # Mock a request exception (e.g., network failure)
        mock_get.side_effect = requests.RequestException("Network error")

        # Call the function under test
        public_url = get_public_url()

        # Assert that the function returns None due to the request error
        self.assertIsNone(public_url)
    
    @patch("subprocess.run")
    def test_commit_readme(self, mock_subprocess):
        '''Test the git commit process'''
        # Mock the subprocess.run calls
        mock_subprocess.return_value = None

        commit_readme()

        # Ensure the subprocess.run was called for reach git command
        mock_subprocess.assert_any_call(["git", "add", "README.md"])
        mock_subprocess.assert_any_call(["git", "commit", "-m", "Updated README.md with the latest public URL"])
        mock_subprocess.assert_any_call(["git", "push","origin","main"])

if __name__ == "__main__":
    unittest.main()