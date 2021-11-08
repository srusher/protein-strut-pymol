################################################################################
# File          : 3DPrintMenu.py
# Author        : Tony Kamenick
# Date          : 6/6/06 
# 
# Description   : Adds a 3-D printer menu to the PyMOL tcl/tk GUI window. It
#                 contains options to create struts and export VRML files
###############################################################################


from .build_struts import *
from .increment_coords import *
from .strut_finder import *
from pymol import *
import os

#sets mouse selection mode to 'Atoms'
cmd.set('mouse_selection_mode','0')

def __init__(self):
    self.menuBar.addmenu('Strut Insertion','Strut Insertion')
    
    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Insert Struts: User Selection',label='Insert Struts: User Selection',
                        command = lambda : insert_user_select_struts())

    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Automated Strut Insertion',label='Automated Strut Insertion',
                        command = lambda : main_strut())

    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Strut Modification',label='Strut Modification',
                        command = lambda : XYZ_increment())

    self.menuBar.addmenuitem('Strut Insertion', 'command',
                        'Verfiy DSSP Install/Update',label='Verify DSSP Install/Update',
                        command = lambda : update_dssp())

def update_dssp():
    os.system("conda install -c schrodinger pymol-psico")



