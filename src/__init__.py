################################################################################
# File          : 3DPrintMenu.py
# Author        : Tony Kamenick
# Date          : 6/6/06 
# 
# Description   : Adds a 3-D printer menu to the PyMOL tcl/tk GUI window. It
#                 contains options to create struts and export VRML files
###############################################################################

from .build_struts import *
import tkinter.filedialog
from tkinter import *
from .increment_coords import *
from pymol import cmd

def __init__(self):
    self.menuBar.addmenu('Strut Insertion','Strut Insertion')
    
    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Insert Struts: User Selection',label='Insert Struts: User Selection',
                        command = lambda s=self : set_i_global(s))

    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Strut Endpoint Adjustment',label='Strut Endpoint Adjustment',
                        command = lambda s=self : XYZ_increment())



def _exportVRML(app):
    file = tkinter.filedialog.asksaveasfilename(filetypes=[('VRML 2 WRL File','*.wrl')])
    if len(file) > 0:
        cmd.save(file)
        print ("file exported as "+file)