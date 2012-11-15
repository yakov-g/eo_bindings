# -*- coding: UTF-8 -*-
import sys

#from base.eodefault import py_elm_init, elem_runi
from eobase import EoBase
#from evas_lib.py.evas_l import Evas, EvasObjectRectangle, EvasObjectLine
from evas_elem_l.py.evas_elem_py import Evas, EvasObjectRectangle, EvasObjectLine, ElmWin

ev = Evas(None)
rect = EvasObjectRectangle(ev)
line = EvasObjectLine(ev)

rect.color_set(255, 55, 0, 255)
r, g, b, a = rect.color_get()
print "%d %d %d %d"%(r, g, b, a)
print "=================="

line.xy_set(0, 0, 10, 20)
r, g, b, a = line.xy_get()
print "%d %d %d %d"%(r, g, b, a)
print "=================="


