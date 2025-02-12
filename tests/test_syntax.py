import unittest
import sys
import subprocess
import os
sys.path.append('app/lib')
from util import check_syntax, clone_repo, delete_repo


class TestSyntax(unittest.TestCase):

    def test_check_syntax(self):
        # check if the function check_syntax is working correctly
        self.assertTrue(check_syntax("app/lib/util.py"))

    def test_err_syntax(self):
        # check if the function check_syntax is working correctly
        self.assertFalse(check_syntax("tests/example_files.py"))

    def test_no_file(self):
        # check if the function check_syntax is working correctly
        self.assertFalse(check_syntax("tests/no_file.py"))
    

class TestClone(unittest.TestCase):
    
    def test_clone_not_github(self):
        # check if the function clone_repo identifies a not real github repo
        self.assertFalse(clone_repo("https://gitfake.com/fake/url", 123))

    def test_clone_no_url(self):
        # check if the function clone_repo identifies a not real github repo
        self.assertFalse(clone_repo("https://github.com/5fake/0error-test", 124))

    def test_clone(self):
        # check if the function clone_repo is working correctly
        self.assertTrue(clone_repo("https://github.com/rtyley/small-test-repo", 234))

    def test_clone_2(self):
        # the function clones the same repo but with a different id so it works
        self.assertTrue(clone_repo("https://github.com/rtyley/small-test-repo", 232))

    def test_same_name(self):
        # check if the function clone_repo is working correctly
        self.assertRaises(Exception, clone_repo("https://github.com/rtyley/small-test-repo", 232))

class TestDelete(unittest.TestCase):

    def test_delete(self):
        # check if the function delete_repo is working correctly
        self.assertTrue(delete_repo("small-test-repo-234"))

    def test_no_repo(self):
        # check that it cannot delete a repo that doesn't exist
        self.assertFalse(delete_repo("small-test-repo-234"))

    def test_delete2(self):
        # check if the function delete_repo is working correctly
        self.assertTrue(delete_repo("small-test-repo-232"))
