# -*- coding: UTF-8 -*-

from base.eodefault import *
from eobase import EoBase
from signals.py.signals_py import Simple

def cb_del(o):
  print "OBJECT DELETED"

def cb_free(o):
  print "OBJECT FREED"

def cb_a_changed(o):
  print "A_CHANGED"

def cb_a_changed_stop(o):
  print "A_CHANGED_STOP"
  return CALLBACK_STOP

def cb_add(o):
  print "CALBACK_ADD"
def cb_del(o):
  print "CALBACK_DEL"


print "Creating Simple object"
sobj = Simple(None)


print "adding event on EV_DELETING"
sobj.event_callback_priority_add(EoBase.DEL, 0, cb_del)

print "adding event on CHANGING"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed)

print "adding event on EV_ADDING"
sobj.event_callback_priority_add(EoBase.CALLBACK_ADD, 0, cb_add)

print "adding 2 events on EV_DELETING"
sobj.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, cb_del)
sobj.event_callback_priority_add(EoBase.CALLBACK_DEL, 0, cb_del)

print "adding event on CHANGING"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed)

print "adding 2nd event on ADDING"
sobj.event_callback_priority_add(EoBase.CALLBACK_ADD, 0, cb_add)

sobj.a_set(4)

print "deleting event on EV_ADDING"
sobj.event_callback_del(EoBase.CALLBACK_ADD, cb_add)

print "deleting event on EV_DELETING"
sobj.event_callback_del(EoBase.CALLBACK_DEL, cb_del)

print "adding 4 events on CHANGING, second is STOP"
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed_stop)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed)
sobj.event_callback_priority_add(Simple.A_CHANGED, 0, cb_a_changed)

sobj.a_set(5)


print "deleting event on CHANGING"
res = sobj.event_callback_del(Simple.A_CHANGED, cb_a_changed)
print "Res:", res

print "explicitly calling ON_CHANGE"
res = sobj.event_callback_call(Simple.A_CHANGED, (123,123))
print "Res:", res


sobj.event_global_freeze()

sobj.a_set(89)
#sobj.b_set(8)

#res = sobj.c_get()
#print "Res:", res

del sobj





