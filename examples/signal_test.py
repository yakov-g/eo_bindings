# -*- coding: UTF-8 -*-

from eoeoeo.eodefault import *#for CALLBACK_STOP
from eoeoeo.eobase import EoBase
from eoeoeo.signals_py import Simple

def cb_del(o, d):
  print "OBJECT DELETED"

_o_cb_del = (cb_del, None)

def cb_free(o, d):
  print "OBJECT FREED"

_o_cb_free = (cb_free, None)

def cb_a_changed(o, d):
  print "A_CHANGED"

_o_cb_a_changed = (cb_a_changed, None)

def cb_a_changed_stop(o, d):
  print "A_CHANGED_STOP"
  return CALLBACK_STOP
_o_cb_a_changed_stop = (cb_a_changed_stop, None)

def cb_add(o, d):
  print "CALBACK_ADD"

_o_cb_add = (cb_add, None)

def cb_del(o, d):
  print "CALBACK_DEL"

_o_cb_del = (cb_del, None)


print "Creating Simple object"
sobj = Simple(None)

print "adding event on EV_DELETING"
sobj.event_callback_priority_add(EoBase.DEL, 0, _o_cb_del)

print "adding event on CHANGING"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed)

print "adding event on EV_ADDING"
sobj.event_callback_priority_add(EoBase.CALLBACK_ADD, 0, _o_cb_add)

print "adding 2 events on EV_DELETING"
sobj.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, _o_cb_del)
sobj.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, _o_cb_del)

print "adding event on CHANGING"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed)

print "adding 2nd event on ADDING"
sobj.event_callback_priority_add(EoBase.CALLBACK_ADD, 0, _o_cb_add)

sobj.simple_a_set(4)

print "deleting event on EV_ADDING"
sobj.event_callback_del(EoBase.CALLBACK_ADD, cb_add)

print "deleting event on EV_DELETING"
sobj.event_callback_del(EoBase.CALLBACK_DEL, cb_del)

print "adding 4 events on CHANGING, second is STOP"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed_stop)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, _o_cb_a_changed)
sobj.simple_a_set(5)


print "deleting event on CHANGING"
res = sobj.event_callback_del(Simple.A_CHANGED, _o_cb_a_changed)
print "Res:", res

print "explicitly calling ON_CHANGE"
res = sobj.event_callback_call(Simple.A_CHANGED, (123,123))
print "Res:", res


sobj.event_global_freeze()

sobj.simple_a_set(89)
#sobj.b_set(8)

#res = sobj.c_get()
#print "Res:", res

del sobj





