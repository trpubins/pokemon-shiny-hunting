"""A utility for standardizing unit testing."""

from inspect import getmembers, isfunction
import sys
from typing import Any, List


def run_tests(module_name: str, test_number: int = None):
    """Run tests inside a test module. By default, runs all tests in the module
    unless test_number is specified."""
    # run a specific test number
    if test_number is not None:
        func = get_one_test_function(module_name, test_number)
        func()
        return
    
    # default to running all tests in the module
    test_functions = get_all_test_functions(module_name)
    for func in test_functions:
        func()
    return
    

def get_all_test_functions(module_name: str) -> List:
    """Retrieve all test functions in the provided module."""
    match_pattern = "test_"
    test_functions = [
        obj for name,obj in getmembers(sys.modules[module_name]) 
            if (isfunction(obj) and name.startswith(match_pattern))
    ]
    return test_functions


def get_one_test_function(module_name: str, test_number: int) -> Any:
    """Retrieve the specified test function in the provided module."""
    match_pattern = f"test_{test_number}_"
    test_functions = [
        obj for name,obj in getmembers(sys.modules[module_name]) 
            if (isfunction(obj) and name.startswith(match_pattern))
    ]
    if len(test_functions) == 0:
        raise ValueError(f"Test name starting with {match_pattern} not found in module {module_name}")

    return test_functions[0]
