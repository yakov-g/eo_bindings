# -*- coding: UTF-8 -*-


import sys

from base.eodefault import *
from mixin.mixin_py import Simple


sobj = Simple(None)
print "ref: ", sobj.ref_get()

sobj.a_set(1)
sobj.b_set(2)
sobj.a_get()
sobj.b_get()
sobj.ab_sum_get()
sobj.ab_sum_get()
sobj.ab_sum_get()

super(Simple,sobj).ab_sum_get()

print "end"


