import unittest
import sys
sys.path.append('app/lib')
from util import check_syntax

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