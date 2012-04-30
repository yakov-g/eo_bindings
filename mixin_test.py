# -*- coding: UTF-8 -*-

from eobjdefault import *
from simple import *
from mixin import *

import sys

def cb(obj, *args, **kwargs):
    for arg in args:
        print "object : ", obj.name_get() ,";  data : ", arg


print "Initializing..."
init()
print ""

sobj = Simple(None)
#print "count: %d"%sobj.count

#sobj.callback_sig_a_changed_add(-6, cb, "2!")
print "ref: ", sobj.ref_get()

sobj.a_set(1)
sobj.b_set(2)
#s = sobj.ab_sum_get()
#print "sasdadsum: " , s 
sobj.a_get()
sobj.b_get()
sobj.ab_sum_get()
sobj.ab_sum_get()
sobj.ab_sum_get()
#print "count: %d"%sobj.count
#sobj.count = 110183
#print "count: %d"%sobj.count
#print "count: %d"%sobj.count2

#del sobj.count2






#sobj.add_and_set(0)


"""
sobj.callback_sig_a_changed_add(-6, cb, "2!")
sobj.callback_sig_a_changed_add(-100, cb, "1")

sobj.a_set(4)
sobj.a_set(5)
sobj.callback_sig_a_changed_del(cb)
sobj.a_set(8)
"""

print "end"


