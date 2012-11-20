# -*- coding: UTF-8 -*-
import sys

from base.eodefault import py_elm_init, elem_run
#from eobase import EoBase
#from evas_lib.py.evas_l import Evas, EvasObjectRectangle, EvasObjectLine
from evas_elem_l.py.evas_elem_py import ElmWin, ElmBg, ElmBox, ElmButton

print "Initializing Elementary..."
print "Init res:", py_elm_init(sys.argv)
print ""

w1 = ElmWin(None, "my win name", 0)
w1.title_set("first_title")
t = w1.title_get()
print "title:", t
w1.size_set(370, 350)
xx,yy = w1.size_get()
print "size : " ,  xx, yy
w1.visibility_set(1)
v = w1.visibility_get()
print "v=", v

bg = ElmBg(w1)
bg.size_hint_weight_set(1.0, 1.0)
w1.resize_object_add(bg)
bg.visibility_set(1)


box = ElmBox(w1)
box.size_hint_weight_set(1.0, 1.0)
w1.resize_object_add(box)
box.visibility_set(1)

but = ElmButton(w1)
#but.text_set("Button")
box.pack_end(but)
but.visibility_set(1)

d = w1.screen_dpi_get()
print d
d = w1.role_get()
print d
d = w1.fullscreen_set(1)


elem_run()

"""
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
"""

