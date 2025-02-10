import unittest
import requests
from unittest.mock import patch, mock_open
import subprocess
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from update_readme import get_ngrok_url, update_readme, commit_readme, README_FILE

class TestUpdateReadme(unittest.TestCase):
    '''Unit test for get_ngrok_url(), update_readme, and commit_readme functions'''

    @patch("requests.get")
    def test_get_ngrok_url_success(self, mock_get):
        '''Test successfule retrieval of the ngrok URL'''
        mock_response = {"tunnels": [{"public_url": "http://example.ngrok.io"}]}
        # Mock the ngrok response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ngrok_url()
        self.assertEqual(result, "http://example.ngrok.io")
        mock_get.assert_called_once_with("http://127.0.0.1:4040/api/tunnels")

    
    @patch("requests.get")
    def test_get_ngrok_url_failure(self, mock_get):
        '''Test URL failure'''
        mock_get.side_effect = requests.exceptions.RequestException("Error")
        
        results = get_ngrok_url()
        self.assertIsNone(results)
        mock_get.assert_called_once_with("http://127.0.0.1:4040/api/tunnels")
    
    @patch("builtins.open", new_callable=mock_open, read_data="[FastAPI CI Build List](https://old-url.com)")
    @patch("requests.get")
    def test_update_readme_success(self, mock_get, mock_file):
        '''Test if the README file is updated with the correct ngrok URL'''
        # Mock the response from the URL
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"tunnels": [{"public_url": "http://example.ngrok.io"}]}

        ngrok_url = get_ngrok_url()
        update_readme(ngrok_url)

        # Check if the README file was updated with the new URL
        assert mock_file.call_count == 2
        mock_file().write.assert_called_once_with("[FastAPI CI Build List](http://example.ngrok.io/builds)")

    @patch("builtins.open", new_callable=mock_open)
    @patch("requests.get")
    def test_update_readme_no_ngrok_url(self, mock_get, mock_file):
        '''Test if the README is not updated if ngrok URL is not fetched'''
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"tunnels": []} # Empty tunnels list

        ngrok_url = get_ngrok_url()
        self.assertIsNone(ngrok_url)

        # No update should exist if no ngrok URL is fetched
        update_readme(ngrok_url)
        mock_file.assert_not_called()

    @patch("subprocess.run")
    def test_commit_readme(self, mock_subprocess):
        '''Test the git commit process'''
        # Mock the subprocess.run calls
        mock_subprocess.return_value = None

        commit_readme()

        # Ensure the subprocess.run was called for reach git command
        mock_subprocess.assert_any_call(["git", "add", "README.md"])
        mock_subprocess.assert_any_call(["git", "commit", "-m", "Updated README.md with the latest ngrok URL"])
        mock_subprocess.assert_any_call(["git", "push"])


if __name__ == "__main__":
    unittest.main()