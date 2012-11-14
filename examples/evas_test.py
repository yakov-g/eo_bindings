# -*- coding: UTF-8 -*-
import sys

from base.eodefault import py_elm_init, elem_run
from eobase import EoBase
from evas.py.evas_py import ElwWin, ElwBox, ElwButton, ElwBoxedbutton, ExEvasObject


print "Initializing Elementary..."
print "Init res:", py_elm_init(sys.argv)
print ""

global_obj = None


def freeze_me(obj):
  global global_obj
  global_obj = obj
  obj.event_freeze()
  obj.alert("obl: " + obj.text_get() + "; freezing events; count: " + str(obj.event_freeze_get()))


def thaw_global(obj):
  global global_obj
  if global_obj.event_freeze_get() == 0:
    return
  obj.alert("thawing global")
  global_obj.event_thaw()


########################   setting data  ##########################
def properties_cb(obj):
  a,b,c,d = obj.color_get()
  print "color : ", a, b, c, d
  ww,hh = obj.size_get()
  xx,yy = obj.position_get()
  print "size : " +  str((xx, yy)) + "; pos: " + str((ww, hh))

  obj.size_set(ww-1, hh)
  obj.color_set(a-5, b, c-10, d)

########################   setting data  ##########################
def data_cb(obj):
  print "setting data"
  i = 5
  obj.data_set("int", i)
  i = 999999

  f = obj.data_get("int")
  print f, type(f)
  f = obj.data_del("int")

#ebb.data_set("list", ["a", "bb", "cc", "asdfasfd", "1234124", "asdf", "123", "12"])
#ebb.data_set("list", ["xx", "yy", "zz"])
#f = ebb.data_get("list")
#print f, type(f)

#l = ["a", "b", "c", "asd", "123"]
#ebb.data_set("list2", l)
#l[0] = "12341234124"
#del l
#  f = obj.data_get("list2")
#  print f, type(f)

  obj.data_set("char", "string data")
  f = obj.data_get("char")
  print f, type(f)

  obj.data_set("object",pb)
  f = obj.data_get("object")
  print f, type(f)
#f.text_set("neeew name")
#f = ebb.data_del("object")


########################   print numbers  ##########################
def num_cb(obj):
  obj.no_par()
  obj.par_by_ref(-2147483648, 87, -2147483649)

  obj.ints(0, 0, 1)
  print "\n\n ===  Testing int ==="
  a = 4294967295
  b = -2147483648
  aa = bb = 0
  aa,bb = ba.ints(a, b, 0)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  (a, b) = ba.ints(1, 2, 3)
  print a, b

  a = 0
  b = 2147483647
  aa = bb = 0
  aa,bb = obj.ints(a, b, 0)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  print "\n\n ===  Testing long  ==="
  a = 4294967295
  b = -2147483648
  aa = bb = 0
  aa,bb = obj.longs(a, b)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  a = 0
  b = 2147483647
  aa = bb = 0
  aa,bb = obj.longs(a, b)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  print "\n\n ===  Testing long long  ==="
  a = 18446744073709551615
  b = 9223372036854775807
  aa = bb = 0
  aa,bb = obj.longlongs(a, b)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  a = 0
  b = -9223372036854775808
  aa = bb = 0
  aa,bb = obj.longlongs(a, b)
  print "a == aa %s, b == bb %s"%(a == aa, b == bb)

  print "\n\n ===  Testing floats  ==="
  b = -246524637565987672456521345235235235234836234523523452351123.55123546946256245634563465
  c = -24652463756598767235234836234523523452351123.55123546946256245634563465
  bb = cc = 0
  bb, cc = obj.floats(b, c)
  print "b == bb %s, c == cc %s"%( b == bb, c == cc)

###########################################################################
###########################################################################


def cb_add(o):
  o.alert("  obj: " + o.text_get() + "; cb_added")

def cb_del(o):
  o.alert("  obj: " + o.text_get() + "; cb_deleted")

def thaw_ba(o):
  print "  size:", o.size_get()
  p_but.event_thaw()

def cb_clicked(o):
  o.alert("  obj: " + o.text_get())
  

w1 = ElwWin(None)
w1.size_set(370, 350)
w1.visibility_set(1)


w = w1

bt = ElwButton(w)
bt.position_set(30, 30)
bt.size_set(210, 60)
bt.color_set(159, 245, 255, 255)
bt.text_set("Hello")
bt.visibility_set(1)

print "> adding cb on CALLBACK_ADD"
bt.event_callback_priority_add(EoBase.CALLBACK_ADD, -100, cb_add)
print "> adding cb on CALLBACK_DEL"
bt.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, cb_del)
print "> adding cb on CLICKED"
bt.event_callback_priority_add(ElwButton.CLICKED, -100, cb_clicked)
#bt.event_callback_priority_add(ElwButton.CLICKED, -200, thaw_ba)
print "> adding cb on CLICKED"
bt.event_callback_priority_add(ElwButton.CLICKED, -200, properties_cb)

del w
w = bt.parent_get()
print type(w)

ba = ElwButton(w);
ba.visibility_set(1)
ba.position_set(30, 100)
ba.size_set(100, 50)
ba.color_set(255, 0, 255, 255)
ba.text_set("(B) ADD cb")
ba.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)

bb = ElwBoxedbutton(w);
p_bb = bb
bb.visibility_set(1)
bb.position_set(140, 100)
bb.size_set(100, 50)
bb.color_set(255, 0, 5, 255)
bb.text_set(u"Red button")




try:
  bb.text_set(bb)
except TypeError as ex:
  print "TypeError: %s"%ex


bb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)



#===========================
but = ElwButton(w)
but.visibility_set(1)
#but.position_set(250, 100)
but.size_set(90, 20)
but.color_set(255, 0, 255, 255)
but.text_set("1st button in box - gl_thaw")
but.event_callback_priority_add(ElwButton.CLICKED, 0, thaw_global)



but2 = ElwButton(w)
but2.visibility_set(1)
#but2.position_set(270, 150)
#but2.size_set(90, 50)
but2.color_set(255, 255, 0, 255)
but2.text_set("2nd button in box - freeze cb")
but2.event_callback_priority_add(ElwButton.CLICKED, 0, freeze_me)




box = ElwBox(w)
p_box = box
box.position_set(140, 170) 
box.size_set(50, 50) 
box.visibility_set(1) 



box.pack_end(but)
box.pack_end(but2)



#===========================
pb = ElwButton(w)
pb.visibility_set(1)
#pb.position_set(310, 150)
#pb.size_set(70, 50)
pb.color_set(240, 240, 245, 255)
pb.text_set("But in BB")
pb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)
pb.event_callback_priority_add(ElwButton.CLICKED, 0, num_cb)


ebb = ElwBoxedbutton(w)
ebb.visibility_set(1)
ebb.position_set(30, 170)
ebb.size_set(100, 50)
ebb.color_set(100, 85, 255, 255)
ebb.text_set("BoxedButton")
ebb.event_callback_priority_add(ElwButton.CLICKED, 0, cb_clicked)
ebb.event_callback_priority_add(ElwButton.CLICKED, 0, data_cb)
ebb.pack_end(pb)


print "Running Elementary..."

elem_run()

