"""This file contains the Schematic QA test cases"""
import pytest
import test_utility

# Methods to execute the Schematic QA test cases
def test_case_1():
    test_utility.run_and_verify("test-case-1")

def test_case_2():
    test_utility.run_and_verify("test-case-2")

def test_case_4():
    test_utility.run_and_verify("test-case-4")
