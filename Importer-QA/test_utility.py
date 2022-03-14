"""This file contains the methods required for executing the Importer QA test cases"""
import logging
from os import listdir
from os.path import isdir, join, basename, dirname, abspath
import subprocess
import filecmp
import shutil
import glob
import sys
import platform
import pytest

# To import file from parent directory
sys.path.append("../")
from utility_methods import comp_dir, get_output_dir

# Constants
STANZA_EXT = ".stanza"
BOARD_IMAGE = "board.svg"
SCHEMATIC_IMAGE = "schematic.svg"
JITX_DESIGN = "jitx-design"

# Path of stanza.proj file
OCDB_PATH = join(join(dirname(dirname(abspath(__file__))),"ocdb"),"stanza.proj").replace('\\','/')

def run_command(command):
    """
    Executes the given command
    :param command: Command to be executed
    """
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen( "cmd.exe", shell=False, universal_newlines=True,
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate(command)
        else:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, check=True)
    except subprocess.CalledProcessError as err:
        logging.error(err.output)
        pytest.fail("Test case failed with error "+ err.output)

def get_main_filename(test_dir):
    """
    Returns the name of the stanza files in given directory
    :param test_dir: Path of the test directory
    :return: List of names of stanza files
    """
    input_dir= join(test_dir, "input")
    input_dir_files= listdir(input_dir)
    main_files=[]
    if "kicad" in test_dir:
        files = [item for item in input_dir_files if item.endswith(".kicad_pcb")]
        main_files= [files[0].split(".")[0]+ STANZA_EXT] if files else ["KicadProject.stanza"]
    elif "altium" in test_dir:
        files = glob.glob(input_dir + "/**/*(PRJPCB).JSON", recursive = True)
        main_files= [basename(file).replace("(PRJPCB).JSON", STANZA_EXT) for file in files]
    return main_files

def generate_and_verify_views(test_dir, output_dir, mainfile):
    """
    Generates board and schematic views and verifies them with the expected views
    :param test_dir: Path of the test directory
    :param output_dir: Path of the output directory
    :param mainfile: Name of the stanza file
    """
    try:
        file= open(join(output_dir, mainfile), "a")
        cmd = ["save-to-svg(\""+BOARD_IMAGE+"\")", "save-schematic-to-svg(\""+SCHEMATIC_IMAGE+"\")"]
        file.writelines(cmd)
    except Exception as err:
        pytest.fail("Main stanza file is not generated." + err)
    finally:
        file.close()
    if platform.system() == "Windows":
        command = "cd " + output_dir+ "\n"+ "jitx run " + mainfile+"\n"
    else:
        command = "cd " + output_dir + " ; jitx run " + mainfile
    run_command(command)

    # Verifying generated views
    mainfile_name = mainfile.split(".")[0]
    if platform.system() == "Windows":
        expected_board = mainfile_name+ "-win-"+ BOARD_IMAGE
        expected_schematic = mainfile_name+ "-win-"+ SCHEMATIC_IMAGE
    else:
        expected_board = mainfile_name+ "-"+ BOARD_IMAGE
        expected_schematic = mainfile_name+ "-"+ SCHEMATIC_IMAGE
    try:
        assert filecmp.cmp(join(output_dir, BOARD_IMAGE), \
            join(test_dir, expected_board)), "Board view is incorrect for " + mainfile
        assert filecmp.cmp(join(output_dir, SCHEMATIC_IMAGE), \
            join(test_dir, expected_schematic)), "Scematic view is incorrect for " + mainfile
    except FileNotFoundError as not_found:
        if mainfile_name in not_found.filename:
            pytest.fail("Expected Views are not present for" + mainfile)
        else:
            pytest.fail("Views are not generated for " + mainfile)

def verify_negative_test(test_dir, err_msg):
    """
    Verifies test cases which fails
    :param test_dir: Path of the test directory
    :param err_msg: Message to be verified in console output
    """
    # Running test stanza file
    files = [item for item in listdir(test_dir) if item.endswith(STANZA_EXT)]
    if not files:
        pytest.fail("No test stanza file found")
    if platform.system() == "Windows":
        command = "cd " + test_dir+ "\n"+ "jitx run " + files[0]+"\n"
    else:
        command = "cd " + test_dir + " ; jitx run " + files[0]
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen( "cmd.exe", shell=False, universal_newlines=True,
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate(command)
        else:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, check=True)
    except subprocess.CalledProcessError as err:
        if not err_msg in err.output:
            logging.error(err.output)
            pytest.fail("Test case failed with error "+ err.output)

def check_overwrite(test_dir, mainfile):
    """
    Checks the overwrite feature
    :param test_dir: Path of the test directory
    :param mainfile: Name of the stanza file
    """
    filename = test_dir + "/" + mainfile
    file = open(filename, "r")
    text = "`overwrite => true"
    for line in file:
        if text in line:
            if platform.system() == "Windows":
                command_1 = "cd " + test_dir + "\n" + "mkdir output " + "\n"
                command_2 = "cd " + test_dir + "/output " + "\n" + "touch hello.txt" + "\n"
            else:
                command_1 = "cd " + test_dir + " ; mkdir output "
                command_2 = "cd " + test_dir + "/output " + " ; touch hello.txt"
            run_command(command_1)
            run_command(command_2)

def run_and_verify(test_dir):
    """
    Executes the test case steps and verifies the output directory
    :param test_dir: Path of the test directory
    """
    assert isdir(test_dir), "No such directory exists: {}".format(test_dir)
    outdir= get_output_dir(test_dir)

    # Deleting output directory if already exists
    if isdir(outdir) and listdir(outdir):
        shutil.rmtree(outdir)

    # Running test stanza file
    files = [item for item in listdir(test_dir) if item.endswith(STANZA_EXT)]

    check_overwrite(test_dir,files[0])
    if files:
        if platform.system() == "Windows":
            command = "cd " + test_dir + "\n" + "jitx run " + files[0] + "\n"
        else:
            command = "cd " + test_dir + " ; jitx run " + files[0]
        run_command(command)
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
    assert comp_dir(actual_output_dir, expected_output_dir, append_jitx_design = True), "Output directory doesn't match"
    
    if test_dir in ["test-kicad-sch", "test-kicad-lib"]:
        return

    # Get main stanza file name
    mainfiles= get_main_filename(test_dir)
    if not mainfiles:
        pytest.fail("Main stanza file is not generated")

    # Adding ocdb component to stanza.proj file
    try:
        temp = open(join(outdir, "stanza.proj"), "a")
        cmd = ["include \""+OCDB_PATH+"\""]
        temp.writelines(cmd)
        temp.close()
    except Exception as err:
        pytest.fail("Could not find stanza.proj file." + str(err))

    # Verifying views
    error_list= []
    for file in mainfiles:
        try:
            generate_and_verify_views(test_dir, actual_output_dir, file)
            if "bulk" in test_dir:
                if platform.system() == "Windows":
                    expected_design= file.split(".")[0]+ "-win-"+ JITX_DESIGN
                else:
                    expected_design= file.split(".")[0]+ "-"+ JITX_DESIGN
                assert comp_dir(join(actual_output_dir,JITX_DESIGN), \
                    join(test_dir, expected_design)), "Output directory doesn't match for "+file
        except AssertionError as msg:
            logging.error(msg)
            error_list.append(str(msg))
        else:
            logging.info("Test successful for " + file)

    if error_list:
        pytest.fail(", ".join(error_list))
