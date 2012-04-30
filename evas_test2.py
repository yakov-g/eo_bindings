# -*- coding: UTF-8 -*-

from c_eobj import *
#from evasobj import *
from elwwin import *

from elwboxedbutton import *

import sys


print "Initializing..."
init()
print ""

print sys.argv, "  ", len(sys.argv)
print ' '.join(sys.argv)

print "Initializing Elementary..."
print "Init res:", py_elm_init(sys.argv)

print ""



w = ElwWin(None)
w.size_set(400, 400)
w.visibility_set(1)






bb = ElwBoxedButton(w);

bb.visibility_set(1)
bb.position_set(100, 100)
bb.size_set(70, 50)
bb.color_set(0, 255, 255, 255)
bb.text_set("(BB) DEL cb")





"""
bb2 = BB(w)
bb2.visibility_set(1)
bb2.position_set(70, 160)
bb2.size_set(40, 40)
bb2.color_set(128, 255, 128, 255)
bb2.text_set("BB")
bb2.some_box_function()
"""

print "Running Elementary..."
elem_run()

