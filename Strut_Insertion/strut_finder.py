#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 22:09:38 2021
@author: nd
@author: Sam Rusher
"""

import os
import sys
from pymol import cmd
from .sec_strut import *

# this will assign a different path depending on if it is a Windows or Linux OS
if platform.system() == "Windows":
    pdb_dir_path = os.path.dirname(os.path.realpath(__file__)) + '\pdb_files\\'
else:
    pdb_dir_path = os.path.dirname(os.path.realpath(__file__)) +'/pdb_files/'

cmd.set('fetch_type_default','pdb')
cmd.set('fetch_path', cmd.exp_path(pdb_dir_path), quiet=0)

## define global variables
dssp_out = "dssp_output.txt"
command = "mkdssp"

def main_strut():
    original_workdir = os.getcwd()  
    os.chdir(pdb_dir_path)

    for obj in cmd.get_object_list():
        if 'strut' not in str(obj).lower():
            os.system(f'pymol dssp {str(obj)}')
            molecule = str(obj)+'.pdb'
            cmd.save(molecule,str(obj))
            cmd.rebuild()
            #cmd.delete(obj)
            #new_path = pdb_dir_path + str(obj) + '.pdb'
            #cmd.load(new_path)

            #pdb_file_path = pdb_dir_path + molecule
            print(f'{command} --output-format=dssp -i {molecule} -o {dssp_out}')
            os.system(f'{command} -i {molecule} -o {dssp_out}')
            print('command 1')
            main_sec_strut(dssp_out)
            print('command 2')
            #cmd.fetch(molecule,str(obj))
    
    os.chdir(original_workdir)
    #os.system("python3 loop_bridge.py " + "loop_output.txt")