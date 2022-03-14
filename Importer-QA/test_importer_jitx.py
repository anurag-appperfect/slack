"""This file contains the Importer QA test cases"""
import pytest
import test_utility

# Methods to execute the Importer QA test cases
def test_kicad_exists():
    test_utility.verify_negative_test("test-kicad-exists", \
        "Directory output already exists and overwrite is disabled")

def test_kicad_not_exists():
    test_utility.verify_negative_test("test-kicad-not-exists", "No input directory input found")

def test_kicad_not_directory():
    test_utility.verify_negative_test("test-kicad-not-directory", "Not a directory: input.txt")

def test_altium_bulk_import():
    test_utility.run_and_verify("test-altium-bulk-import")

def test_altium_import():
    test_utility.run_and_verify("test-altium-import")

def test_altium_import_box_symbols():
    test_utility.run_and_verify("test-altium-import-box-symbols")

def test_altium_import_existing():
    test_utility.run_and_verify("test-altium-import-existing")

def test_kicad():
    test_utility.run_and_verify("test-kicad")

def test_kicad_box_symbols():
    test_utility.run_and_verify("test-kicad-box-symbols")

def test_kicad_mod():
    test_utility.run_and_verify("test-kicad-mod")

def test_kicad_overwrite():
    test_utility.run_and_verify("test-kicad-overwrite")

def test_kicad_pcb():
    test_utility.run_and_verify("test-kicad-pcb")

def test_kicad_lib():
    test_utility.run_and_verify("test-kicad-lib")

def test_kicad_sch():
    test_utility.run_and_verify("test-kicad-sch")
