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
from pymol import cmd

def __init__(self):
    self.menuBar.addmenu('3-D Printer','3-D Printer')
    
    self.menuBar.addmenuitem('3-D Printer', 'command',
                        'Manual Strut Insertion',label='Insert Strut Between Current Selection',
                        command = lambda s=self : ManualStrutsDialog(s))

    self.menuBar.addmenuitem('3-D Printer', 'command',
                      'Build Struts (CA)',
                      label='Build Struts (CA)',
                      command = lambda s = self: buildStrutsDialog(s,'CA'))

    self.menuBar.addmenuitem('3-D Printer', 'command',
                      'Build Struts (P)',
                      label='Build Struts (P)',
                      command = lambda s = self: buildStrutsDialog(s,'P'))

    self.menuBar.addmenuitem('3-D Printer', 'command',
                        'Export VRML',label='Export VRML',
                        command = lambda s=self : _exportVRML(s))
    
    

def _exportVRML(app):
    file = tkinter.filedialog.asksaveasfilename(filetypes=[('VRML 2 WRL File','*.wrl')])
    if len(file) > 0:
        cmd.save(file)
        print ("file exported as "+file)


