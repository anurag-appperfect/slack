"""This file contains the methods required for executing the Schematic QA test cases"""
from os import remove, listdir
from os.path import isdir, join, isfile, expanduser, dirname, abspath
import subprocess
import filecmp
import xml.dom.minidom
import sys
import platform
import pytest

# To import file from parent directory
sys.path.append("../")
from utility_methods import get_current_jitx_version

# Constants
STANZA_EXT= ".stanza"
BOARD_IMAGE= "board.svg"
FILE = "ble-mote.stanza"
SCHEMATIC_IMAGE= "schematic.svg"

# Path of stanza.proj file
OCDB_PATH = join(join(dirname(dirname(abspath(__file__))),"ocdb"),"stanza.proj").replace('\\','/')

def run_stanza_file(directory, file):
    """
    Runs the given stanza file
    :param directory: Path of the directory containing the stanza file
    :param file: Name of the stanza file
    """
    if platform.system() == "Windows":
        command = "cd " + directory + "\n" + "jitx run designs/" + file
        if int(directory[-1]) == 4:
            command += " > output.txt \n"
        else:
            command += "\n"
        try:
            process = subprocess.Popen( "cmd.exe", shell=False, universal_newlines=True,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            out, err = process.communicate(command)
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(
                err.cmd, err.returncode, err.output))
    else:
        command = "cd " + directory + " ; jitx run designs/" + file
        if int(directory[-1]) == 4:
            command += " > output.txt"
        try:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, check=True)
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(
                err.cmd, err.returncode, err.output))

def get_schematic_file(test_dir):
    """
    Returns the svg file for schematic view
    :param test_dir: Path of the test directory
    :return: Path of the schematic file
    """
    if isfile(join(test_dir, "schematic.svg")):
        return join(test_dir, "schematic.svg")
    else:
        return ""

def check_terminal_output(test_dir, mainfile, expected_output):
    """
    Compares the terminal output on running stanza file with expected terminal output
    :param test_dir: Path of the test directory
    :param mainfile: Name of the stanza file
    :param expected_output: Expected output filename
    """
    run_stanza_file(test_dir, mainfile)
    try:
        assert filecmp.cmp(join(test_dir, "output.txt"), \
            join(test_dir, expected_output)), "Terminal output is incorrect"
    except FileNotFoundError:
        pytest.fail("Terminal output file are not generated")

def check_violet_rectangle(test_dir, schematic_svg):
    """
    Checks for violet rectangle in svg file
    :param test_dir: Path of the test directory
    :param schematic_svg: Schematic svg filename
    :return: True if violet rectangle is present else False
    """
    filename  = test_dir + "/" + schematic_svg
    doc = xml.dom.minidom.parse(filename)
    for i in range(34):
        name = doc.getElementsByTagName("polygon")[i].attributes
        if name.getNamedItem("stroke") is not None:
            if name.getNamedItem("stroke").nodeValue == "rgb(68.0%, 51.0%, 100.0%, 100.0%)":
                return True
    return False

def run_and_verify(test_dir):
    """
    Executes the test case steps and verifies the output directory
    :param test_dir: Path of the test directory
    """
    assert isdir(test_dir), "No such directory exists: {}".format(test_dir)
    out_schematic = get_schematic_file(test_dir)

    # Deleting output directory if already exists
    if isfile(out_schematic):
        remove(out_schematic)

    # Removing cache from jitx root directory
    cache_dir_path = join(join(join(expanduser("~"), ".jitx"), get_current_jitx_version()), "cache")
    if isdir(cache_dir_path):
        for cache in listdir(cache_dir_path):
            remove(join(cache_dir_path, cache))

    # Adding ocdb component to stanza.proj file
    try:
        ab = join(test_dir, "designs")
        temp = open(join(ab, "stanza.proj"), "a")
        cmd = ["include \""+OCDB_PATH+"\""]
        temp.writelines(cmd)
        temp.close()
    except Exception as err:
        pytest.fail("Could not find stanza.proj file." + str(err))

    if int(test_dir[-1]) == 1:
        check_terminal_output(test_dir,FILE,"expected-output.txt")

    elif int(test_dir[-1]) == 2:
        run_stanza_file(test_dir,FILE)
        if check_violet_rectangle(test_dir,SCHEMATIC_IMAGE):
            pytest.fail("Schematic view contain voilet rectangle")
    elif int(test_dir[-1]) == 4:
        if platform.system() == "Windows":
            expected_output = "expected-output-win.txt"
            expected_reload_output = "expected-reload-output-win.txt"
        else:
            expected_output = "expected-output.txt"
            expected_reload_output = "expected-reload-output.txt"
        check_terminal_output(test_dir,FILE, expected_output)
        check_terminal_output(test_dir,FILE, expected_reload_output)
    else:
        pytest.fail("Test case not valid")
        return
