from tkinter import *
from pymol import cmd, stored, selector

def XYZ_increment():

    def update_window():
        root.destroy()
        XYZ_increment()

    def x_increment():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('x=x+1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('x=x+1'))

    def x_decrement():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('x=x-1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('x=x-1'))

    def y_increment():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('y=y+1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('y=y+1'))

    def y_decrement():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('y=y-1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('y=y-1'))

    def z_increment():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('z=z+1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('z=z+1'))

    def z_decrement():
        if str(var1.get()) == 'sele':
            cmd.alter_state(1, 'sele', str('z=z-1'))
        else:    
            cmd.alter_state(1, str('/'+var1.get()+'/PSDO/P/PSD`1/'+var2.get()), str('z=z-1'))


    def radius_increment():
        radius = cmd.get('stick_radius',str(var1.get()))
        radius = float(radius) + 0.1
        cmd.set('stick_radius', str(radius), str(var1.get()))
        # default value for stick radius is 0.3

    def radius_decrement():
        radius = cmd.get('stick_radius',str(var1.get()))
        radius = float(radius) - 0.1
        cmd.set('stick_radius', str(radius), str(var1.get()))
        # default value for stick radius is 0.3

    
    # I couldn't get the drag function to work - may not be fully developed...
    
    # def drag_on():
    #    cmd.drag('sele',1,1,1)

    # def drag_off():
    #    cmd.drag()

    ####### Tkinter Window initialization #######
    
    root = Tk()
    root.geometry("600x400")
    root.title("Adjust Strut Endpoints")

    object_list_1 = ["sele"]
    for obj in cmd.get_object_list():
        if '_' not in str(obj):
            next
        else:
            object_list_1.append(str(obj))
    
    object_list_2 = ['A','B']

    B0 = Button(root, text ="Update Object List", command=lambda : update_window())
    B0.grid(row=1,column=3)

    ## Option Menu Lable

    l1 = Label(root, text="Strut Object Name:")
    l1.grid(row=1,column=1, sticky='E')
    
    ## Option Menu: Object List

    var1 = StringVar()
    var1.set(object_list_1[0]) # default value

    w1 = OptionMenu(root, var1, *object_list_1)
    w1.grid(row=1,column=2)

    ## Strut End-point Selector

    l2 = Label(root, text="Strut Endpoint:")
    l2.grid(row=2,column=1, sticky='E')

    var2 = StringVar()
    var2.set(object_list_2[0]) # default value

    w2 = OptionMenu(root, var2, *object_list_2)
    w2.grid(row=2,column=2)

    ####### X-Value #######

    l3 = Label(root, text="X-Value:")
    l3.grid(row=3,column=2)

    B1 = Button(root, text ="+", command=lambda : x_increment())
    B1.grid(row=3,column=3)

    B2 = Button(root, text ="-", command=lambda : x_decrement())
    B2.grid(row=3,column=4)

    ####### Y-Value #######
    
    l4 = Label(root, text="Y-Value:")
    l4.grid(row=4,column=2)

    B3 = Button(root, text ="+", command=lambda : y_increment())
    B3.grid(row=4,column=3)

    B4 = Button(root, text ="-", command=lambda : y_decrement())
    B4.grid(row=4,column=4)

    ####### Z-Value #######

    l5 = Label(root, text="Z-Value:")
    l5.grid(row=5,column=2)

    B5 = Button(root, text ="+", command=lambda : z_increment())
    B5.grid(row=5,column=3)

    B6 = Button(root, text ="-", command=lambda : z_decrement())
    B6.grid(row=5,column=4)

    ####### Strut Radius #######
    
    l6 = Label(root, text="Strut Radius:")
    l6.grid(row=6,column=2)

    B7 = Button(root, text ="+", command=lambda : radius_increment())
    B7.grid(row=6,column=3)

    B8 = Button(root, text ="-", command=lambda : radius_decrement())
    B8.grid(row=6,column=4)
    
    # l7 = Label(root, text="Drag:")
    # l7.grid(row=7,column=2)

    # B9 = Button(root, text ="ON", command=lambda : drag_on())
    # B9.grid(row=7,column=3)

    # B10 = Button(root, text ="OFF", command=lambda : drag_off())
    # B10.grid(row=7,column=4)
    
    root.attributes('-topmost',True)
    root.mainloop()