/**
 * generated from "/tmp/evas_py/l/elwboxedbutton.xml"
 */
#ifndef _JS_ELWBOXEDBUTTON_H_
#define _JS_ELWBOXEDBUTTON_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_boxedbutton.h" //eo-class include file
#include "elwbox.h" //include generated js-wrapping classes
#include "elwbutton.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwBoxedbutton : public virtual CElmObject, public virtual ElwBox, public virtual ElwButton {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   ElwBoxedbutton();
   ElwBoxedbutton(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   virtual ~ElwBoxedbutton();

public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<ElwBoxedbutton>(const Arguments& args);




}; //end class

/* properties callbacks */

/* properties(events) callbacks */

/* methods callbacks */

} //end namespace elm

#endif
