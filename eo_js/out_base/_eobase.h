/**
 * generated from "/home/yakov/xml/base/eobase.xml"
 */
#ifndef _JS_EOBASE_H_
#define _JS_EOBASE_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "Eo.h" //eo-class include file

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class EoBase : public virtual CElmObject {
private:
protected:
   EoBase();
   struct {
      Persistent<Value> _event_eo_ev_callback_add;
      Persistent<Value> _event_eo_ev_callback_del;
      Persistent<Value> _event_eo_ev_del;
   } cb;

   virtual ~EoBase();

public:



   Handle<Value> eo_ev_callback_add_get() const;
   void eo_ev_callback_add_set(Handle<Value> val);
   void eo_ev_callback_add(void *event_info);
   static Eina_Bool eo_ev_callback_add_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);
   Handle<Value> eo_ev_callback_del_get() const;
   void eo_ev_callback_del_set(Handle<Value> val);
   void eo_ev_callback_del(void *event_info);
   static Eina_Bool eo_ev_callback_del_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);
   Handle<Value> eo_ev_del_get() const;
   void eo_ev_del_set(Handle<Value> val);
   void eo_ev_del(void *event_info);
   static Eina_Bool eo_ev_del_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);

   Handle<Value> event_thaw(const Arguments&);
   Handle<Value> event_freeze(const Arguments&);
   Handle<Value> event_freeze_get(const Arguments&);

}; //end class

/* properties callbacks */

/* properties(events) callbacks */
   Handle<Value> Callback_eo_ev_callback_add_get(Local<String>, const AccessorInfo &info);
   void Callback_eo_ev_callback_add_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_eo_ev_callback_del_get(Local<String>, const AccessorInfo &info);
   void Callback_eo_ev_callback_del_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_eo_ev_del_get(Local<String>, const AccessorInfo &info);
   void Callback_eo_ev_del_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* methods callbacks */
   Handle<Value> Callback_event_global_thaw(const Arguments&);
   Handle<Value> Callback_event_thaw(const Arguments&);
   Handle<Value> Callback_event_global_freeze(const Arguments&);
   Handle<Value> Callback_event_freeze(const Arguments&);
   Handle<Value> Callback_event_freeze_get(const Arguments&);

} //end namespace elm

#endif
