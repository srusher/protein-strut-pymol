###############################################################################
# Author  : George Phillips
# Original Author of build_struts: Tony Kamenick, 2006
# Email   : georgep@rice.edu
# Program : build_struts.py
# Version : 0.3
# Copyright 2014
###############################################################################
# Author  : Stuart Ballard
# Original Author of build_struts: Tony Kamenick, 2006
# Email   : srballard@wisc.edu
# Program : strutbuilder.py
# Version : 0.2
# Copyright 2009
#
################################################################################
#
#   original author = george phillips
#   email  = phillips@biochem.wisc.edu
#   ported to python / bug-fixed by tony kamenick 4/06
#   program_name = build_struts.py
#   copyright reserved, 2005-2006
#
################################################################################


# To load this script, enter the following in PyMol:
# PyMOL> run [*file*path*]/strutbuilder.py


from pymol import cmd, stored, selector, menu
from pymol.cgo import *


# set_i_global keeps track of the 'index' of the struts and will increment it by 1 based off of the last strut
## this is not a real 'index' just a number to help the user keep better track of the struts when editing
def set_i_global(app):

    object_list = [""]
    for obj in cmd.get_object_list():
        count = 0
        i = 0
        index = 0
        for char in str(obj):
            if char == '_':
                count = count + 1
                if count == 1:
                    index = i
            i = i + 1
        if count == 2:
            object_list.append(obj[:index])
        
    if len(object_list) == 1:
        print("STILL ON IF")
        i_global = 0
    else:
        print('MADE IT TO ELSE')
        i_global = str(int(object_list[-1]) + 1)
    
    user_select_struts('sele', i_global)

# user_select_struts will insert a strut in-between the 2 atoms the user has selected in the PyMol Viewer window
def user_select_struts(userSel, i):
    view = cmd.get_view()
    coordinate_pairs = []
    stored.coords = []
    if(cmd.count_atoms(userSel) != 2):
        print("Error! Select exactly 2 atoms to build a strut.")
        return
    cmd.iterate_state(1, selector.process(userSel),
                      "stored.coords.append([x,y,z,ID])")
    coordinate_pairs.append(stored.coords)
    name = ""
    # cmd.create(name, "not *")

    # this doesn't need to be in a for loop, but will easily translate to large lists of atom pairs
    for atom1, atom2 in coordinate_pairs:
        cmd.pseudoatom("temp"+str(i), pos=[atom1[0], atom1[1], atom1[2]], name="A")
        cmd.pseudoatom("temp"+str(i), pos=[atom2[0], atom2[1], atom2[2]], name="B")
        str1 = "temp"+str(i)+"////A"
        str2 = "temp"+str(i)+"////B"
        name = str(i) + "_" + str(atom1[3]) + "_" + str(atom2[3])
        cmd.bond(str1, str2)
        cmd.create(name, "temp*")
        cmd.hide("everything", name)
        cmd.delete("temp*")
        cmd.show("sticks", name)
        cmd.color("white", name)

    cmd.set_view(view)