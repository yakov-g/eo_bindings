# -*- coding: UTF-8 -*-

from eobjdefault import *
from evasobject import *
#from evasobj import *
from elwwin import *
from elwbox import *
from elwbutton import *
from elwboxedbutton import *

import sys


print "Initializing..."
init()
print ""

print sys.argv, "  ", len(sys.argv)
print ' '.join(sys.argv)

print "Initializing Elementary..."
print "Init res:", py_elm_init(sys.argv)

print ""

def ggg(obj, *args, **kwargs):
    for arg in args:
        print "object : ", obj.name_get() ,";  data : ", arg

def callback_del(obj, *args, **kwargs):
    o = args[0]
    o.callback_sig_clicked_del(ggg)

def callback_add(obj, *args, **kwargs):
    o = args[0]
    o.callback_sig_clicked_add(0, ggg, "bUtToN")

def fff(obj, *args, **kwargs):
    for arg in args:
        print "object : ", obj.name_get() ,";  data : ", arg


w1 = ElwWin(None)
w1.size_set(400, 400)
w1.visibility_set(1)

w = w1

bt = ElwButton(w)
bt.position_set(65, 25)
bt.size_set(80, 60)
bt.color_set(159, 245, 255, 255)
bt.text_set("שלום")
bt.visibility_set(1)
bt.callback_eobj_ev_callback_add_add(0, fff, "BUTTON: callback_added")
bt.callback_eobj_ev_callback_del_add(0, fff, "BUTTON: callback_deleted")

del w
w = bt.parent_get()
print type(w)

ba = ElwButton(w);
ba.visibility_set(1)
ba.position_set(10, 100)
ba.size_set(70, 50)
ba.color_set(255, 0, 255, 255)
ba.text_set("(B) ADD cb")
#ba.callback_sig_clicked_add(0, ggg, "bUtToN")


ba.callback_sig_clicked_add(0, callback_add, bt)
a,b,c,d = ba.color_get()
print "color : ", a, b, c, d
#xx,yy,ww,hh = ba.geometry_get(1234567890)
#print "geometry : ", xx, yy, ww, hh
#ba.no_par()
#ba.par_by_ref(90, 87)


bb = ElwBoxedButton(w);
bb.visibility_set(1)
bb.position_set(100, 100)
bb.size_set(70, 50)
bb.color_set(0, 255, 255, 255)
bb.text_set("(BB) DEL cb")



bb.callback_sig_clicked_add(0, callback_del, bt)

#===========================
but = ElwButton(w)
but.visibility_set(1)
but.position_set(250, 100)
but.size_set(90, 50)
but.color_set(255, 0, 255, 255)
but.text_set("1st button in box")

but2 = ElwButton(w)
but2.visibility_set(1)
but2.position_set(270, 150)
but2.size_set(90, 50)
but2.color_set(240, 240, 240, 255)
but2.text_set("2nd button in box")

box = ElwBox(w)
box.position_set(250, 250) 
box.size_set(50, 25) 
box.visibility_set(1) 
box.pack_end(but)
box.pack_end(but2)


#===========================
pb = ElwButton(w)
pb.visibility_set(1)
pb.position_set(310, 150)
pb.size_set(70, 50)
pb.color_set(240, 240, 245, 255)
pb.text_set("But in BB")
pb.callback_sig_clicked_add(0, callback_del, bt)

ebb = ElwBoxedButton(w)

ebb.visibility_set(1)
ebb.position_set(200, 150)
ebb.size_set(70, 50)
ebb.color_set(100, 85, 255, 255)
ebb.text_set("BoxedButton")
ebb.callback_sig_clicked_add(0, callback_del, bt)
ebb.pack_end(pb)


ebb.par_by_ref(5, 6)
ebb.no_par()

(x, y, w, h) = ebb.geometry_get(999)
print "geometry: ", x, y, w, h


print "setting data"
i = 5
ebb.data_set("int", i, None)
i = 999999

f = ebb.data_get("int")
print f, type(f)
f = ebb.data_del("int")

#ebb.data_set("list", ["a", "bb", "cc", "asdfasfd", "1234124", "asdf", "123", "12"])
#ebb.data_set("list", ["xx", "yy", "zz"])
#f = ebb.data_get("list")
#print f, type(f)

#l = ["a", "b", "c", "asd", "123"]
#ebb.data_set("list2", l)
#l[0] = "12341234124"
#del l
f = ebb.data_get("list2")
print f, type(f)


ebb.data_set("char", "string data", None)
f = ebb.data_get("char")
print f, type(f)

ebb.data_set("object",pb, None)
f = ebb.data_get("object")
print f, type(f)
f.text_set("neeew name")


#f = ebb.data_del("object")
#f = ebb.data_get("object")

#print f, type(f)


"""
bb2 = BB(w)
bb2.visibility_set(1)
bb2.position_set(70, 160)
bb2.size_set(40, 40)
bb2.color_set(128, 255, 128, 255)
bb2.text_set("BB")
bb2.some_box_function()
"""

print "Running Elementary..."
elem_run()

