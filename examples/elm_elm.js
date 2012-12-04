//var elm = require('jse');
var elm = require('jsevaselm');

//var m = new elm.Mixin()

function cb_add(par){
  print(par.text + ": calback_added")
}

function cb_del(par){
  print(par.text + ": calback_deleted")
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
  print("callback called for: " + par.text)
     /*
  par.alert("getting size")

  o = par.size
  par.alert("W: " + o.w)
  par.alert("H: " + o.h)

  o = par.position
  par.alert("X: " + o.x)
  par.alert("Y: " + o.y)
  */
}


var win = elm.ElmWin({
    evas_obj_size: { w: 300, h: 350},
    elm_obj_win_title: "My JS window",

    elements: {
        bg: elm.ElmBg({
                         // text: "Hello",
                          evas_obj_size: {w: 210, h: 60},
                          elm_obj_bg_color: {r: 0, g: 245, b: 255, a: 255},
                    }),
        shalom_bt: elm.ElmButton({
                         // text: "Hello",
                          evas_obj_position : {x: 30, y: "asdf"},
                          evas_obj_size: {w: 210, h: 60},
                          evas_obj_color: {r: 159, g: 245, b: 255, a: 255},
        /*
                          eo_ev_callback_add : cb_add,
                          eo_ev_callback_del : cb_del,
                          ev_clicked : cb3
                          */
                    }),
        ba: elm.ElmButton({
//                          text: "(B) ADD cb",
                          evas_obj_position : {x: 30, y: 100},
                          evas_obj_size: {w: 100, h: 50},
                          evas_obj_color: {r: 255, g: 0, b: 255, a: 255},
//                          evas_obj_visibility : false,
  //                        ev_clicked : cb3
                    }),

    }
    
});
/*
var w = elm.ElwWin({
    size: { w: 300, h: 350},
    elements: {


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
*/
var w = elm.realise(win);

print ("=========  DPI  ========")
print (w.elm_obj_win_screen_dpi)
print ("====================")

print ("==== call for bitton size =====")
var s = w.elements.ba.evas_obj_size
print (s)
print ("==== end call for button size =====")

print ("==== Window size =====")
print( w.evas_obj_size )
print ("====================")

//var dpi = e.elements.w.elm_obj_win_screen_dpi
//print ("DPI: " + dpi)

print ("====================")
print (w.elm_obj_win_aspect)
w.elm_obj_win_center(1, 1)



w.elements.ba.evas_obj_visibility = false
w.elements.ba.elm_wdg_text_part_set(null, "Button")
w.elements.ba.evas_obj_visibility = true
var t = w.elements.ba.elm_wdg_text_part_get(null)
print ("====================")
print(t)
print ("====================")

/*

e.elements.box.pack_end(e.elements.but1)

e.elements.box.pack_end(e.elements.but2)
e.elements.ebb.pack_end(e.elements.pb)

//e.elements.shalom_bt.eo_ev_callback_add = cb_add
e.elements.shalom_bt.ev_clicked = cb3



elm.ElwWin.event_global_freeze()
elm.ElwWin.event_global_thaw()





*/
