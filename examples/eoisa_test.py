# -*- coding: UTF-8 -*-

from eoisa.eoisa_py import Simple, Complex, Mixin, Interface

so = Simple(None)
co = Complex(None)

print "Simple: isa-simple: %s; isa-complex: %s; isa-mixin: %s; isa-interface %s"%\
(isinstance(so, Simple), isinstance(so, Complex), isinstance(so, Mixin), isinstance(so, Interface))
print "Complex: isa-simple: %s; isa-complex: %s; isa-mixin: %s; isa-interface %s"%\
(isinstance(co, Simple), isinstance(co, Complex), isinstance(co, Mixin), isinstance(co, Interface))

so.a_set(4)

a = so.a_get()
a2 = so.a_square_get()
a3 = so.a_power_3_get()

print "a = %d; a^2 = %d; a^3 = %d " %(a, a2, a3)

