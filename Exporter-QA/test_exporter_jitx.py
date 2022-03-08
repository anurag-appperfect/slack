"""This file contains the Exporter QA test cases"""
import pytest
import test_utility

# Methods to execute the Exporter QA test cases
def test_export_altium():
    test_utility.run_and_verify("export-altium")

def test_export_altium_set_design():
    test_utility.run_and_verify("export-altium-set-design")

def test_export_altium_set_paper_a4():
    test_utility.run_and_verify("export-altium-set-paper-A4")

def test_export_altium_set_paper_b():
    test_utility.run_and_verify("export-altium-set-paper-B")

def test_export_altium_set_paper_e():
    test_utility.run_and_verify("export-altium-set-paper-E")

def test_export_board():
    test_utility.run_and_verify("export-board")

def test_export_schematic():
    test_utility.run_and_verify("export-schematic")

def test_export_neither_board_nor_schematic():
    test_utility.run_and_verify("export-neither-board")

def test_export_kicad():
    test_utility.run_and_verify("export-kicad")

def test_export_kicad_net_class():
    test_utility.run_and_verify("export-net-class")

def test_export_net_class_routing():
    test_utility.run_and_verify("export-net-class-routing")

def test_export_net_class_vias():
    test_utility.run_and_verify("export-net-class-vias")

def test_export_kicad_set_design():
    test_utility.run_and_verify("export-set-design")

def test_export_kicad_set_paper_ansi_a4():
    test_utility.run_and_verify("export-set-paper-A4")

def test_export_kicad_set_paper_ansi_b():
    test_utility.run_and_verify("export-set-paper-B")

def test_export_kicad_set_paper_ansi_e():
    test_utility.run_and_verify("export-set-paper-E")
