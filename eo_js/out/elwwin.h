/**
 * generated from "/tmp/evas_py/l/elwwin.xml"
 */
#ifndef _JS_ELWWIN_H_
#define _JS_ELWWIN_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_win.h" //eo-class include file
#include "evasobject.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwWin : public virtual CElmObject, public virtual EvasObject {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   ElwWin();
   ElwWin(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   virtual ~ElwWin();

public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<ElwWin>(const Arguments& args);




}; //end class

/* properties callbacks */

/* properties(events) callbacks */

/* methods callbacks */

} //end namespace elm

#endif
