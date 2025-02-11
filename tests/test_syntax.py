import unittest
import sys
import subprocess
import os
sys.path.append('app/lib')
from util import check_syntax, clone_repo


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
        self.assertFalse(clone_repo("https://gitfake.com/fake/url"))

    def test_clone_no_url(self):
        # check if the function clone_repo identifies a not real github repo
        self.assertFalse(clone_repo("https://github.com/5fake/0error-test"))

    def test_clone(self):
        # check if the function clone_repo is working correctly
        self.assertTrue(clone_repo("https://github.com/rtyley/small-test-repo"))

