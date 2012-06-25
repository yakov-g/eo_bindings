/**
 * generated from "/home/yakov/xml/base/eobase.xml"
 */
#include "_eobase.h"
namespace elm {

using namespace v8;




EO_GENERATE_METHOD_CALLBACKS(EoBase, event_thaw);
EO_GENERATE_METHOD_CALLBACKS(EoBase, event_freeze);
EO_GENERATE_METHOD_CALLBACKS(EoBase, event_freeze_get);

EO_GENERATE_PROPERTY_CALLBACKS(EoBase, eo_ev_callback_add);
EO_GENERATE_PROPERTY_CALLBACKS(EoBase, eo_ev_callback_del);
EO_GENERATE_PROPERTY_CALLBACKS(EoBase, eo_ev_del);

EoBase::EoBase(){}

EoBase::~EoBase(){} //need to add destruction of cb variables

void EoBase::eo_ev_callback_add(void *event_info) //parse of event_info need to be added 
{
  Handle<Function> callback(Function::Cast(*cb._event_eo_ev_callback_add));
  Handle<Value> args[1] = {jsObject};
  callback->Call(jsObject, 1, args);
}

Eina_Bool EoBase::eo_ev_callback_add_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)
{
                           HandleScope scope;
                           static_cast<EoBase*>(data)->eo_ev_callback_add(event_info);
                           return EINA_TRUE;
                           (void) obj;
                           (void) desc;
                       }

Handle<Value> EoBase::eo_ev_callback_add_get() const
{
                           return cb._event_eo_ev_callback_add;
                       }

void EoBase::eo_ev_callback_add_set(Handle<Value> val)
{
  if (!val->IsFunction())
                           return;
  if (!cb._event_eo_ev_callback_add.IsEmpty())
                         {
                            cb._event_eo_ev_callback_add.Dispose();
                            cb._event_eo_ev_callback_add.Clear();
                            eo_do(eobj, eo_event_callback_del(EO_EV_CALLBACK_ADD, eo_ev_callback_add_wrapper, this));
                         }
  cb._event_eo_ev_callback_add = Persistent<Value>::New(val);
                         eo_do(eobj, eo_event_callback_add(EO_EV_CALLBACK_ADD, eo_ev_callback_add_wrapper, this));
}

void EoBase::eo_ev_callback_del(void *event_info) //parse of event_info need to be added 
{
  Handle<Function> callback(Function::Cast(*cb._event_eo_ev_callback_del));
  Handle<Value> args[1] = {jsObject};
  callback->Call(jsObject, 1, args);
}

Eina_Bool EoBase::eo_ev_callback_del_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)
{
                           HandleScope scope;
                           static_cast<EoBase*>(data)->eo_ev_callback_del(event_info);
                           return EINA_TRUE;
                           (void) obj;
                           (void) desc;
                       }

Handle<Value> EoBase::eo_ev_callback_del_get() const
{
                           return cb._event_eo_ev_callback_del;
                       }

void EoBase::eo_ev_callback_del_set(Handle<Value> val)
{
  if (!val->IsFunction())
                           return;
  if (!cb._event_eo_ev_callback_del.IsEmpty())
                         {
                            cb._event_eo_ev_callback_del.Dispose();
                            cb._event_eo_ev_callback_del.Clear();
                            eo_do(eobj, eo_event_callback_del(EO_EV_CALLBACK_DEL, eo_ev_callback_del_wrapper, this));
                         }
  cb._event_eo_ev_callback_del = Persistent<Value>::New(val);
                         eo_do(eobj, eo_event_callback_add(EO_EV_CALLBACK_DEL, eo_ev_callback_del_wrapper, this));
}

void EoBase::eo_ev_del(void *event_info) //parse of event_info need to be added 
{
  Handle<Function> callback(Function::Cast(*cb._event_eo_ev_del));
  Handle<Value> args[1] = {jsObject};
  callback->Call(jsObject, 1, args);
}

Eina_Bool EoBase::eo_ev_del_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)
{
                           HandleScope scope;
                           static_cast<EoBase*>(data)->eo_ev_del(event_info);
                           return EINA_TRUE;
                           (void) obj;
                           (void) desc;
                       }

Handle<Value> EoBase::eo_ev_del_get() const
{
                           return cb._event_eo_ev_del;
                       }

void EoBase::eo_ev_del_set(Handle<Value> val)
{
  if (!val->IsFunction())
                           return;
  if (!cb._event_eo_ev_del.IsEmpty())
                         {
                            cb._event_eo_ev_del.Dispose();
                            cb._event_eo_ev_del.Clear();
                            eo_do(eobj, eo_event_callback_del(EO_EV_DEL, eo_ev_del_wrapper, this));
                         }
  cb._event_eo_ev_del = Persistent<Value>::New(val);
                         eo_do(eobj, eo_event_callback_add(EO_EV_DEL, eo_ev_del_wrapper, this));
}

Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(EO_BASE_CLASS, eo_event_global_thaw());
 return Undefined();
}
Handle<Value> EoBase::event_thaw(const Arguments& args)
{
   HandleScope scope;
   eo_do(eobj, eo_event_thaw());
   return Undefined();
}

Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(EO_BASE_CLASS, eo_event_global_freeze());
 return Undefined();
}
Handle<Value> EoBase::event_freeze(const Arguments& args)
{
   HandleScope scope;
   eo_do(eobj, eo_event_freeze());
   return Undefined();
}

Handle<Value> EoBase::event_freeze_get(const Arguments& args)
{
   HandleScope scope;
   int fcount;
   eo_do(eobj, eo_event_freeze_get(&fcount));
   return scope.Close(Number::New(fcount));//need to put proper values
}


} //end namespace elm
