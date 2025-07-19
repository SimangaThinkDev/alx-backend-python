import unittest
from parameterized import parameterized
import requests

# Import classes to be tested
from . import utils

class TestAccessNestedMap(unittest.TestCase):
    """
    A class that uses parameterized testing to broadingly test
    multiple possibilities at once.
    """

    @parameterized.expand([
        [{"a": 1}, ("a",), 1],
        [{"a": {"b": 2}}, ("a",), {"b": 2}],
        [{"a": {"b": 2}}, ("a", "b"), 2]
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        This method tests for whether a method in our utils module
        behaves as expected
        """
        self.assertEqual( expected, utils.access_nested_map(nested_map, path) )


if __name__ == "__main__":
    unittest.main()