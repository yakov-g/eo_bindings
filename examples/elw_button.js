//var elm = require('jse');
var elm = require('jse');

//var m = new elm.Mixin()

function cb_add(par){
  par.alert(par.text + ": calback_added")
}

function cb_del(par){
  par.alert(par.text + ": calback_deleted")
}

//==============================
var global_obj

function freeze_this(par){
  par.alert("Object: " + par.text)
  par.alert("Freezing cb for this obj")
  global_obj = par
  par.event_freeze()
  par.alert("Freeze count = " + par.event_freeze_get())
}

function thaw_cb(par){
  par.alert("Thawing cb for global_obj")
  global_obj.event_thaw()  
}
//==================================

function numbers_cb(par){
  par.alert("numbers_cb")
  par.no_par()

  par.ints(0, 0)
  print (" ===  Testing int ===")

  o = par.ints(1, 2, 3) 
  par.alert("xx: " + o.xx)
  par.alert("yy: " + o.yy)

  par.par_by_ref(1, 2, 3)


  print (" ===  Testing floats ===")
  a = 7.32
  b = -21474.5134
  o = par.floats(a, b) 

  par.alert("bb: " + o.bb)
  par.alert("cc: " + o.cc)
}

function cb3(par)
{
  par.alert("callback called for: " + par.text)
  par.alert("getting size")

  o = par.size
  par.alert("W: " + o.w)
  par.alert("H: " + o.h)

  o = par.position
  par.alert("X: " + o.x)
  par.alert("Y: " + o.y)
}



var w = elm.ElwWin({
    size: { w: 300, h: 350},
    elements: {
        shalom_bt: elm.ElwButton({
                          text: "Hello",
                          position : {x: 30, y: 30},
                          size: {w: 210, h: 60},
                          color: {r: 159, g: 245, b: 255, a: 255},
                          eo_ev_callback_add : cb_add,
                          eo_ev_callback_del : cb_del,
                          ev_clicked : cb3
                    }),

        ba: elm.ElwButton({
                          text: "(B) ADD cb",
                          position : {x: 30, y: 100},
                          size: {w: 100, h: 50},
                          color: {r: 255, g: 0, b: 255, a: 255},
                          ev_clicked : cb3
                    }),

        red_bt: elm.ElwBoxedbutton({
                        text: "Red button",
                        position : {x: 140, y: 100},
                        size: {w: 100, h: 50},
                        color: {r: 255, g: 0, b: 5, a: 255},
                        ev_clicked : cb3

                    }),

        but1: elm.ElwButton({
                        text: "1st but in box",
                      //position : { x: 250, y: 100},
                      //size: { w: 90, h: 20},
                        color: { r: 255, g: 0, b: 255, a: 255},
                        ev_clicked : thaw_cb
                    }),

        but2: elm.ElwButton({
                        text: "2nd but in box",
                      //position : { x: 270, y: 150},
                      //size: { w: 90, h: 50},
                        color: {r: 240, g: 240, b: 0, a: 255},
                        ev_clicked : freeze_this
                    }),

                    box : elm.ElwBox ({
                        position : {x: 140, y: 170},
                        size: {w: 100, h: 50},
                     }),

        pb: elm.ElwButton({
                        text: "But in BB (num)",
                      //position : { x: 310, y: 150},
                      //size: { w: 70, h: 50},
                        color: {r: 240, g: 240, b: 245, a: 255},
                        ev_clicked : numbers_cb
                    }),

        ebb: elm.ElwBoxedbutton({
                        text: "BoxedButton",
                         position : {x: 30, y: 170},
                         size: { w: 100, h: 50},
                         color: { r: 100, g: 85, b: 255, a: 255},
                         //ev_clicked : freeze_all,
                    }),
    }
});


var e = elm.realise(w);


e.elements.box.pack_end(e.elements.but1)
e.elements.box.pack_end(e.elements.but2)
e.elements.ebb.pack_end(e.elements.pb)

//e.elements.shalom_bt.eo_ev_callback_add = cb_add
e.elements.shalom_bt.ev_clicked = cb3



elm.ElwWin.event_global_freeze()
elm.ElwWin.event_global_thaw()






