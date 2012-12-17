# -*- coding: UTF-8 -*-

from simple.py.simple_py import Simple, Mixin, Interface

so = Simple(None)

so.a_set(4)

a = so.a_get()
a2 = so.a_square_get()
a3 = so.a_power_3_get()

print "a = %d; a^2 = %d; a^3 = %d " %(a, a2, a3)

