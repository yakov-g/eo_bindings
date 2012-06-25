/**
 * generated from "/home/yakov/xml/mixin/simple.xml"
 */
#ifndef _JS_SIMPLE_H_
#define _JS_SIMPLE_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "simple.h" //eo-class include file
#include "_eobase.h" //include generated js-wrapping classes
#include "_mixin3.h" //include generated js-wrapping classes
#include "_mixin2.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class Simple : public virtual CElmObject, public virtual EoBase, public virtual Mixin3, public virtual Mixin2 {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   Simple();
   Simple(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   virtual ~Simple();

public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<Simple>(const Arguments& args);

   Handle<Value> a_get() const;
   void a_set(Handle<Value> val);
   Handle<Value> b_get() const;
   void b_set(Handle<Value> val);





}; //end class

/* properties callbacks */
   Handle<Value> Callback_a_get(Local<String>, const AccessorInfo &info);
   void Callback_a_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_b_get(Local<String>, const AccessorInfo &info);
   void Callback_b_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* properties(events) callbacks */

/* methods callbacks */

} //end namespace elm

#endif
