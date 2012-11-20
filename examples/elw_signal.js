var elm = require('jssimple');


function cb_add(par){
  print("Callback on callback adding")
}

var poo = function(pa){
  print("Callback on changing: a = " + pa.a);
}


var ms = new elm.Simple()

print("\nSetting a...")
ms.a = 12345678
print("a = " + ms.a + "\n")

print("\nAdding callback...")
ms.eo_ev_callback_add = cb_add
ms.ev_a_changed = poo

print("\nSetting b(a) to 896...")
ms.b = 896
print("Reading \"b\" (no getter for \"b\" prop): " + ms.b)


print("\nSetting c(a) to 123...")
ms.c = 123
print("Reading \"c\" (no setter for \"c\" prop, so it should be 896): " + ms.c + "\n")



print("\nFreezing callback...")
ms.event_freeze()
ms.a = 123

print("\nThawing callback...")
ms.event_thaw()
ms.a = 123



/*

var ss = elm.realise(elm.Simple({a:5, on_change:poo, b:55}))

ss.ev_a_changed = cb
ss.a = 123
*/

elm.exit()


