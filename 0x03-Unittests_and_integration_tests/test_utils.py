#!/usr/bin/env python3

"""
Unit tests for the utility functions: access_nested_map, get_json, and memoize.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map function with various inputs."""

    @parameterized.expand([
        ("simple_path", {"a": 1}, ("a",), 1),
        ("nested_dict", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_path", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, _, nested_map, path, expected):
        """Test that access_nested_map returns correct values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",), KeyError),
        ("missing_nested_key", {"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, _, nested_map, path, expected):
        """Test that access_nested_map raises KeyError on invalid path."""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json function with mocked HTTP responses."""

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": True}),
    ])
    @patch("utils.requests.get")
    def test_get_json(
        self,
        _,
        test_url: str,
        test_payload: dict,
        mock_get: Mock
    ) -> None:
        """Test that get_json returns the correct JSON payload."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoization behavior of the memoize decorator."""

    def test_memoize(self):
        """Test that the method is called only once when memoized."""

        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
