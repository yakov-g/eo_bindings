/**
 * generated from "/home/yakov/xml/evas/elwbox.xml"
 */
#ifndef _JS_ELWBOX_H_
#define _JS_ELWBOX_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "elw_box.h" //eo-class include file
#include "_evasobject.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwBox : public virtual CElmObject, public virtual EvasObject {
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





   Handle<Value> pack_end(const Arguments&);

}; //end class

/* properties callbacks */

/* properties(events) callbacks */

/* methods callbacks */
   Handle<Value> Callback_pack_end(const Arguments&);

} //end namespace elm

#endif
