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


from pymol import cmd, stored, selector
from pymol.cgo import *
from .struts import *  # uses strut selector developed by George Phillips
import sys  # used only in PyMolX11Hybrid
import tkinter.simpledialog  # used only in PyMolX11Hybrid


# def __init__(self):
#    cmd.extend("build_struts", build_struts)
#    cmd.set_key("F2", build_struts)
#    cmd.extend("strut", strut)
#    cmd.set_key("F1", ManualStrutsDialog)


# To create single struts directly, simply select two atoms and press F1.
# Alternatively, in the PyMol command line, type:
#         PyMOL> strut
# By default, either of these will create a white CGO (Compiled Graphic Object) cylinder
# connecting the two atoms, named by the ID # of each atom, separated by a space
#
# To customize atom selection, strut width, or strut color:
#     PyMOL> strut (selection), (radius), (red), (green), (blue)
# Colors are floats: 1.0, 1.0, 1.0 is white; 0.0, 0.0, 0.0 is black

def strut(userSel, radius, r, g, b):
    if(radius == 'stick'):
        radius = cmd.get("stick_radius")
    elif(radius == 'cartoon'):
        radius = cmd.get('cartoon_radius')
    view = cmd.get_view()
    stored.coords = []
    if(cmd.count_atoms(userSel) != 2):
        print("Error! Select exactly 2 atoms to build a strut.")
        return
    cmd.iterate_state(1, selector.process(userSel),
                      "stored.coords.append([x,y,z])")
    strut = [CYLINDER,
             stored.coords[0][0], stored.coords[0][1], stored.coords[0][2],
             stored.coords[1][0], stored.coords[1][1], stored.coords[1][2],
             float(radius), float(r), float(g), float(b), float(r), float(g), float(b)]
    stored.cgoName = ""
    cmd.iterate(userSel, "stored.cgoName = stored.cgoName + str(ID) + \" \"")
    
    cmd.load_cgo(strut, stored.cgoName)
    
    cmd.set_view(view)

def ManualStrutsDialog(app):
    userSel = 'sele'
    radius = tkinter.simpledialog.askstring('Strut Radius',
                                                  'Please enter the desired radius preset for the strut (try stick or cartoon):',
                                                  parent=app.root)
    r = tkinter.simpledialog.askfloat('Strut Color: Red Value',
                                                  'Please enter the Red color value (between 0.0 - 1.0):',
                                                  parent=app.root)
    g = tkinter.simpledialog.askfloat('Strut Color: Green Value',
                                                  'Please enter the Green color value (between 0.0 - 1.0):',
                                                  parent=app.root)
    b = tkinter.simpledialog.askfloat('Strut Color: Blue Value',
                                                  'Please enter the Blue color value (between 0.0 - 1.0):',
                                                  parent=app.root)
    strut(userSel, radius, r, g, b)

cmd.extend("strut", strut)
# cmd.set_key("F1", ManualStrutsDialog)

####default values for printing#####

CARTOON_RECT_WIDTH = 1.5
CARTOON_RECT_LENGTH = 1.5
CARTOON_OVAL_WIDTH = 1
CARTOON_OVAL_LENGTH = 1.5
CARTOON_LOOP_RADIUS = 1
CARTOON_LOOP_CAP = 2

####################################
    

# establishes menu if version is PyMolX11 hybrid, unused otherwise
def buildStrutsDialog(app, type):
    strutLength = tkinter.simpledialog.askinteger('Strut Length',
                                                  'Please enter the maximum length of a strut in Angstroms (try 8):',
                                                  parent=app.root)
    thresh = tkinter.simpledialog.askinteger('Strut Distance',
                                             'Please enter the minimum distance in Angstroms between struts (try 8):',
                                             parent=app.root)
    selection = tkinter.simpledialog.askstring('Scope',
                                               'Please enter a selection (try (all) or (visible)):',
                                               parent=app.root)
    build_struts(type, strutLength, thresh, str(selection))


# Function originally created by Tony Kamenick 2006, modified by Stuart Ballard 2009
# This function creates bond objects between atom pairs identified by
# the struts script (Phillips, Kamenick) to act as struts. To run this script, press F2.
# Alternatively, type:
#     PyMol> build_struts
# By default, this script connects all visible Carbon alphas, separated by a maximum of 8
# angstroms, with a minimum separation of 8 residues along a chain between struts
# To customize these parameters, type:
#     PyMol> build_struts (CA or P--for nucleic acids),
#                         (max strut length), (min strut separation),
#                         (selection to add struts to)
def build_struts(type="CA", strutLength=8, thresh=8, scope="visible"):
    if type == "CA" or type == "P":
        view = cmd.get_view()
        cmd.select("strutted", selector.process(scope))
        pdb = cmd.get_pdbstr(selector.process("strutted")).split("\n")
        cont = True
        try:
            title = cmd.get_names()[0]
        except:
            cont = False
        if cont:
            if type == "CA":
                mon = monitors(pdb, strutLength, thresh, type)
                sts = mon.getStruts()
                if len(sts) == 0:
                    print("ERROR: no struts found")
                    return
                cmd.set("cartoon_rect_width", CARTOON_RECT_WIDTH)
                cmd.set("cartoon_rect_length", CARTOON_RECT_LENGTH)
                cmd.set("cartoon_oval_width", CARTOON_OVAL_WIDTH)
                cmd.set("cartoon_oval_length", CARTOON_OVAL_LENGTH)
                cmd.set("cartoon_loop_radius", CARTOON_LOOP_RADIUS)
                cmd.set("cartoon_loop_cap", CARTOON_LOOP_CAP)
            else:
                mon = monitors(pdb, strutLength, thresh, type)
                sts = mon.getStruts()
                if len(sts) == 0:
                    print("ERROR: no struts found")
                    return
                cmd.set("cartoon_tube_radius", "2")
                cmd.set("cartoon_ladder_radius", "1.4")

            # cmd.hide("all")
            cmd.hide("lines")               # can't print them
            cmd.hide("dots")                # can't print them
            cmd.hide("nonbonded")           # can't print them

            cmd.set("stick_radius", ".8")

            cmd.show("cartoon", selector.process("strutted"))

            # cmd.spectrum()

            cmd.select("struts", selector.process("none"))
            i = 0
            name = type + "struts"
            cmd.create(name, "not *")
            for atom1, atom2 in sts:
                cmd.pseudoatom(
                    "temp"+str(i), pos=[atom1[0], atom1[1], atom1[2]], name="A")
                cmd.pseudoatom(
                    "temp"+str(i), pos=[atom2[0], atom2[1], atom2[2]], name="B")
                str1 = "temp"+str(i)+"////A"
                str2 = "temp"+str(i)+"////B"
                cmd.bond(str1, str2)
            #    cmd.create(name,"///"+str(atom1[4])+"/"+
            #               str(atom1[3])+"/"+type+ " | " + "///"+
            #               str(atom2[4])+"/"+ str(atom2[3])+"/"+type)
            #    cmd.bond("/"+name+"//"+str(atom1[4])+"/"+
            #               str(atom1[3])+"/"+type , "/"+name+"//"+
            #               str(atom2[4])+"/"+str(atom2[3])+"/"+type)

            #    cmd.select("struts", "struts or " + type+"strut"+str(i))
                i += 1
            cmd.hide("everything", name)
            cmd.create(name, "temp*")
            cmd.delete("temp*")
            cmd.show("sticks", name)
            cmd.color("white", name)
            cmd.set_view(view)
    else:
        print("type must be either CA or P")


cmd.extend("build_struts", build_struts)
cmd.set_key("F2", build_struts)
