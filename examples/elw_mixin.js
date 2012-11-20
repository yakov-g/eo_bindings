var elm = require('jsmixin');

var obj1 = new elm.Simple({a:5, b:5})

obj1.a = 1
obj1.b = 2
sum = obj1.ab_sum

print("Sum for obj1: " + sum)


var obj2 = elm.Simple({a:3, b:4})
var e = elm.realise(obj2)

sum = e.ab_sum
print("Sum for obj1: " + sum)

elm.exit()
