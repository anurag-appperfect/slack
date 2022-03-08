EESchema Schematic File Version 4
EELAYER 25 0
EELAYER END
$Descr E 44016.0 34016.0
encoding utf-8
Sheet 1 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L project_symbols:component U2
U 1 1 00000000
P 1150 32950
F 0 "U2" H 1150 33009 30 0 C CNN
F 1 "" H 1150 32950 60 1 C CNN
F 2 "jitx-design:basic_landpattern" H 1150 32950 60 1 C CNN
F 3 "" H 1150 32950 60 1 C CNN
  1 1150 32950
  0 -1 -1 0
$EndComp
$Comp
L project_symbols:component U1
U 1 1 00000000
P 900 32900
F 0 "U1" H 900 32959 30 0 C CNN
F 1 "" H 900 32900 60 1 C CNN
F 2 "jitx-design:basic_landpattern" H 900 32900 60 1 C CNN
F 3 "" H 900 32900 60 1 C CNN
  1 900 32900
  0 -1 -1 0
$EndComp
Wire Wire Line
  900 33050 900 33100
Wire Wire Line
  900 32750 900 32700
Wire Wire Line
  1150 33100 1150 33150
Wire Wire Line
  1150 32800 1150 32750
Wire Wire Line
  900 33250 1150 33250
Wire Wire Line
  900 33250 900 33100
Wire Wire Line
  1150 33250 1150 33150
Wire Wire Line
  900 32550 1150 32550
Wire Wire Line
  1150 32750 1150 32550
Wire Wire Line
  900 32700 900 32550
Text Label 900 33100 3 40 ~
gnd
Text Label 900 32700 1 40 ~
vdd
$EndSCHEMATC