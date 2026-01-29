import pytest
import sys

if __name__ == '__main__':
    sys.exit(pytest.main(["-q", "tests/test_case_insensitive.py::test_search_category_case_insensitive"]))
