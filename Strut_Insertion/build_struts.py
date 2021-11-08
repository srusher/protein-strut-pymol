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

import platform
import sys
import os
from pymol import cmd, stored, selector, menu
from pymol.cgo import *
import math


# set_i_global keeps track of the 'index' of the struts and will increment it by 1 based off of the last strut
## this is not a real 'index' just a number to help the user keep better track of the struts when editing
def set_i_global():

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
        if ('strut' in str(obj).lower()):
            object_list.append(obj[:index])
        
    if len(object_list) == 1:
        i_global = 1
    else:
        i_global = str(int(object_list[-1]) + 1)
    
    return i_global


# user_select_struts will insert a strut in-between the 2 atoms the user has selected in the PyMol Viewer window
def insert_user_select_struts():
    
    i_global = set_i_global()
    userSel = 'sele'
    view = cmd.get_view()
    coordinate_pairs = []
    stored.coords = []
    if(cmd.count_atoms(userSel) != 2):
        print("Error! Select exactly 2 atoms to build a strut.")
        return
    cmd.iterate_state(1, 'sele',
                      "stored.coords.append([x,y,z,ID])")
    coordinate_pairs.append(stored.coords)
    name = ""

    for atom1, atom2 in coordinate_pairs:
        cmd.pseudoatom("temp"+str(i_global), pos=[atom1[0], atom1[1], atom1[2]], name="A")
        cmd.pseudoatom("temp"+str(i_global), pos=[atom2[0], atom2[1], atom2[2]], name="B")
        str1 = "temp"+str(i_global)+"////A"
        str2 = "temp"+str(i_global)+"////B"
        cmd.bond(str1, str2)
        name = str(i_global) + "_userStrut_" + str(atom1[3]) + "_" + str(atom2[3])
        cmd.create(name, "temp*")
        cmd.hide("everything", name)
        cmd.delete("temp*")
        cmd.set('stick_radius', float(0.5) , name)
        cmd.show("sticks", name)
        cmd.color("white", name)

    cmd.set_view(view)

    print("User Select strutting completed.")
    return

#Refine and structurally support Secondary Structures
def secondary_struts(alphas, betas):
    i_global = set_i_global()
    #Alpha Supports
    alpha_list = alphas
    
    count = 1

    #Parse list and change secondary structure designations
    print('Reassigning alpha helix atoms based on DSSP output...')
    for i in alpha_list:
        y=-1
        #iterate through sub-list to find length
        for j in i:
            y +=1
            
        #Use sub-list lengths to convert residues to alpha helix designation in pymol
        cmd.alter("resi"+str(i[0][1])+'-'+str(i[y][1])+"/", "ss='H'")
        cmd.sort()
        cmd.rebuild()
        
        #Use sub-list length to add struts to the given helix, strut default color is white.
        name = ""
        cmd.pseudoatom("temp"+str(i_global), pos=[i[0][2], i[0][3], i[0][4]], name="A")
        cmd.pseudoatom("temp"+str(i_global), pos=[i[-1][2], i[-1][3], i[-1][4]], name="B")
        str1 = "temp"+str(i_global)+"////A"
        str2 = "temp"+str(i_global)+"////B"
        name = str(i_global) + "_helixStrut_" + str(i[0][1]) + "_" + str(i[-1][1])
        cmd.bond(str1, str2)
        cmd.create(name, "temp*")
        cmd.hide("everything", name)
        cmd.delete("temp*")
        cmd.set('stick_radius', float(0.5) , name)
        cmd.show("sticks", name)
        cmd.color("white", name)
        i_global = set_i_global()
        count +=1
        cmd.rebuild()
        
    #Reset view    
    cmd.reset()    
    print('Alpha helix reassignment and strut insertion completed.')
    
    #Beta supports
    print('Strutting beta sheets based on DSSP output...')
    beta_list = betas
    
    count = 1
    midResis = []
    for i in beta_list:
        #Find number of values in the sub-list
        x=len(i)
        
        #Reassign C-alpha to sheet designation in PyMOL
        for j in i:
            cmd.alter("resi"+str([1])+"/", "ss='S'")
            cmd.sort()
            cmd.rebuild()
        
        #find midpoint of the sub-list, round to nearest whole number
        mid = round(x/2)
        midResis.append(i[mid])
       
        
        #Support each collection of beta strands
        name = ""
        cmd.pseudoatom("temp"+str(i_global), pos=[i[0][2], i[0][3], i[0][4]], name="A")
        cmd.pseudoatom("temp"+str(i_global), pos=[i[x-1][2], i[x-1][3], i[x-1][4]], name="B")
        str1 = "temp"+str(i_global)+"////A"
        str2 = "temp"+str(i_global)+"////B"
        name = str(i_global) + "_betaStrut_" + str(i[0][1]) + "_" + str(i[x-1][1])
        cmd.bond(str1, str2)
        cmd.create(name, "temp*")
        cmd.hide("everything", name)
        cmd.delete("temp*")
        cmd.set('stick_radius', float(0.5) , name)
        cmd.show("sticks", name)
        cmd.color("white", name)
        i_global = set_i_global()
        count+=1
        cmd.reset()

    #Connect mid-points of beta strand groupings
    listLength = len(midResis)
    nextMid = 1
    for j in midResis:
        if nextMid < listLength:
            name = ""
            cmd.pseudoatom("temp"+str(i_global), pos=[j[2],j[3],j[4]], name="A")
            cmd.pseudoatom("temp"+str(i_global), pos=[midResis[nextMid][2],midResis[nextMid][3],midResis[nextMid][4]], name="B")
            str1 = "temp"+str(i_global)+"////A"
            str2 = "temp"+str(i_global)+"////B"
            name = str(i_global) + "_midStrut_" + str(j[1])
            cmd.bond(str1, str2)
            cmd.create(name, "temp*")
            cmd.hide("everything", name)
            cmd.delete("temp*")
            cmd.set('stick_radius', float(0.5) , name)
            cmd.show("sticks", name)
            cmd.color("white", name)
            i_global = set_i_global()
            nextMid+=1
            cmd.sort()
            cmd.rebuild()

        else:
            name = ""
            cmd.pseudoatom("temp"+str(i_global), pos=[j[2],j[3],j[4]], name="A")
            cmd.pseudoatom("temp"+str(i_global), pos=[midResis[0][2],midResis[0][3],midResis[0][4]], name="B")
            str1 = "temp"+str(i_global)+"////A"
            str2 = "temp"+str(i_global)+"////B"
            name = str(i_global) + "_midStrut_" + str(j[1])
            cmd.create(name, "temp*")
            cmd.hide("everything", name)
            cmd.delete("temp*")
            cmd.set('stick_radius', float(0.5) , name) 
            cmd.show("sticks", name)
            cmd.color("white", name)
            i_global = set_i_global()
            cmd.sort()
            cmd.rebuild()

    cmd.reset()
    print("Beta strutting completed.")
    return

