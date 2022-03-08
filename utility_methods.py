"""This file contains the utility methods required for executing the test cases"""
from os.path import isdir, join
from os import walk
import filecmp
import subprocess
import pytest
import platform
import re

def comp_dir(dir1, dir2, append_jitx_design = False):
    """
    Compares the contents of two directories
    :param dir1: Path of a directory
    :param dir2: Path of a directory
    :param append_jitx_design: True to add jitx-design in list of empty directories 
    :return: True if the contents of the directories are same else False
    """
    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore = get_empty_directories(dir1, append_jitx_design))
    if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or \
        len(dirs_cmp.funny_files)>0:
        return False
    (_, mismatch, errors) =  filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch)>0 or len(errors)>0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        sub_dir1 = join(dir1, common_dir)
        sub_dir2 = join(dir2, common_dir)
        if not comp_dir(sub_dir1, sub_dir2):
            return False
    return True

def run_stanza_file(directory, file):
    """
    Runs the given stanza file
    :param directory: Path of the directory containing the stanza file
    :param file: Name of the stanza file
    """
    if platform.system() == "Windows":
        command = "cd " + directory + "\n" + "jitx run " + file + "\n"
        try: 
            process = subprocess.Popen( "cmd.exe", shell=False, universal_newlines=True,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )                             
            out, err = process.communicate(command) 
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(err.cmd, err.returncode, err.output))
    else:
        command = "cd " + directory + " ; jitx run " + file
        try:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, check=True)
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(
                err.cmd, err.returncode, err.output))

def get_output_dir(test_dir):
    """
    Returns the output directory
    :param test_dir: Path of the test directory
    :return: Path of the output directory
    """
    if isdir(join(test_dir,"jitx-design")):
        return join(test_dir,"jitx-design")
    elif isdir(join(test_dir,"custom-design")):
        return join(test_dir,"custom-design")
    else:
        return join(test_dir,"output")

def get_current_jitx_version():
    """
    Returns the current jitx version
    :return: Current jitx version eg: 0.11.5-rc.2
    """
    if platform.system() == "Windows":
        command = "jitx check-install" + "\n"
        try: 
            process = subprocess.Popen( "cmd.exe", shell=False, universal_newlines=True,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )                             
            out, err = process.communicate(command)
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(err.cmd, err.returncode, err.output))
    else:
        command = "jitx check-install"
        try:
            test_case = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, check=True)
            out = test_case.stdout
        except subprocess.CalledProcessError as err:
            pytest.fail("command '{}' return with error (code {}): {}".format(
                err.cmd, err.returncode, err.output))

    version = re.search(r'(?<=version: ).*', out)
    return version.group()

def get_empty_directories(directory, append_jitx_design):
    """
    Returns a list of empty directories
    :param directory: Name of a directory
    :param append_jitx_design: True to add jitx-design in list of empty directories
    :return: List of names of empty directories
    """
    empty_dirs = []
    # Traversing through directory
    for root, dirs, files in walk(directory):
        # Checking the size of tuple
        if not len(dirs) and not len(files):    
            # Adding the empty directory to list
            if platform.system() == "Windows":
                empty_dirs.append(root.split('\\')[-1])
            else:
                empty_dirs.append(root.split('/')[-1])              
    
    # Add jitx design in empty directories
    if append_jitx_design is True:
        empty_dirs.append('jitx-design')
    return empty_dirs
