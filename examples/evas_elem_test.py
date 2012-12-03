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
w1.elm_obj_win_title_set("first_title")
t = w1.elm_obj_win_title_get()
print "title:", t
w1.evas_obj_size_set(370, 350)
xx,yy = w1.evas_obj_size_get()
print "size : " ,  xx, yy
w1.evas_obj_visibility_set(1)
v = w1.evas_obj_visibility_get()
print "v=", v

bg = ElmBg(w1)
bg.evas_obj_size_hint_weight_set(1.0, 1.0)
w1.elm_obj_win_resize_object_add(bg)
bg.evas_obj_visibility_set(1)


box = ElmBox(w1)
box.evas_obj_size_hint_weight_set(1.0, 1.0)
w1.elm_obj_win_resize_object_add(box)
box.evas_obj_visibility_set(1)

but = ElmButton(w1)
box.elm_obj_box_pack_end(but)
but.evas_obj_visibility_set(1)
but.evas_obj_color_set(255, 255, 0, 255)
but.elm_wdg_text_part_set(None, "Button")

d = w1.elm_obj_win_screen_dpi_get()
print d
d = w1.elm_obj_win_role_get()
print d
#d = w1.fullscreen_set(1)


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

