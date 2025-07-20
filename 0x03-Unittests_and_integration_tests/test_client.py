#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
import requests
from unittest.mock import patch, PropertyMock, Mock
from utils import get_json
from parameterized import parameterized
from parameterized import parameterized_class
from utils import access_nested_map
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient methods"""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that .org returns expected data and calls get_json once"""
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct repos_url"""
        test_url = "https://api.github.com/orgs/test/repos"
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": test_url}
        ):
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, test_url)

@patch("client.get_json")
def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list and calls get_json"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        test_url = "https://api.github.com/orgs/test/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value=test_url
        ) as mock_url:
            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(test_url)
            mock_url.assert_called_once()

@parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

class TestIntegrationGithubOrgClient(unittest.TestCase):
        """Integration test for GithubOrgClient.public_repos"""
        @classmethod
        def setUpClass(cls):
            """Start patcher and configure fixture-based side effects"""
            cls.get_patcher = patch("requests.get")
            mock_get = cls.get_patcher.start()
            # Repeat mocks to match the number of HTTP requests in your tests
            mock_get.side_effect = [
                Mock(**{"json.return_value": cls.org_payload}),
                Mock(**{"json.return_value": cls.repos_payload}),
                Mock(**{"json.return_value": cls.org_payload}),
                Mock(**{"json.return_value": cls.repos_payload}),
            ]

        @classmethod
        def tearDownClass(cls):
            """Stop patcher"""
            cls.get_patcher.stop()


def test_public_repos(self):
            """Test public_repos returns full repo list from fixture"""
            client = GithubOrgClient("test_org")
            self.assertEqual(
                client.public_repos(),
                self.expected_repos
            )

def test_public_repos_with_license(self):
            """Test public_repos filters repos by license"""
            client = GithubOrgClient("test_org")
            self.assertEqual(
                client.public_repos(license="apache-2.0"),
                self.apache2_repos
            )


if __name__ == '__main__':
    unittest.main()
