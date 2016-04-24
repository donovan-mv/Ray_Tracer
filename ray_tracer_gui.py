#GUI and graphical display for ray_tracer backend


from Tkinter import *
import ray_tracer as rt
import math
import sys


def compute():
    img.delete("all")
    
    org_x = 151
    org_y = 76
    scale = 7

    ret = (0, 0, 0, 0, 0, 0)
    try:
        r1 = float(ent_r1.get())
        r2 = float(ent_r2.get())
        led = float(ent_led.get())
        if led > 0:
            led = led*(-1)
        led = led - 1 #required for distance from lens
        ret = rt.trace(r1, r2, led, float(ent_theta.get()))
        #print math.degrees(math.atan(ret[5]))
    except:
        print "\n**********************************************\nIncompatible data!!"

    if r1 < 0:
        img.create_arc(org_x-(scale*3), org_y-(scale*math.sqrt(r1**2-(-2-(r1-1))**2)), org_x-scale*1, org_y+(scale*math.sqrt(r1**2-(-2-(r1-1))**2)), start=90, extent=-180, style=ARC)
    else:
        img.create_arc(org_x-(scale*1), org_y-(scale*math.sqrt(r1**2-(r1-1)**2)), org_x+scale*1,org_y+(scale*math.sqrt(r1**2-(r1-1)**2)), start=90, extent=180, style=ARC)

    if r2 < 0:
        img.create_arc(org_x-scale*1, org_y-(scale*math.sqrt(r2**2-(r2+1)**2)), org_x+(scale*1),org_y+(scale*math.sqrt(r2**2-(r2+1)**2)), start=90, extent=-180, style=ARC)
    else:
        img.create_arc(org_x+(scale*1), org_y-(scale*math.sqrt(r2**2-(2-(r2+1))**2)), org_x+scale*3, org_y+(scale*math.sqrt(r2**2-(2-(r2+1))**2)), start=90, extent=180, style=ARC)
    
    if ret[0] is -1 or ret[2] is -1 or ret[5] is -1:
        root.destroy()
        sys.exit()

    img.create_line(org_x+scale*ret[0], org_y-scale*ret[1], org_x+scale*led, org_y, arrow=FIRST)
    img.create_line(org_x+scale*ret[2], org_y-scale*ret[3], org_x+scale*ret[0], org_y-scale*ret[1])

    if ret[5] < 0:
        print "here"
        img.create_line(250, org_y + math.fabs(scale*(ret[3]+(ret[5]*((250/scale)-ret[2])))), org_x+scale*ret[2], org_y-scale*ret[3])
    else:
        img.create_line(250, org_y - (scale*(ret[3]+(ret[5]*((250/scale)-ret[2])))), org_x+scale*ret[2], org_y-scale*ret[3])

    img.create_line(org_x,10, org_x,141, dash=(3,8))
    img.create_line(10,org_y, 291,org_y, dash=(3,8))
    

root = Tk()
root.title("Ray Tracer (Spherical Lens)")
root.resizable(height=FALSE, width=FALSE)

fr = Frame(root, bd=5)
fr.grid()

lb_r1 = Label(fr, text="R1", anchor=W, width=17)
lb_r1.grid(row=0, column=0)
lb_r2 = Label(fr, text="R2", anchor=W, width=17)
lb_r2.grid(row=1, column=0)
lb_led = Label(fr, text="LED x pos", anchor=W, width=17)
lb_led.grid(row=2, column=0)
lb_theta = Label(fr, text="Input ray inclination", anchor=W, width=17)
lb_theta.grid(row=3, column=0)

ent_r1 = Entry(fr, width=15)
ent_r1.grid(row=0, column=1, pady=5, sticky=W)
ent_r2 = Entry(fr, width=15)
ent_r2.grid(row=1, column=1, pady=5, sticky=W)
ent_led = Entry(fr, width=15)
ent_led.grid(row=2, column=1, pady=5, sticky=W)
ent_theta = Entry(fr, width=15)
ent_theta.grid(row=3, column=1, pady=5, sticky=W)

butt = Button(fr, text="Compute", width=30, command=compute)
butt.grid(row=4, column=0, columnspan=2, pady=10)

img = Canvas(fr, width=301, height=151, relief=GROOVE, bd=3)
img.grid(row=0, column=2, rowspan=5, padx=10, pady=2, sticky=E)

root.mainloop()
