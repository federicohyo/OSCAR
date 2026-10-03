#!/usr/bin/python3
from builtins import FileNotFoundError, len, open, print
import sys
import os
import json
import subprocess
import shutil
import re

# Function to check if the folder exist
def does_folder_exist(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        sys.exit(1)

# Function to check if the file exist in folder
def does_file_exist(folder_path, filename):
    if filename not in os.listdir(folder_path):
        print(f"Error: The file '{filename}' does not exist in the '{folder_path}' folder.")
        sys.exit(1)

# Function to load configuration from JSON file
def load_config(configname):
    try:
        with open(configname, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{configname}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in configuration file '{filename}'.")
        sys.exit(1)

#Define Transistor
class Transistor:
    def __init__(self, name, W, L, nf,mult, transistor_type):
        self.name = name
        self.W = W
        self.L = L
        self.nf = nf
        self.mult = mult
        self.transistor_type = transistor_type

    def __repr__(self):
        return f"Transistor(name={self.name}, W={self.W}, L={self.L}, nf={self.nf}, mult={self.mult}, type={self.transistor_type})"
    
#Define Capacitor
class Capacitor:
    def __init__(self, name, W, L, capacitor_type):
        self.name = name
        self.W = W
        self.L = L
        self.capacitor_type = capacitor_type

    def __repr__(self):
        return f"Capacitor(name={self.name}, W={self.W}, L={self.L}, type={self.capacitor_type})"

#Define modules
class Module:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Module(name={self.name})"

#function that extracts transistor components from file
def extract_components_from_file(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        text = file.read()

    # Exclude lines after *expanding keyword           #PLEASE CHANGE THIS IF YOU WANT TO IMPORT MULTIPLE MODULES
    text = text.split('* expanding')[0]

    # Regex pattern to match the transistor, capacitor lines, and module lines
    transistor_pattern = re.compile(r'(XM\d+)\s.*?sky130_fd_pr__(nfet_01v8|pfet_01v8)\s+L=([\d.]+)\s+W=([\d.]+)\s+nf=([\d.]+)\s+m=([\d.]+)')
    capacitor_pattern = re.compile(r'(XC\d+)\s.*?sky130_fd_pr__(cap_mim_m3_1|cap_mim_m3_2)\s+W=([\d.]+)\sL=([\d.]+)')
    module_pattern = re.compile(r'(x\d+\[?\d*]?)\s.*?\s(\S+)$', re.MULTILINE)

    # Find all matches in the text
    transistor_matches = transistor_pattern.findall(text)
    capacitor_matches = capacitor_pattern.findall(text)
    module_matches = module_pattern.findall(text)

    # Create Transistor, Capacitor, and Module objects from the matchess
    transistors = [Transistor(name, float(W), float(L), float(nf), float(mult), t_type) for name, t_type, L, W, nf, mult in transistor_matches]
    capacitors = [Capacitor(name, float(W), float(L), c_type) for name, c_type, W, L in capacitor_matches]
    modules = [Module(name) for _, name in module_matches]

    return transistors, capacitors, modules


# Load configuration from config.json
config = load_config('config.json')
magicpath = config["magicpath"]
xschempath = config["xschempath"]
netlistpath = config["netlistpath"]
scriptpath = config["scriptpath"]

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 layout.py <filename>")
    sys.exit(1)

# Capture the variables from the command line arguments
filename = sys.argv[1]
magicname = filename  + ".mag"
xschemname = filename + ".sch"
spicename = filename + ".spice"

# Check if the filename contains a dot (.)
if filename.count(".") != 0:
    print(f"Error: The filename '{filename}' should not contain a dot (.)")
    sys.exit(1)

# Check if the folder "magic" exists
does_folder_exist(magicpath)
# Check if the folder "xschem" exists
does_folder_exist(xschempath)
# Check if the folder "netlist" exists
does_folder_exist(netlistpath)
# Check if the magic file exists in the "mag" folder
if magicname in os.listdir(magicpath):
       print(f"Error: The file '{filename}' already exists in '{magicpath}' folder.")
       sys.exit(1)
# Check if the xschem file exists in the "xschem" folder
does_file_exist(xschempath, xschemname)
# Check if the spice file exists in the "netlist" folder
does_file_exist(netlistpath, spicename)

# Extract transistors, capacitors, and modules
spicefile = os.path.join(netlistpath, spicename)
transistors, capacitors, modules = extract_components_from_file(spicefile)

# Print the extracted components
print("\nTransistors:")
for transistor in transistors:
    print(transistor)

print("\nCapacitors:")
for capacitor in capacitors:
    print(capacitor)

print("\nModules:")
for module in modules:
    print(module)

def generate_magic_script(transistors, capacitors, modules, script_file):
    nfets = [t for t in transistors if t.transistor_type == 'nfet_01v8']
    pfets = [t for t in transistors if t.transistor_type == 'pfet_01v8']
    cap3s = [c for c in capacitors if c.capacitor_type == 'cap_mim_m3_1']
    cap4s = [c for c in capacitors if c.capacitor_type == 'cap_mim_m3_2']

    # Calculate maximum L for each type of component
    max_L_nfet = max((t.L for t in nfets), default=0)
    max_L_pfet = max((t.L for t in pfets), default=0)
    max_L_cap3 = max((c.L for c in cap3s), default=0)
    max_L_cap4 = max((c.L for c in cap4s), default=0)

    # Define settings
    ymargin = 1.0
    xmargin = 1.0
    polyextend = 0.13
    polyextendconnectn = 0.11
    polyextendconnectp = 0.16
    polyconnectmargin = 0.08
    polyheight = 0.33
    wellextend = 0.29
    wellconnectmargin = 0.06
    liextend = 0.02
    nwellextend = 0.18
    mimcapmargin = 0.14
    powermetal1h = 0.48
    powermetal1w = 0.46
    powermetalli = 0.155
    powerliedge = 0.145
    mcondimension = 0.17
    standardcellheight = 2.24


    # Calculate row positions
    x_positions = {
        'stndrail': 0,
        'analograil': xmargin,
        'nfet': 2 * xmargin,
        'pfet': max_L_nfet + 3 * xmargin,
        'cap3': max_L_nfet + max_L_pfet + 4 * xmargin,
        'cap4': max_L_nfet + max_L_pfet + max_L_cap3 + 5 * xmargin,
        'module': max_L_nfet + max_L_pfet + max_L_cap3 + max_L_cap4 + 6 * xmargin
    }

    with open(script_file, 'w') as file:
        file.write("# Generated Magic TCL script\n")
        file.write("grid 5nm 5nm\n")
        file.write("setlabel -default font FreeSans\n")
        file.write("setlabel -default size 200nm\n")
        file.write("snap user\n")
        
        # Generate nfet layouts in the first row
        y_offset = 0
        for nfet in nfets:
            if nfet.mult != 1:
                input(f"The transitor {nfet.name} has a mult different to 1. This script does not yet support that. Press Enter to continue...")
            if nfet.nf != 1:
                input(f"The transitor {nfet.name} has nf different to 1. This script does not yet support that. Press Enter to continue...")
            # Calculate polyextend based on nfet.L
            if nfet.L < 0.33:
                polyoverextend = (0.33 - nfet.L) / 2
                polywidth = 0.33
            else:
                polyoverextend = 0
                polywidth = nfet.L
            #start layout
            file.write(f"box {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um\n")
            file.write(f"label {nfet.name} w\n")
            file.write(f"box {x_positions['nfet']:.2f}um {y_offset:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend:.2f}um {y_offset + nfet.W:.2f}um\n")
            file.write(f"paint ndiff\n")
            file.write(f"box {x_positions['nfet'] + wellextend:.2f}um {y_offset-polyextend:.2f}um {x_positions['nfet'] + nfet.L + wellextend:.2f}um {y_offset + nfet.W + polyextend:.2f}um\n")
            file.write(f"paint poly\n")
            file.write(f"box {x_positions['nfet'] + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
            file.write(f"paint ndiffc\n")
            file.write(f"box {x_positions['nfet'] + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W +liextend:.2f}um\n")
            file.write(f"paint li\n")
            file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
            file.write(f"paint ndiffc\n")
            file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W + liextend:.2f}um\n")
            file.write(f"paint li\n")
            file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight:.2f}um\n")
            file.write(f"paint poly\n")
            file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend + polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth- polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
            file.write(f"paint pc\n")
            file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
            file.write(f"paint li\n")
            y_offset += nfet.W + ymargin

#multple finger not yet implemented and not yet correct!!!!

#        for nfet in nfets:
#            # Calculate polyextend based on nfet.L
#            if nfet.L < 0.33:
#                polyoverextend = (0.33 - nfet.L) / 2
#                polywidth = 0.33
#            else:
#                polyoverextend = 0
#                polywidth = nfet.L
#            
#                if nfet.nf == 1:
#                    #start layout
#                    file.write(f"box {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um\n")
#                    file.write(f"label {nfet.name} w\n")
####                    file.write(f"box {x_positions['nfet']:.2f}um {y_offset:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend:.2f}um {y_offset + nfet.W:.2f}um\n")
#                    file.write(f"paint ndiff\n")
#                    file.write(f"box {x_positions['nfet'] + wellextend:.2f}um {y_offset-polyextend:.2f}um {x_positions['nfet'] + nfet.L + wellextend:.2f}um {y_offset + nfet.W + polyextend:.2f}um\n")
#                    file.write(f"paint poly\n")
#                    file.write(f"box {x_positions['nfet'] + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
##                    file.write(f"paint ndiffc\n")
#                    file.write(f"box {x_positions['nfet'] + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W +liextend:.2f}um\n")
###                    file.write(f"paint li\n")
#                    file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
#                    file.write(f"paint ndiffc\n")
#                    file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W + liextend:.2f}um\n")
##                    file.write(f"paint li\n")
#                    file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight:.2f}um\n")
#                    file.write(f"paint poly\n")
#                    file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend + polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth- polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
#                    file.write(f"paint pc\n")
#                    file.write(f"box {x_positions['nfet'] + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
#                    file.write(f"paint li\n")
#                else:
#                    Lengthbetweenfingers = nfet.L / nfet.nf
#                    Length = Lengthbetweenfingers
#                    file.write(f"box {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um {x_positions['nfet']-0.2:.2f}um {y_offset:.2f}um\n")
#                    file.write(f"label {nfet.name} w\n")
#                    while Length < nfet.L:
#                        file.write(f"box {x_positions['nfet'] + Length - 2:.2f}um {y_offset:.2f}um {x_positions['nfet'] + Length + 2 * wellextend:.2f}um {y_offset + nfet.W:.2f}um\n")
#                        file.write(f"paint ndiff\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2 + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + Length - 2 + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
#                        file.write(f"paint ndiffc\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2 + wellextend:.2f}um {y_offset-polyextend:.2f}um {x_positions['nfet'] +  + Length - 2  + wellextend:.2f}um {y_offset + nfet.W + polyextend:.2f}um\n")
#                        file.write(f"paint poly\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2 + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + Length - 2  + wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W +liextend:.2f}um\n")
#                        file.write(f"paint li\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn:.2f}um {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight:.2f}um\n")
#                        file.write(f"paint poly\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend + polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend +polywidth- polyconnectmargin:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
#                        file.write(f"paint pc\n")
#                        file.write(f"box {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend:.2f}um {y_offset + nfet.W + polyextendconnectn+ polyconnectmargin:.2f}um {x_positions['nfet'] + Length - 2  + wellextend - polyoverextend +polywidth:.2f}um {y_offset + nfet.W + polyextendconnectn+polyheight- polyconnectmargin:.2f}um\n")
#                        file.write(f"paint li\n")
#
#                        Length + Lengthbetweenfingers
#                    file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W - wellconnectmargin:.2f}um\n")
#                    file.write(f"paint ndiffc\n")
#                    file.write(f"box {x_positions['nfet'] + nfet.L + wellextend + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['nfet'] + nfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + nfet.W + liextend:.2f}um\n")
#                    file.write(f"paint li\n")
#

        # Generate pfet layouts in the second row
        y_offset = 0
        for pfet in pfets:
            if pfet.mult != 1:
                input(f"The transitor {pfet.name} has a mult different to 1. This script does not yet support that. Press Enter to continue...")
            if pfet.nf != 1:
                input(f"The transitor {pfet.name} has nf different to 1. This script does not yet support that. Press Enter to continue...")
            # Calculate polyextend based on pfet.L
            if pfet.L < 0.33:
                polyoverextend = (0.33 - pfet.L) / 2
                polywidth = 0.33
            else:
                polyoverextend = 0
                polywidth = pfet.L
            #start layout
            file.write(f"box {x_positions['pfet']-0.2:.2f}um {y_offset:.2f}um {x_positions['pfet']-0.2:.2f}um {y_offset:.2f}um\n")
            file.write(f"label {pfet.name} w\n")
            file.write(f"box {x_positions['pfet']:.2f}um {y_offset:.2f}um {x_positions['pfet'] + pfet.L + 2 * wellextend:.2f}um {y_offset + pfet.W:.2f}um\n")
            file.write(f"paint pdiff\n")
            file.write(f"box {x_positions['pfet'] + wellextend:.2f}um {y_offset-polyextend:.2f}um {x_positions['pfet'] + pfet.L + wellextend:.2f}um {y_offset + pfet.W + polyextend:.2f}um\n")
            file.write(f"paint poly\n")
            file.write(f"box {x_positions['pfet'] + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['pfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + pfet.W - wellconnectmargin:.2f}um\n")
            file.write(f"paint pdiffc\n")
            file.write(f"box {x_positions['pfet'] + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['pfet'] + wellextend - wellconnectmargin:.2f}um {y_offset + pfet.W +liextend:.2f}um\n")
            file.write(f"paint li\n")
            file.write(f"box {x_positions['pfet'] + pfet.L + wellextend + wellconnectmargin:.2f}um {y_offset + wellconnectmargin:.2f}um {x_positions['pfet'] + pfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + pfet.W - wellconnectmargin:.2f}um\n")
            file.write(f"paint pdiffc\n")
            file.write(f"box {x_positions['pfet'] + pfet.L + wellextend + wellconnectmargin:.2f}um {y_offset - liextend:.2f}um {x_positions['pfet'] + pfet.L + 2 * wellextend - wellconnectmargin:.2f}um {y_offset + pfet.W + liextend:.2f}um\n")
            file.write(f"paint li\n")
            file.write(f"box {x_positions['pfet'] + wellextend - polyoverextend:.2f}um {y_offset + pfet.W + polyextend:.2f}um {x_positions['pfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + pfet.W + polyextend+polyheight:.2f}um\n")
            file.write(f"paint poly\n")
            file.write(f"box {x_positions['pfet'] + wellextend - polyoverextend + polyconnectmargin:.2f}um {y_offset + pfet.W + polyextendconnectp+ polyconnectmargin:.2f}um {x_positions['pfet'] + wellextend - polyoverextend +polywidth- polyconnectmargin:.2f}um {y_offset + pfet.W + polyextendconnectp+polyheight- polyconnectmargin:.2f}um\n")
            file.write(f"paint pc\n")
            file.write(f"box {x_positions['pfet'] + wellextend - polyoverextend:.2f}um {y_offset + pfet.W + polyextendconnectp+ polyconnectmargin:.2f}um {x_positions['pfet'] + wellextend - polyoverextend +polywidth:.2f}um {y_offset + pfet.W + polyextendconnectp+polyheight- polyconnectmargin:.2f}um\n")
            file.write(f"paint li\n")
            file.write(f"box {x_positions['pfet'] + -nwellextend:.2f}um {y_offset + -nwellextend:.2f}um {x_positions['pfet'] + pfet.L + 2* wellextend + nwellextend:.2f}um {y_offset + pfet.W +nwellextend:.2f}um\n")
            file.write(f"paint nwell\n")
            y_offset += pfet.W + ymargin

        # Generate capacitor3 layouts in the third row
        y_offset = 0
        for cap3 in cap3s:
            #start layout
            file.write(f"box {x_positions['cap3']-0.2:.2f}um {y_offset:.2f}um {x_positions['cap3']-0.2:.2f}um {y_offset:.2f}um\n")
            file.write(f"label {cap3.name} w\n")
            file.write(f"box {x_positions['cap3']:.2f}um {y_offset:.2f}um {x_positions['cap3'] + cap3.L:.2f}um {y_offset + cap3.W:.2f}um\n")
            file.write(f"paint mimcap\n")
            file.write(f"box {x_positions['cap3']-mimcapmargin:.2f}um {y_offset-mimcapmargin:.2f}um {x_positions['cap3'] + cap3.L+mimcapmargin:.2f}um {y_offset + cap3.W+mimcapmargin:.2f}um\n")
            file.write(f"paint m3\n")
            file.write(f"box {x_positions['cap3']+2*mimcapmargin:.2f}um {y_offset+2*mimcapmargin:.2f}um {x_positions['cap3'] + cap3.L-2*mimcapmargin:.2f}um {y_offset + cap3.W-2*mimcapmargin:.2f}um\n")
            file.write(f"paint mimcapc\n")
            file.write(f"box {x_positions['cap3']+mimcapmargin:.2f}um {y_offset+mimcapmargin:.2f}um {x_positions['cap3'] + cap3.L-mimcapmargin:.2f}um {y_offset + cap3.W-mimcapmargin:.2f}um\n")
            file.write(f"paint m4\n")
            y_offset += cap3.W + ymargin

        # Generate capacitor4 layouts in the third row 
        y_offset = 0
        for cap4 in cap4s:
            #start layout
            file.write(f"box {x_positions['cap4']-0.2:.2f}um {y_offset:.2f}um {x_positions['cap4']-0.2:.2f}um {y_offset:.2f}um\n")
            file.write(f"label {cap4.name} w\n")
            file.write(f"box {x_positions['cap4']:.2f}um {y_offset:.2f}um {x_positions['cap4'] + cap4.L:.2f}um {y_offset + cap4.W:.2f}um\n")
            file.write(f"paint mimcap2\n")
            file.write(f"box {x_positions['cap4']-mimcapmargin:.2f}um {y_offset-mimcapmargin:.2f}um {x_positions['cap4'] + cap4.L+mimcapmargin:.2f}um {y_offset + cap4.W+mimcapmargin:.2f}um\n")
            file.write(f"paint m4\n")
            file.write(f"box {x_positions['cap4']+2*mimcapmargin:.2f}um {y_offset+2*mimcapmargin:.2f}um {x_positions['cap4'] + cap4.L-2*mimcapmargin:.2f}um {y_offset + cap4.W-2*mimcapmargin:.2f}um\n")
            file.write(f"paint mimcap2c\n")
            file.write(f"box {x_positions['cap4']+mimcapmargin:.2f}um {y_offset+mimcapmargin:.2f}um {x_positions['cap4'] + cap4.L-mimcapmargin:.2f}um {y_offset + cap4.W-mimcapmargin:.2f}um\n")
            file.write(f"paint m5\n")
            y_offset += cap4.W + ymargin
        
        # Add submodules
        y_offset = 0
        for module in modules:
            #start layout
            file.write(f"box {x_positions['module']:.2f}um {y_offset:.2f}um {x_positions['module']:.2f}um {y_offset:.2f}um\n")
            file.write(f"getcell {module.name}\n")
            y_offset += y_offset+ ymargin
        
        # Add DIGITAL Power and ground rails
        y_offset = 0
        #start layout
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['stndrail']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        y_offset = y_offset + powermetal1h + standardcellheight
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['stndrail']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        y_offset = y_offset + powermetal1h + standardcellheight
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['stndrail']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['stndrail']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['stndrail']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")

        # Add DIGITAL Power and ground rails
        y_offset = 0
        #start layout
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label stndcell w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        y_offset = y_offset + 2*powermetal1h
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label GNDtap w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint ptap\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint ptapc\n")
        y_offset = y_offset + 3.12
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label sout w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        y_offset = y_offset + 3.12
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label vdd w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        y_offset = y_offset + 2*powermetal1h
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label GNDtap w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint ptap\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint ptapc\n")
        y_offset = y_offset + 1.76
        file.write(f"box {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um {x_positions['analograil']-0.2:.2f}um {y_offset:.2f}um\n")
        file.write(f"label stndcell w\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetal1h:.3f}um\n")
        file.write(f"paint m1\n")
        file.write(f"box {x_positions['analograil']:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powermetal1w:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint li\n")
        file.write(f"box {x_positions['analograil']+powerliedge:.3f}um {y_offset+powermetalli:.3f}um {x_positions['analograil']+powerliedge+mcondimension:.3f}um {y_offset+powermetalli+mcondimension:.3f}um\n")
        file.write(f"paint mcon\n")
        
        file.write(f"save {magicname}\n")

# Generate Magic TCL script
scriptname = 'generate_layout.tcl'
scriptfile = os.path.join(scriptpath, scriptname)
generate_magic_script(transistors, capacitors,modules, scriptname)
magic_command = f"""magic -dnull -noconsole -rcfile .magicrc << EOF
#source {scriptfile}
source ../script/generate_layout.tcl
"""
try:
    with open(os.devnull, 'w') as devnull:
        subprocess.run(magic_command, shell=True, check=True, cwd=magicpath, stdout=devnull, stderr=devnull)
except subprocess.CalledProcessError as e:
    print(f"Error while running Magic: {e}")
finally:
    # Delete the Tcl script
    print("Deleting Tcl script...")
    if os.path.exists(scriptfile):
        os.remove(scriptfile)

print("Magic layout process completed successfully.")
print(f"Magic script saved to {scriptfile}")
