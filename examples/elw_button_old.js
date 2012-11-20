var elm = require('elm');
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

 // par.floats(0.6, 43.345)
  print (" ===  Testing floats ===")
  a = 7.32
  b = -21474.5134
  o = par.floats(a, b) 

  par.alert("bb: " + o.bb)
  par.alert("cc: " + o.cc)


}

function cb3(par){
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
                          text: "שלום",
                          position : { x: 30, y: 30},
                          size: { w: 210, h: 60},
                          color: { r: 159, g: 245, b: 255, a: 255},
                          eo_ev_callback_add : cb_add,
                          eo_ev_callback_del : cb_del,
                          ev_clicked : cb3
                    }),

        ba: elm.ElwButton({
                          text: "(B) ADD cb",
                          position : { x: 30, y: 100},
                          size: { w: 100, h: 50},
                          color: { r: 255, g: 0, b: 255, a: 255},
                          ev_clicked : cb3
                    }),

        red_bt: elm.ElwBoxedbutton({
                        text: "Красная кнопка",
                        position : { x: 140, y: 100},
                         size: { w: 100, h: 50},
                         color: { r: 255, g: 0, b: 5, a: 255},
                      //ev_clicked : cb2

                    }),

        but1: elm.ElwButton({
                        text: "1st but in box (thaw_cb)",
                      //position : { x: 250, y: 100},
                      //size: { w: 90, h: 20},
                        color: { r: 255, g: 0, b: 255, a: 255},
                        ev_clicked : thaw_cb
                    }),

        but2: elm.ElwButton({
                        text: "2nd but in box (freeze_this)",
                      //position : { x: 270, y: 150},
                      //size: { w: 90, h: 50},
                        color: { r: 240, g: 240, b: 0, a: 255},
                        ev_clicked : freeze_this

                    }),

                    box : elm.ElwBox ({
                     position : {x: 140, y: 170},
                     size: { w: 50, h: 100},

                     }),

        pb: elm.ElwButton({
                        text: "But in BB (num)",
                      //     position : { x: 310, y: 150},
                      //   size: { w: 70, h: 50},
                         color: { r: 240, g: 240, b: 245, a: 255},
                         ev_clicked : numbers_cb

                    }),

        ebb: elm.ElwBoxedbutton({
                        text: "BoxedButton",
                         position : { x: 30, y: 170},
                         size: { w: 100, h: 50},
                         color: { r: 100, g: 85, b: 255, a: 255},
                         //ev_clicked : freeze_all,
                    }),

/*
        bb2: elm.ElwBoxedbutton({
                        text: "BoxedButton",
//                         mixin: "hello, שלום, привет",
                           position : { x: 180, y: 250},
                         size: { w: 100, h: 65},
                         color: { r: 0, g: 255, b: 0, a: 255},
                         ev_clicked : cb2,
    //                     on_test : cb1,

/*
                    disabled1: elm.Button({
                        text: "Dis1",
                        x: 10,
                         y: 160,
                        width: 100,
                        height: 15,
                        enabled: true,
                        on_click : ff,
                    }),

                    disabled2: elm.Button({
                        text: "Dis2",
                        x: 10,
                         y: 190,
                        width: 100,
                        height: 15,
                        enabled: true,
                         on_click : ff,
                    }),
*/
/*
        bb2: elm.ElwBoxedbutton({
                        text: "BoxedButton",
//                         mixin: "hello, שלום, привет",
                           position : { x: 180, y: 250},
                         size: { w: 100, h: 65},
                         color: { r: 0, g: 255, b: 0, a: 255},
                         ev_clicked : cb2,
    //                     on_test : cb1,

                           elements : {
                                        label_only: elm.ElwButton({
                                        color: { r: 10, g: 20, b: 30, a: 255},
                                        text: "button in the boxedbutton!",
                                        size: { w: 80, h: 65},
                                       }),
                                    },
                    }),
*/

/*
                    disabled: elm.Button({
                        text: "Don",
                        x: 10,
                         y: 160,
                        width: 100,
                        height: 300,
                        enabled: true
                    }),

                    label_only: elm.Button({
                    weight: { x: 1.0, y: 1.0 },
                        style: "anchor",
                        text: "hello!",
                        x: 110,
                         y: 260,
                         width: 80,
                         height: 65
                    }),
*/
/*
                    hbox2 : elm.ElwBox ({
                     position : {x: 90, y: 180},

                   elements : {
                                label_only2: elm.ElwButton({
                                text: "button in the box! + exit()",
                                // pos : {x: 110, y: 260},
                                 color: { r: 0, g: 5, b: 255, a: 255},
                                 size: { w: 80, h: 65},
                                 on_test: function(par){
                                             par.alert("close application")
                                             elm.exit()
                                            }
                                 
                                 }),
                            },
                     }),
*/

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



