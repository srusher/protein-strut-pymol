#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:31:47 2021

@author: nd
"""

import sys

# add file names here

## origin file
file_in = sys.argv[1]
## output file
file_out = "_output.txt"

# read in file
def file_read(file_name):  
    lines = open(file_in, "r").readlines()
    return lines

# outputs file
def file_output(file_out_list):
    # sec_strut_output, helices, b_sheets, loops, gaps
    out_type = ['secStrut', 'helix', 'sheet', 'loop', 'gap']
    for i, j in zip(out_type, file_out_list):    
        convert_list = [str(x) for x in j]
        wrt = open(i + file_out, "w")
        for line in ','.join(convert_list):
            wrt.write(line)

# extracts needed residue information
def extract_info(in_file):
    new_list = []
    for line in in_file:
        line_s = line.split()
        line_seg = line[16:35].split()
        try: 
            line_s[1] = int(line_s[1])
            new_line_s = [line_s[2], line_s[1], line[16:25], line_seg[-2], line_seg[-1], float(line_s[-3]), float(line_s[-2]), float(line_s[-1])]
            new_list.append(new_line_s)
        except: 
            continue
    return new_list

# Extracts helix residue information and builds a list of helices
# lists info for each alph carbon in each helix
def helix(in_list):
    helix_list, temp_helix, scraps, temp  = [], [], [], []
    for res in (in_list):
        try:
            int(res[0]) == False
        except:
            if "H" in res[2] or "I" in res[2] or "G" in res[2]:
                temp_helix.append(res)
            else:
               scraps.append(res)
    for res in temp_helix:
        if temp == []:
            temp.append([res[0], res[1], res[-3], res[-2], res[-1]])
        elif res[1] == temp[-1][1] + 1:
            temp.append([res[0], res[1], res[-3], res[-2], res[-1]])
        else:
            helix_list.append(temp)
            temp = []
            temp.append([res[0], res[1], res[-3], res[-2], res[-1]])
    helix_list.append(temp)
    return helix_list, scraps

# Extracts strand residue information
def sheet_loop(in_list):
    temp_sheet, new_sheet = [], []
    # builds a list of strand residues
    # and directly hydrogen bonded strand residues    
    for strand in in_list:
        temp_strand = []
        for res in strand:
            if res[2] not in temp_strand and res[2] != '0A':
                temp_strand.append(res[2])
            if res[3] not in temp_strand and res[3] != '0A':
                temp_strand.append(res[3])
            if res[4] not in temp_strand and res[4] != '0A':
                temp_strand.append(res[4])
        temp_sheet.append(temp_strand)
    # groups strands into sheets
    for sheet in temp_sheet:
        if sheet == temp_sheet[0]:
            new_sheet.append(sheet)
            continue
        else:
            for res in sheet:
                idx2 = 0
                for sheet_t in new_sheet:
                    if new_sheet[0] == 0:
                        new_sheet = [] 
                        new_sheet.append(sheet)
                        break
                    elif res in sheet_t and sheet != sheet_t:
                        a = list(dict.fromkeys(sheet + sheet_t))
                        new_sheet.pop(idx2)
                        new_sheet.append(a)
                        break
                    elif res not in sheet_t:
                        continue
                    elif res == sheet[-1] and res not in sheet_t:
                        new_sheet.append(sheet)
                    idx2 += 1   
    return new_sheet
            
# Extracts strand residue information
# Builds a list of sheets
def sheets(in_list):
    strand_list, temp_sheet, scraps, temp  = [], [], [], []
    for res in (in_list):
        try:
            int(res[0]) == False
        except:
            if "E" in res[2]:
                temp_sheet.append(res)
            else:
               scraps.append(res)
    for res in temp_sheet:
        if temp == []:
            temp.append([res[0], res[1], str(res[1])+res[0], str(res[3])+res[0], res[4], res[-3], res[-2], res[-1]])
        elif res[1] == temp[-1][1] + 1:
            temp.append([res[0], res[1], str(res[1])+res[0], str(res[3])+res[0], res[4], res[-3], res[-2], res[-1]])
        else:
            strand_list.append(temp)
            temp = []
            temp.append([res[0], res[1], str(res[1])+res[0], str(res[3])+res[0], res[4], res[-3], res[-2], res[-1]])
    strand_list.append(temp)
    # converts list of strands to a list of sheets
    sheet_list = sheet_loop(strand_list)
    # extracts positional info for sheet residues 
    out_list = []
    for sheet in sheet_list:
        out_sheet_t = []
        for res in sheet:
            for item in temp_sheet:
                if int(res[:-1]) == item[1]:
                    out_sheet_t.append(item[:2]+item[-3:])
        out_list.append(out_sheet_t)     
    return out_list, scraps

# extracts loops and gaps
def disordered(full_list, scrap_list):
    gaps, loops, loop = [], [], []
    # finds gaps
    i = full_list[0][1]
    item_k = False
    for item in full_list:
        item_l = [item[0], item[1], item[-3], item[-2], item[-1]]
        if item_l[1] == i:
            continue
        elif item_l[1] != i+1:
            gaps.append([item_k, item_l])
        i = item_l[1]
        item_k = item_l 
    
    #finds loops
    j = scrap_list[0][1]
    for item in scrap_list:
        item_l = [item[0], item[1], item[-3], item[-2], item[-1]]
        if item_l[1] == j:
            loop.append(item_l)
            j = item_l[1]
        elif j == scrap_list[-1] and len(loop) > 0:
            loops.append(loop)
            j = item_l[1] 
        elif item_l[1] == j+1:
            loop.append(item_l)
            j = item_l[1]
        elif item_l[1] > j+1:
            loops.append(loop)
            loop = []
            j = item_l[1]
    
    #print(loops)
    return loops, gaps


# Main fxn        
def main():
    file_list_1 = file_read(file_in)
    extract = extract_info(file_list_1)    
    helices, scraps = helix(extract)
    b_sheets, leftovers = sheets(scraps)
    loops, gaps = disordered(extract, leftovers)
    sec_strut_output = helices + b_sheets
    file_output([sec_strut_output, helices, b_sheets, loops, gaps])

main()