# -*- coding: UTF-8 -*-


import sys

from base.eodefault import *
from mixin.py.mixin_py import Simple


sobj = Simple(None)

sobj.a_set(1)
sobj.b_set(2)
a = sobj.a_get()
b = sobj.b_get()
s = sobj.ab_sum_get()
print a + b + 2 == s
"""
sobj.ab_sum_get()
sobj.ab_sum_get()
"""

print "suuuuper..."
super(Simple,sobj).ab_sum_get()

print "end"


