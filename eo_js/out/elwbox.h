########################################################
##
## generated from from "/tmp/evas_py/l/elwbox.xml"
##
########################################################

#ifndef _JS_ELWBOX_H_
#define _JS_ELWBOX_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_box.h" //eo-class include file
#include "evasobject.h" //include generated js-wrapping classes
#include "elwalert.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwBox : public virtual CElmObject, public virtual EvasObject, public virtual ElwAlert {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   ElwBox();
   ElwBox(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   virtual ~ElwBox();
public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<ElwBox>(const Arguments& args);


cdef extern from "elw_box.h":

  Eo_Op ELW_BOX_BASE_ID


  ctypedef enum:
    ELW_BOX_SUB_ID_PACK_END

  Eo_Class* elw_box_class_get()

}; //end class

} //end namespace elm

#endif

