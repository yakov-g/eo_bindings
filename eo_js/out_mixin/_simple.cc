/**
 * generated from "/home/yakov/xml/mixin/simple.xml"
 */
#include "_simple.h"
namespace elm {

using namespace v8;

EO_GENERATE_PROPERTY_CALLBACKS(Simple, a);
EO_GENERATE_PROPERTY_CALLBACKS(Simple, b);





Simple::Simple(Local<Object> _jsObject, CElmObject *parent)
 : CElmObject(_jsObject, eo_add(SIMPLE_CLASS , parent ? parent->GetEo() : NULL))
{
   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));
}
void Simple::DidRealiseElement(Local<Value> obj)
 {
                      (void) obj; 
                      }

Simple::Simple(){}

Simple::~Simple(){} //need to add destruction of cb variables

Handle<Value> Simple::a_get() const
{
   HandleScope scope;
   int a;
   eo_do(eobj, simple_a_get(&a));
   return scope.Close(Number::New(a));//need to put proper values
}

void Simple::a_set(Handle<Value> val)
{
  int a;
  a = val->ToInt32()->Value();
   eo_do(eobj, simple_a_set(a));
}

Handle<Value> Simple::b_get() const
{
   HandleScope scope;
   int b;
   eo_do(eobj, simple_b_get(&b));
   return scope.Close(Number::New(b));//need to put proper values
}

void Simple::b_set(Handle<Value> val)
{
  int b;
  b = val->ToInt32()->Value();
   eo_do(eobj, simple_b_set(b));
}

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(SIMPLE_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(SIMPLE_CLASS, eo_event_global_thaw());
 return Undefined();
}
GENERATE_TEMPLATE(Simple,
PROPERTY(elements),
   PROPERTY(a),
   PROPERTY(b),
   PROPERTY(ab_sum),
   PROPERTY(eo_ev_callback_add),
   PROPERTY(eo_ev_callback_del),
   PROPERTY(eo_ev_del),
   METHOD(event_thaw),
   METHOD(event_freeze),
   METHOD(event_freeze_get));
void Simple::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("Simple") , GetTemplate()->GetFunction());
EO_REGISTER_STATIC_METHOD(event_global_thaw);
EO_REGISTER_STATIC_METHOD(event_global_freeze);
}
} //end namespace elm
