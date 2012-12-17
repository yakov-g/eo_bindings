//var elm = require('jse');
var elm = require('jse');
//var elm = require('/opt/e17/lib/elev8/linux-gnu-i686-0.1.0/libjse.so');

//var m = new elm.Mixin()

function cb_add(par){
  par.elw_alert_alert(par.elw_button_text + ": calback_added")
}

function cb_del(par){
  par.elw_alert_alert(par.elw_button_text + ": calback_deleted")
}

//==============================
var global_obj

function freeze_this(par){
  par.elw_alert_alert("Object: " + par.elw_button_text)
  par.elw_alert_alert("Freezing cb for this obj")
  global_obj = par
  par.event_freeze()
  par.elw_alert_alert("Freeze count = " + par.event_freeze_get())
}

function thaw_cb(par){
  par.elw_alert_alert("Thawing cb for global_obj")
  global_obj.event_thaw()  
}
//==================================

function numbers_cb(par){
  par.elw_alert_alert("numbers_cb")
  par.no_par()

  par.ints(0, 0)
  print (" ===  Testing int ===")

  o = par.ints(1, 2, 3) 
  par.elw_alert_alert("xx: " + o.xx)
  par.elw_alert_alert("yy: " + o.yy)

  par.par_by_ref(1, 2, 3)


  print (" ===  Testing floats ===")
  a = 7.32
  b = -21474.5134
  o = par.floats(a, b) 

  par.elw_alert_alert("bb: " + o.bb)
  par.elw_alert_alert("cc: " + o.cc)
}

function cb3(par, f)
{
  print(par)
  print(f)
  par.elw_alert_alert("callback called for: " + par.elw_button_text)
  par.elw_alert_alert("getting size")

  o = par.exevas_obj_size
  par.elw_alert_alert("W: " + o.w)
  par.elw_alert_alert("H: " + o.h)

  o = par.exevas_obj_position
  par.elw_alert_alert("X: " + o.x)
  par.elw_alert_alert("Y: " + o.y)
}



var w = elm.ElwWin({
    exevas_obj_size: { w: 300, h: 350},
    elements: {
        shalom_bt: elm.ElwButton({
                          elw_button_text: "Hello",
                          exevas_obj_position : {x: 30, y: 30},
                          exevas_obj_size: {w: 210, h: 60},
                          exevas_obj_color: {r: 159, g: 245, b: 255, a: 255},
                          eo_ev_callback_add : cb_add,
                          eo_ev_callback_del : cb_del,
                          ev_clicked : cb3
                    }),

        ba: elm.ElwButton({
                          elw_button_text: "(B) ADD cb",
                          exevas_obj_position : {x: 30, y: 100},
                          exevas_obj_size: {w: 100, h: 50},
                          exevas_obj_color: {r: 255, g: 0, b: 255, a: 255},
                          ev_clicked : cb3
                    }),

        red_bt: elm.ElwBoxedbutton({
                        elw_button_text: "Red button",
                        exevas_obj_position : {x: 140, y: 100},
                        exevas_obj_size: {w: 100, h: 50},
                        exevas_obj_color: {r: 255, g: 0, b: 5, a: 255},
                        ev_clicked : cb3

                    }),

        but1: elm.ElwButton({
                        elw_button_text: "1st but in box",
                      //exevas_obj_position : { x: 250, y: 100},
                      //exevas_obj_size: { w: 90, h: 20},
                        exevas_obj_color: { r: 255, g: 0, b: 255, a: 255},
                        ev_clicked : thaw_cb
                    }),

        but2: elm.ElwButton({
                        elw_button_text: "2nd but in box",
                      //exevas_obj_position : { x: 270, y: 150},
                      //exevas_obj_size: { w: 90, h: 50},
                        exevas_obj_color: {r: 240, g: 240, b: 0, a: 255},
                        ev_clicked : freeze_this
                    }),

                    box : elm.ElwBox ({
                        exevas_obj_position : {x: 140, y: 170},
                        exevas_obj_size: {w: 100, h: 50},
                     }),

        pb: elm.ElwButton({
                        elw_button_text: "But in BB (num)",
                      //exevas_obj_position : { x: 310, y: 150},
                      //exevas_obj_size: { w: 70, h: 50},
                        exevas_obj_color: {r: 240, g: 240, b: 245, a: 255},
                        ev_clicked : numbers_cb
                    }),

        ebb: elm.ElwBoxedbutton({
                        elw_button_text: "BoxedButton",
                         exevas_obj_position : {x: 30, y: 170},
                         exevas_obj_size: { w: 100, h: 50},
                         exevas_obj_color: { r: 100, g: 85, b: 255, a: 255},
                         //ev_clicked : freeze_all,
                    }),
    }
});


var e = elm.realise(w);


e.elements.box.elw_box_pack_end(e.elements.but1)
e.elements.box.elw_box_pack_end(e.elements.but2)
e.elements.ebb.elw_box_pack_end(e.elements.pb)

//e.elements.shalom_bt.eo_ev_callback_add = cb_add
e.elements.shalom_bt.ev_clicked = cb3



elm.ElwWin.event_global_freeze()
elm.ElwWin.event_global_thaw()






