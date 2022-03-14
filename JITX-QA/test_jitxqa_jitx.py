"""This file contains the JITX QA test cases"""
import pytest
import test_utility

# Methods to execute the JITX QA test cases
def test_one_large_component():
    test_utility.run_and_verify("one-large-component")

def test_two_large_component():
    test_utility.run_and_verify("two-large-component")

def test_very_large_component():
    test_utility.run_and_verify("very-large-component")
