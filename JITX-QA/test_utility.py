"""This file contains the methods required for executing the JITX QA test cases"""
from os import listdir, remove
from os.path import isdir, join, isfile
import filecmp
import sys
import platform
import pytest

# To import file from parent directory
sys.path.append("../")
from utility_methods import run_stanza_file

# Constants
STANZA_EXT= ".stanza"
BOARD_IMAGE= "board.svg"
SCHEMATIC_IMAGE= "schematic.svg"

def get_view_file(test_dir):
    """
    Returns the svg file for board/schematic view
    :param test_dir: Path of the test directory
    :return: Path of the view file
    """
    if isfile(join(test_dir,"board.svg")):
        return join(test_dir,"board.svg")
    else:
        return join(test_dir,"schematic.svg")

def generate_and_verify_views(test_dir, mainfile):
    """
    Generates board and schematic views and verifies them with the expected views
    :param test_dir: Path of the test directory
    :param mainfile: Name of the stanza file
    """
    run_stanza_file(test_dir, mainfile)
    try:
        if platform.system() == "Windows":
            expected_board = "expected-board-win.svg"
            expected_schematic = "expected-schematic-win.svg"
        else:
            expected_board = "expected-board.svg"
            expected_schematic = "expected-schematic.svg"
        assert filecmp.cmp(join(test_dir, BOARD_IMAGE), \
            join(test_dir, expected_board)), "Board view is incorrect"
        assert filecmp.cmp(join(test_dir, SCHEMATIC_IMAGE), \
            join(test_dir, expected_schematic)), "Scematic view is incorrect"
    except FileNotFoundError:
        pytest.fail("Views are not generated")

def run_and_verify(test_dir):
    """
    Executes the test case steps and verifies the output directory
    :param test_dir: Path of the test directory
    """
    assert isdir(test_dir), "No such directory exists: {}".format(test_dir)

    # Deleting board view file if already exists
    out_board = get_view_file(test_dir)
    if isfile(out_board):
        remove(out_board)

    # Deleting the schematics view file if already exists
    out_schematic = get_view_file(test_dir)
    if isfile(out_schematic):
        remove(out_schematic)

    # Running test stanza file
    files = [item for item in listdir(test_dir) if item.endswith(STANZA_EXT)]
    if files:
        generate_and_verify_views(test_dir, files[0])
    else:
        pytest.fail("No test stanza file found")
        return
