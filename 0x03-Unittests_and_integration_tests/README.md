# Project Overview

This project is designed to test the functionality of the access_nested_map function in the utils module. The access_nested_map function is intended to access nested values in a dictionary using a provided path.

## Task 1: Unit Testing with Parameterized Testing

In this task, we implemented unit tests for the access_nested_map function using the parameterized library. This allows us to test multiple scenarios with a single test method.

#### Test Cases
The following test cases are covered:
Accessing a value in a non-nested dictionary
Accessing a nested dictionary
Accessing a value in a nested dictionary

#### Test Code

The test code is implemented in the TestAccessNestedMap class, which inherits from unittest.TestCase. The test_access_nested_map method is decorated with @parameterized.expand to run the test with different inputs.
Running the Tests
To run the tests, execute the test file using the unittest framework.

Requirements
- Python 3.x
- parameterized library
- unittest framework

#### Usage
Clone the repository
    Install the required libraries using pip install parameterized
    Run the tests using python -m unittest test_file.py (replace test_file.py with the actual file name)