def disorganized_struts(helices, b_sheets, loops):
    i_global = set_i_global()

    all_but_disorganized = helices
    for i in b_sheets:
        all_but_disorganized.append(i)

    disorgnized_region_dssp_output = loops

    start_positions = []
    Nearby_atom_dictionary = {}
    Nearby_atom_dictionary_refined = {}
    Paired_atoms = {}

    all_but_disorganized_flat = []
    for i in all_but_disorganized:
        for j in i:
                all_but_disorganized_flat.append(j)

    for i in disorgnized_region_dssp_output:
        if len(i) == 1:
            pos_1 = i[0]
            start_positions.append(pos_1) 

    for i in disorgnized_region_dssp_output:
        if len(i) % 2 == 0:
            pos_1 = i[int(len(i)/2)]
            start_positions.append(pos_1)

    for i in disorgnized_region_dssp_output:
        if len(i) != 1 and len(i) % 2 != 0:
            pos_1 = i[int((len(i)-1)/2+1)]
            start_positions.append(pos_1)

    for i in start_positions:
        Nearby_atom_dictionary[tuple(i)] = all_but_disorganized_flat

    for i in Nearby_atom_dictionary:
            u = i 
            v = Nearby_atom_dictionary[i]
            for j in v:
                v = v[:]
                if j[1] == u[1]-3 or j[1] == u[1]-2 or j[1] == u[1]-1 or j[1] == u[1] or j[1] == u[1]+1 or j[1] == u[1]+2 or j[1] == u[1]+3:
                    v.remove(j)
                    Nearby_atom_dictionary_refined[u]= v
                    
    def distance(y,i):
        a = int(float(y[2]))-int(float(i[2]))
        b = a**2
        c = int(float(y[3]))-int(float(i[3]))
        d = c**2
        e = int(float(y[4]))-int(float(i[4]))
        f = e**2
        distance = math.sqrt(b+d+f)
        return distance

    for y in Nearby_atom_dictionary_refined.keys():
        distances = map(lambda x:(x,distance(y,x)),tuple(Nearby_atom_dictionary_refined[tuple(y)]))
        #print(list(distances))
        distance_to_closest_atom = min(distances,key = lambda z:z[1])
        #print(y,"has the smallest distance of ",distance_to_closest_atom)
        Paired_atoms[tuple (y)]= distance_to_closest_atom[0]

    for i in Paired_atoms:
        u = i 
        v = Paired_atoms[i]

        name = ""
        cmd.pseudoatom("temp"+str(i_global), pos=[u[2],u[3],u[4]], name="A")
        cmd.pseudoatom("temp"+str(i_global), pos=[v[2],v[3],v[4]], name="B")
        str1 = "temp"+str(i_global)+"////A"
        str2 = "temp"+str(i_global)+"////B"
        name = str(i_global) + "_disorderedStrut_" + str(u[1]) + "_" + str(v[1])
        cmd.bond(str1, str2)
        cmd.create(name, "temp*")
        cmd.hide("everything", name)
        cmd.delete("temp*")
        cmd.set('stick_radius', float(0.5) , name)
        cmd.show("sticks", name)
        cmd.color("white", name)
        i_global = set_i_global()
    
    cmd.reset()
    print("Disorganized strutting completed.")
    return

def gap_struts(gap_list):
    i_global = set_i_global()
    count = 1
    
    for i in gap_list:
        gap = [CYLINDER, float(i[0][2]), float(i[0][3]), float(i[0][4]),
               float(i[1][2]), float(i[1][3]), float(i[1][4]), 0.5,
               0.5, 0, 1, 0.5, 0, 1]
        strutName = str(i_global) + '_gapStrut_' + str(count)
        cmd.load_cgo(gap, strutName)
        count += 1
        i_global = set_i_global()

    cmd.reset()
    print("Gap strutting completed.")
    return