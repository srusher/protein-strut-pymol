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
