# -*- coding: UTF-8 -*-

import sys

from base.eodefault import py_elm_init, elem_run
from eobase import EoBase
from evas.py_evas import ElwWin, ElwBox, ElwButton, ElwBoxedbutton, EvasObject


def my_alert(ob):
  ob.alert("Hello")

print "Initializing Elementary..."
print "Init res:", py_elm_init(sys.argv)
print ""

p_but = None
p_box = None
p_bb = None

def cb_add():
  print "cb_add"

def cb_add2():
  print "cb_add2"

def cb_del():
  print "cb_del"

def cb_clicked():
  print ElwBoxedbutton.__mro__
  #p_but.alert("ALERT WORKS!!!")
  my_alert(p_but)
  my_alert(p_bb)
  #p_box.alert("BOX ALERT WORKS!!!")
#  p_bb.alert("BBB ALERT WORKS!!!")
  print "cb_clicked"

def cb_clicked2():
  print "cb_clicked2"
  #return CALLBACK_STOP

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

bt.event_callback_priority_add(EoBase.CALLBACK_ADD, -100, cb_add)
bt.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, cb_del)
print "adding clicked"
bt.event_callback_priority_add(ElwButton.CLICKED, -100, cb_clicked)
bt.event_callback_priority_add(ElwButton.CLICKED, -200, cb_clicked2)

del w
w = bt.parent_get()
print type(w)

ba = ElwButton(w);
p_but = ba
ba.visibility_set(1)
ba.position_set(10, 100)
ba.size_set(70, 50)
ba.color_set(255, 0, 255, 255)
ba.text_set("(B) ADD cb")

ba.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)
ba.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked2)

a,b,c,d = ba.color_get()
print "color : ", a, b, c, d
xx,yy,ww,hh = ba.size_get()
print "size : ", xx, yy, ww, hh
ba.no_par()
ba.par_by_ref(-2147483648, 87, -2147483649)
#ba.par_by_ref(-2147483648, 87, -9223372036854775808)
#ba.par_by_ref(-2147483648, 87, 9223372036854775807)

"""
ba.ints(0, 0)
print "\n\n ===  Testing int ==="
a = 4294967295
b = -2147483648
aa = bb = 0
aa,bb = ba.ints(a, b)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)
"""

(a, b) = ba.ints(1, 2, 3)
print a, b



a = 0
b = 2147483647
aa = bb = 0
aa,bb = ba.ints(a, b, 0)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)


print "\n\n ===  Testing long  ==="
a = 4294967295
b = -2147483648
aa = bb = 0
aa,bb = ba.longs(a, b)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)

a = 0
b = 2147483647
aa = bb = 0
aa,bb = ba.longs(a, b)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)


print "\n\n ===  Testing long long  ==="
a = 18446744073709551615
b = 9223372036854775807
aa = bb = 0
aa,bb = ba.longlongs(a, b)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)

a = 0
b = -9223372036854775808
aa = bb = 0
aa,bb = ba.longlongs(a, b)
print "a == aa %s, b == bb %s"%(a == aa, b == bb)


print "\n\n ===  Testing floats  ==="
b = -246524637565987672456521345235235235234836234523523452351123.55123546946256245634563465
c = -24652463756598767235234836234523523452351123.55123546946256245634563465
bb = cc = 0
bb, cc = ba.floats(b, c)
print "b == bb %s, c == cc %s"%( b == bb, c == cc)

bb = ElwBoxedbutton(w);
p_bb = bb
bb.visibility_set(1)
bb.position_set(100, 100)

bb.size_set(70, 50)
bb.color_set(255, 0, 5, 255)

bb.text_set(u"Красная кнопка")
try:
  bb.text_set(bb)
except TypeError as ex:
  print "TypeError: %s"%ex

bb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)

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
p_box = box
box.position_set(250, 250) 
box.size_set(50, 25) 
box.visibility_set(1) 
box.pack_end(but)
box.pack_end(but2)

#but3 = ElwButton(box)
#but3.visibility_set(1)
#but3.position_set(279, 150)
#but3.size_set(20, 30)
#but3.color_set(240, 240, 240, 255)
#but3.text_set("3nd button in box")


#===========================
pb = ElwButton(w)
pb.visibility_set(1)
pb.position_set(310, 150)
pb.size_set(70, 50)
pb.color_set(240, 240, 245, 255)
pb.text_set("But in BB")
pb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)


ebb = ElwBoxedbutton(w)

ebb.visibility_set(1)
ebb.visibility_set(1)
ebb.position_set(200, 150)
ebb.size_set(70, 50)
ebb.color_set(100, 85, 255, 255)
ebb.text_set("BoxedButton")

ebb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)

ebb.pack_end(pb)

"""
ebb.par_by_ref(5, 6)
ebb.no_par()
(x, y, w, h) = ebb.geometry_get(999)
print "geometry: ", x, y, w, h
"""

print "setting data"
i = 5
ebb.data_set("int", i)
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


ebb.data_set("char", "string data")
f = ebb.data_get("char")
print f, type(f)

ebb.data_set("object",pb)
f = ebb.data_get("object")
print f, type(f)
f.text_set("neeew name")


#f = ebb.data_del("object")

"""
bb2 = BB(w)
bb2.visibility_set(1)
bb2.position_set(70, 160)
bb2.size_set(40, 40)
bb2.color_set(128, 255, 128, 255)
bb2.text_set("BB")
bb2.some_box_function()
"""

print but.size_get()
print but.text_get()
print but.visibility_get()
print "Running Elementary..."
elem_run()

