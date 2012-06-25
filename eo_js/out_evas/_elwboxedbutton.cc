/**
 * generated from "/home/yakov/xml/evas/elwboxedbutton.xml"
 */
#include "_elwboxedbutton.h"
namespace elm {

using namespace v8;






ElwBoxedbutton::ElwBoxedbutton(Local<Object> _jsObject, CElmObject *parent)
 : CElmObject(_jsObject, eo_add(ELW_BOXEDBUTTON_CLASS , parent ? parent->GetEo() : NULL))
{
   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));
}
void ElwBoxedbutton::DidRealiseElement(Local<Value> obj)
 {
                      (void) obj; 
                      }

ElwBoxedbutton::ElwBoxedbutton(){}

ElwBoxedbutton::~ElwBoxedbutton(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(ELW_BOXEDBUTTON_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(ELW_BOXEDBUTTON_CLASS, eo_event_global_thaw());
 return Undefined();
}
GENERATE_TEMPLATE(ElwBoxedbutton,
PROPERTY(elements),
   PROPERTY(color),
   PROPERTY(position),
   PROPERTY(visibility),
   PROPERTY(size),
   PROPERTY(text),
   PROPERTY(eo_ev_callback_add),
   PROPERTY(eo_ev_callback_del),
   PROPERTY(eo_ev_del),
   PROPERTY(ev_clicked),
   METHOD(alert),
   METHOD(event_thaw),
   METHOD(event_freeze),
   METHOD(event_freeze_get),
   METHOD(pack_end),
   METHOD(longlongs),
   METHOD(longs),
   METHOD(par_by_ref),
   METHOD(child_add),
   METHOD(ints),
   METHOD(no_par),
   METHOD(floats));
void ElwBoxedbutton::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("ElwBoxedbutton") , GetTemplate()->GetFunction());
EO_REGISTER_STATIC_METHOD(event_global_thaw);
EO_REGISTER_STATIC_METHOD(event_global_freeze);
}
} //end namespace elm
