#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 22:09:38 2021

@author: nd
"""

#import scripts

#import libraries/modules
import os
import sys

## define global variables
## may need to change command depending on dssp configuration
file_pdb = sys.argv[1]
#file_pdb = "6xmy.pdb"
dssp_out = "dssp_output.txt"
command = "mkdssp --output-format=dssp "

def main():
    os.system(command + file_pdb + " > " + dssp_out)
    os.system("python3 sec_strut.py " + dssp_out)
    #os.system("python3 loop_bridge.py " + "loop_output.txt")

main()