
# -*- coding: UTF-8 -*-

from eobjdefault import *
from simple import *


import sys


def cb(obj, *args, **kwargs):
#    for arg in args:
#        print "on_change cb : ", obj.name_get() ,";  data : ", arg
   print "on_change cb : object : %s; event_info: %s; data: %s"%(obj.name_get(), args[0], ",".join(args[1:]))

def fff(obj, *args, **kwargs):
  print "py_cb_func: object : %s; event_info: %s; data: %s"%(obj.name_get(), args[0], ",".join(args[1:]))


print "Initializing..."
init()
print ""

print "Creating Simple object"
sobj = Simple(None)

sobj.callback_eobj_ev_del_add(0, fff, "OBJECT DELETED")
sobj.callback_eobj_ev_free_add(0, fff, "OBJECT FREED")

#sobj.delete()

print "adding event on CHANGING"
sobj.callback_sig_a_changed_add(100, cb, "data 3")


print "adding event on EV_ADDING"
sobj.callback_eobj_ev_callback_add_add(0, fff, "callback on EV_ADD")
print "adding 2 events on EV_DELETING"
sobj.callback_eobj_ev_callback_del_add(0, fff, "callback on EV_DEL")
sobj.callback_eobj_ev_callback_del_add(0, fff, "callback on EV_DEL2")

print "adding event on CHANGING"
sobj.callback_sig_a_changed_add(5, cb, "4")
print "adding 2nd event on ADDING"
sobj.callback_eobj_ev_callback_add_add(0, fff, "callback on EV_ADD2")


sobj.a_set(4)


print "deleting event on EV_ADDING"
sobj.callback_eobj_ev_callback_add_del(fff)
print "deleting event on EV_DELETING"
sobj.callback_eobj_ev_callback_del_del(fff)

print "adding 3 events on CHANGING"
sobj.callback_sig_a_changed_add(3, cb, "5", __stop__ = "")
sobj.callback_sig_a_changed_add(-6, cb, "2!")
sobj.callback_sig_a_changed_add(-100, cb, "1")

sobj.a_set(5)

print "deleting event on CHANGING"
sobj.callback_sig_a_changed_del(cb)



#sobj.callback_sig_a_changed_del(cb)
sobj.a_set(8)



