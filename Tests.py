from unittest.mock import patch
from unittest import TestCase
from unittest import main

from Issues.Issue17_13 import csvImport

# Alyssa Maguire

# unittests for Issue 17 upload CSV
# https://github.com/VERSO-UVM/interactive-management-app/issues/17


class TestCSVMethods(TestCase):

    """
    Alyssa Maguire

    INSTRUCTIONS
    Modify import to acquire issue 17/issue 13
    Modify test data file paths if necessary
    """

    __TEST_DATA_FILE: str = "test_data/set1.csv"

    @patch('builtins.input', side_effect=[__TEST_DATA_FILE])
    def test_get_answer_yes(self, mock_input):
        csvImport()

    # TODO: This test does not currently pass (input loop)
    # Options:
    # 1. Manual input
    # 2. Modify csvImport() to accept filename as param
    @patch('builtins.input', side_effect=["missing_file.csv"])
    def test_missing_file(self, mock_input):
        csvImport()


if __name__ == '__main__':
    main()
