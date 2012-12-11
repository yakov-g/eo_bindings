# -*- coding: UTF-8 -*-
import sys


from eorepo.eobase import EoBase
from eorepo.evas_py import ElwWin, ElwBox, ElwButton, ElwBoxedbutton, ExEvasObject
from eorepo.evas_py import elm_run, elm_init


lst = [56, "elm", 56.76]

print "Initializing Elementary..."
print "Init res:", elm_init(sys.argv)
print ""

global_obj = None


def freeze_me(obj):
  global global_obj
  global_obj = obj
  obj.event_freeze()
  obj.elw_alert_alert("obl: " + obj.text_get() + "; freezing events; count: " + str(obj.event_freeze_get()))


def thaw_global(obj):
  global global_obj
  if global_obj.event_freeze_get() == 0:
    return
  obj.alert("thawing global")
  global_obj.event_thaw()


########################   setting data  ##########################
def properties_cb(obj, data):
  a,b,c,d = obj.exevas_obj_color_get()
  print "color : ", a, b, c, d
  ww,hh = obj.exevas_obj_size_get()
  xx,yy = obj.exevas_obj_position_get()
  print "size : " +  str((ww, hh)) + "; pos: " + str((xx, yy))

  obj.exevas_obj_size_set(ww-1, hh)
  obj.exevas_obj_color_set(a-5, b, c-10, d)

########################   setting data  ##########################
def data_cb(obj, data):
  print "setting data - int : 5"
  i = 5
  obj.data_set("int", i)
  i = 999999

  f = obj.data_get("int")
  print "getting data"
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

  print "setting data - char : string data"
  obj.data_set("char", "string data")
  f = obj.data_get("char")
  print f, type(f)

  obj.data_set("object",pb)
  f = obj.data_get("object")
  print "getting data"
  print f, type(f)
#f.text_set("neeew name")
#f = ebb.data_del("object")




def cb_add(o, data):
  o.elw_alert_alert("  obj: " + o.elw_button_text_get() + "; cb_added")

def cb_del(o, data):
  o.elw_alert_alert("  obj: " + o.elw_button_text_get() + "; cb_deleted")

def thaw_ba(o, data):
  print "  size:", o.size_get()
  p_but.event_thaw()

def cb_clicked(o, data):
  print o
  o.elw_alert_alert("  obj: " + o.elw_button_text_get())
  print "=== data ==="
  d = data
  print d
  print "======"
  lst.append("!")
  

w1 = ElwWin(None)
w1.exevas_obj_size_set(370, 350)
w1.exevas_obj_visibility_set(1)


w = w1

bt = ElwButton(w)
bt.exevas_obj_position_set(30, 30)
bt.exevas_obj_size_set(210, 60)
bt.exevas_obj_color_set(159, 245, 255, 255)
bt.elw_button_text_set("Hello")
bt.exevas_obj_visibility_set(1)

print "\n> adding cb on CALLBACK_ADD"
cb_obj1 = (cb_add, None)
bt.event_callback_priority_add(EoBase.CALLBACK_ADD, -100, cb_obj1)
print "\n> adding cb on CALLBACK_DEL"
cb_obj2 = (cb_del, None)
bt.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, cb_obj2)
print "\n> adding cb on CLICKED"

cb_obj3 = (cb_clicked, None)
bt.event_callback_priority_add(ElwButton.CLICKED, -100, cb_obj3)
#bt.event_callback_priority_add(ElwButton.CLICKED, -200, thaw_ba)
print "\n> adding cb on CLICKED"
cb_obj4 = (properties_cb, None)
bt.event_callback_priority_add(ElwButton.CLICKED, -200, cb_obj4)

del w
w = bt.parent_get()
print type(w)

ba = ElwButton(w);
ba.exevas_obj_visibility_set(1)
ba.exevas_obj_position_set(30, 100)
ba.exevas_obj_size_set(100, 50)
ba.exevas_obj_color_set(255, 0, 255, 255)
ba.elw_button_text_set("(B) ADD cb")



cb_obj5 = (cb_clicked, lst)
print cb_obj5
ba.event_callback_priority_add(ElwButton.CLICKED, 0, cb_obj5)
#ba.event_callback_del(ElwButton.CLICKED, cb_obj5)

print "Running Elementary..."

elm_run()

