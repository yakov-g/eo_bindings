/**
 * generated from "/home/yakov/xml/signals/simple.xml"
 */
#ifndef _JS_SIMPLE_H_
#define _JS_SIMPLE_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "simple.h" //eo-class include file
#include "_eobase.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class Simple : public virtual CElmObject, public virtual EoBase {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   Simple();
   Simple(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   struct {
      Persistent<Value> _event_ev_a_changed;
   } cb;

   virtual ~Simple();

public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<Simple>(const Arguments& args);

   Handle<Value> a_get() const;
   void a_set(Handle<Value> val);

   void b_set(Handle<Value> val);

   Handle<Value> c_get() const;

   Handle<Value> ev_a_changed_get() const;
   void ev_a_changed_set(Handle<Value> val);
   void ev_a_changed(void *event_info);
   static Eina_Bool ev_a_changed_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);


}; //end class

/* properties callbacks */
   Handle<Value> Callback_a_get(Local<String>, const AccessorInfo &info);
   void Callback_a_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_b_get(Local<String>, const AccessorInfo &info);
   void Callback_b_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_c_get(Local<String>, const AccessorInfo &info);
   void Callback_c_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* properties(events) callbacks */
   Handle<Value> Callback_ev_a_changed_get(Local<String>, const AccessorInfo &info);
   void Callback_ev_a_changed_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* methods callbacks */

} //end namespace elm

#endif
