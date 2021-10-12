#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:31:47 2021

@author: nd
"""

# import sys

# add file names here

## origin file
# file_1 = sys.argv[1]
file_1 = "dssp_output.txt"
## output file
file_out = "sec_strut_output.txt"


def file_read(file_name):  
    lines = open(file_1, "r").readlines()
    return lines

def file_output(file_out_list):
    convert_list = [str(x) for x in file_out_list]
    wrt = open(file_out, "w")
    for line in ','.join(convert_list):
        wrt.write(line)

def extract_info(in_file):
    new_list = []
    for line in in_file:
        line_s = line.split()
        line_seg = line[16:35].split()
        try: 
            line_s[1] = int(line_s[1])
            new_line_s = [line_s[2], line_s[1], line[16:25], line_seg[-2], line_seg[-1], line_s[-3], line_s[-2], line_s[-1]]
            new_list.append(new_line_s)
        except: 
            continue
    return new_list

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
    return helix_list, scraps

def sheet_loop(in_list):
    sheet_list, temp_list, temp_sheet = [], [], []
    for t_sheet in in_list:
        if t_sheet not in temp_list:
            temp_list.append(t_sheet)
        for n_sheet in temp_list:
            for t_res in t_sheet:
                if t_res in n_sheet:
                    continue
                elif t_res[1] in n_sheet:
                    n_sheet.append(t_res)
                else:
                    temp_list.append([t_res])
        
    return temp_list
            

def sheets(in_list):
    sheet_list, temp_sheet, scraps, temp = [], [], [], []
        
    for res in in_list:
        if "E" in res[2]:
                temp_sheet.append(res)
        else:
            scraps.append(res)
    
    for res in temp_sheet:
        if len(sheet_list) == 0:
            temp.append(str(res[1])+res[0])
            temp.append(str(res[3])+res[0])
            temp.append(res[4])
            sheet_list.append(temp)
        for lst in sheet_list:
            if str(res[1])+res[0] in lst:
                lst.append(str(res[3])+res[0])
                lst.append(str(res[4]))
            elif str(res[3])+res[0] in lst:
                lst.append(str(res[1])+res[0])
                lst.append(str(res[4]))
            elif str(res[4]) in lst:
                lst.append(str(res[1])+res[0])
                lst.append(str(res[3])+res[0])
            else:
                temp_sheet.append([str(res[1])+res[0], str(res[3])+res[0], res[4]])
    return temp_sheet, scraps


        
def main():
    file_list_1 = file_read(file_1)
    extract = extract_info(file_list_1)
    
    helices, scraps = helix(extract)
    #b_sheets, leftovers = sheets(scraps)
    file_output(helices)
    #rebuilt_1, num, info = rebuild_lists(file_list_1)
    #arrange_1 = arrange_data(num, info, rebuilt_1)
    #file_output(arrange_1)

main()