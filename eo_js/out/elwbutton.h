########################################################
##
## generated from from "/tmp/evas_py/l/elwbutton.xml"
##
########################################################

#ifndef _JS_ELWBUTTON_H_
#define _JS_ELWBUTTON_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_button.h" //eo-class include file
#include "evasobject.h" //include generated js-wrapping classes
#include "elwalert.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwButton : public virtual CElmObject, public virtual EvasObject, public virtual ElwAlert {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   ElwButton();
   ElwButton(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   virtual ~ElwButton();
public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<ElwButton>(const Arguments& args);


cdef extern from "elw_button.h":

  Eo_Op ELW_BUTTON_BASE_ID

  Eo_Event_Description * EV_CLICKED

  ctypedef enum:
    ELW_BUTTON_SUB_ID_TEXT_SET

  Eo_Class* elw_button_class_get()

}; //end class

} //end namespace elm

#endif

