//var elm = require('jstest');
var elm = require('jseoisa');

var so = new elm.Simple()

so.a = 2
a = so.a
a2 = so.a_square
a3 = so.a_power_3
print("a = " + a + "; a^2 = " + a2 + "; a^3 = " + a3)

print("*******************************\n")


var co = new elm.Complex()
co.a = 3
a = co.a
a2 = co.a_square
a3 = co.a_power_3
print("a = " + a + "; a^2 = " + a2 + "; a^3 = " + a3)

elm.exit()


