# -*- coding: UTF-8 -*-


import sys

from lib.eodefault import *
from py_mixin import Simple


sobj = Simple(None)
print "ref: ", sobj.ref_get()

sobj.a_set(1)
sobj.b_set(2)
sobj.a_get()
sobj.b_get()
sobj.ab_sum_get()
sobj.ab_sum_get()
sobj.ab_sum_get()

print "end"


