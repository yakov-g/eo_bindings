/**
 * generated from "/home/yakov/xml/evas/elwwin.xml"
 */
#include "_elwwin.h"
namespace elm {

using namespace v8;






ElwWin::ElwWin(Local<Object> _jsObject, CElmObject *parent)
 : CElmObject(_jsObject, eo_add(ELW_WIN_CLASS , parent ? parent->GetEo() : NULL))
{
   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));
}
void ElwWin::DidRealiseElement(Local<Value> obj)
 {
                      (void) obj; 
                      }

ElwWin::ElwWin(){}

ElwWin::~ElwWin(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(ELW_WIN_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(ELW_WIN_CLASS, eo_event_global_thaw());
 return Undefined();
}
GENERATE_TEMPLATE(ElwWin,
PROPERTY(elements),
   PROPERTY(color),
   PROPERTY(position),
   PROPERTY(visibility),
   PROPERTY(size),
   PROPERTY(eo_ev_callback_add),
   PROPERTY(eo_ev_callback_del),
   PROPERTY(eo_ev_del),
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
void ElwWin::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("ElwWin") , GetTemplate()->GetFunction());
EO_REGISTER_STATIC_METHOD(event_global_thaw);
EO_REGISTER_STATIC_METHOD(event_global_freeze);
}
} //end namespace elm
