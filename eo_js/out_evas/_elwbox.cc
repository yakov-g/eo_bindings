/**
 * generated from "/home/yakov/xml/evas/elwbox.xml"
 */
#include "_elwbox.h"
namespace elm {

using namespace v8;




EO_GENERATE_METHOD_CALLBACKS(ElwBox, pack_end);


ElwBox::ElwBox(Local<Object> _jsObject, CElmObject *parent)
 : CElmObject(_jsObject, eo_add(ELW_BOX_CLASS , parent ? parent->GetEo() : NULL))
{
   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));
}
void ElwBox::DidRealiseElement(Local<Value> obj)
 {
                      (void) obj;
                      }

ElwBox::ElwBox(){}

ElwBox::~ElwBox(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(ELW_BOX_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(ELW_BOX_CLASS, eo_event_global_thaw());
 return Undefined();
}
Handle<Value> ElwBox::pack_end(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _obj = args[0];
   Eo* obj;
   obj = static_cast<CElmObject*>(_obj->ToObject()->GetPointerFromInternalField(0))->GetEo();
   eo_do(eobj, elw_box_pack_end(obj));
   return Undefined();
}

GENERATE_TEMPLATE(ElwBox,
PROPERTY(elements),
   PROPERTY(color),
   PROPERTY(position),
   PROPERTY(visibility),
   PROPERTY(size),
   PROPERTY(eo_ev_callback_add),
   PROPERTY(eo_ev_callback_del),
   PROPERTY(eo_ev_del),
   METHOD(pack_end),
   METHOD(event_thaw),
   METHOD(event_freeze),
   METHOD(event_freeze_get),
   METHOD(longlongs),
   METHOD(longs),
   METHOD(par_by_ref),
   METHOD(child_add),
   METHOD(ints),
   METHOD(no_par),
   METHOD(floats));
void ElwBox::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("ElwBox") , GetTemplate()->GetFunction());
EO_REGISTER_STATIC_METHOD(event_global_thaw);
EO_REGISTER_STATIC_METHOD(event_global_freeze);
}
} //end namespace elm
