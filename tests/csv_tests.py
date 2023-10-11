import sys
import os.path

from unittest.mock import patch
from unittest import TestCase
from unittest import main as test


# Alyssa Maguire

# unittests for Issue 17 upload CSV
# https://github.com/VERSO-UVM/interactive-management-app/issues/17

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from Issues.Issue17_13 import csvImport
class TestCSVMethods(TestCase):
    """
    Alyssa Maguire

    INSTRUCTIONS
    Modify import to acquire issue 17/issue 13
    Modify test data file paths if necessary
    """

    __TEST_DATA_FILE: str = "test_data/set1.csv"

    @patch('Issues.Issue17_13.csvImport', return_value=__TEST_DATA_FILE)
    def test_open(self, input):
        self.assertEqual(csvImport(), True)

    def test_missing_file(self):
        pass

    def test_file_lock(self):
        pass


if __name__ == '__main__':
    test()