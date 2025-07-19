#!/usr/bin/env python3

"""
Implementing unit tests for the access_nested_map 
function using the parameterized library. 
This allows us to test multiple scenarios with 
a single test method.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

# Import classes to be tested
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
    """
    A class that uses parameterized testing to broadingly test
    multiple possibilities at once.
    """

    @parameterized.expand([
        [{"a": 1}, ("a",), 1],
        [{"a": {"b": 2}}, ("a",), {"b": 2}],
        [{"a": {"b": 2}}, ("a", "b"), 2],
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        This method tests for whether a method in our utils module
        behaves as expected
        """
        self.assertEqual( expected, access_nested_map(nested_map, path) )

    @parameterized.expand([
        [{}, ("a",), KeyError],
        [{"a":1}, ("a", "b",), KeyError]
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Tests for exceptional conditions
        """
        self.assertRaises( expected, access_nested_map, nested_map, path )

class TestGetJson(unittest.TestCase):
    """
    class and implement the TestGetJson.test_get_json 
    method to test that utils.get_json returns the 
    expected result.
    """

    @parameterized.expand([
        ["http://example.com", {"payload": True}],
        ["http://holberton.io", {"payload": True}],
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get) -> None:
        """
        Test that the output of get_json is equal to test_payload.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call for testing
        result = get_json( test_url )

        mock_get.assert_called_once_with( test_url )
        self.assertEqual( get_json(test_url), test_payload )


if __name__ == "__main__":
    unittest.main()