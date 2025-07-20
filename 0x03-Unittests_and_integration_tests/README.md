# Python Utils Project — Unit Testing

This project demonstrates proper unit testing of Python utility functions using `unittest`, `parameterized`, and `unittest.mock`. All tests follow the ALX/Holberton-style guidelines and test three core functions: `access_nested_map`, `get_json`, and `memoize`.

---

## Requirements

- Ubuntu 18.04 LTS
- Python 3.7
- `pycodestyle` version 2.5 (PEP8 compliant)
- `parameterized` package (`pip install parameterized`)

---

## Tested Functions

### 1. `access_nested_map(nested_map: Mapping, path: Sequence) -> Any`
Safely accesses values from a nested dictionary using a sequence of keys.

**Example:**
```python
access_nested_map({"a": {"b": 2}}, ("a", "b"))  # ➜ 2