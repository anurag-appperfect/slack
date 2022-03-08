"""This file contains the methods required for executing the Exporter QA test cases"""
from os import listdir
from os.path import isdir, join
import shutil
import sys
import platform
import pytest

# To import file from parent directory
sys.path.append("../")
from utility_methods import comp_dir, run_stanza_file, get_output_dir

# Constants
STANZA_EXT = ".stanza"
BOARD_IMAGE = "board.svg"
SCHEMATIC_IMAGE = "schematic.svg"

def run_and_verify(test_dir):
    """
    Executes the test case steps and verifies the output directory
    :param test_dir: Path of the test directory
    """
    assert isdir(test_dir), "No such directory exists: {}".format(test_dir)
    outdir= get_output_dir(test_dir)

    # Deleting output directory if already exists
    if isdir(outdir):
        shutil.rmtree(outdir)

    # Running test stanza file
    files = [item for item in listdir(test_dir) if item.endswith(STANZA_EXT)]
    if files:
        run_stanza_file(test_dir, files[0])
    else:
        pytest.fail("No test stanza file found")
        return

    # Verify and compare output directory
    actual_output_dir= get_output_dir(test_dir)
    if platform.system() == "Windows":
        expected_output_dir= join(test_dir, "expected-output-win")
    else:
        expected_output_dir= join(test_dir, "expected-output")

    assert isdir(actual_output_dir), "Output not generated"
    assert comp_dir(actual_output_dir, expected_output_dir), "Output directory doesn't match"
