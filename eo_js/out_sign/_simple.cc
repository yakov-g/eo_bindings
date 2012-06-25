/**
 * generated from "/home/yakov/xml/signals/simple.xml"
 */
#include "_simple.h"
namespace elm {

using namespace v8;

EO_GENERATE_PROPERTY_CALLBACKS(Simple, a);

EO_GENERATE_PROPERTY_SET_CALLBACK(Simple, b);
EO_GENERATE_PROPERTY_GET_EMPTY_CALLBACK(Simple, b);

EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(Simple, c);
EO_GENERATE_PROPERTY_GET_CALLBACK(Simple, c);


EO_GENERATE_PROPERTY_CALLBACKS(Simple, ev_a_changed);

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

void Simple::b_set(Handle<Value> val)
{
  int b;
  b = val->ToInt32()->Value();
   eo_do(eobj, simple_b_set(b));
}

Handle<Value> Simple::c_get() const
{
   HandleScope scope;
   int c;
   eo_do(eobj, simple_c_get(&c));
   return scope.Close(Number::New(c));//need to put proper values
}

void Simple::ev_a_changed(void *event_info) //parse of event_info need to be added 
{
  Handle<Function> callback(Function::Cast(*cb._event_ev_a_changed));
  Handle<Value> args[1] = {jsObject};
  callback->Call(jsObject, 1, args);
}

Eina_Bool Simple::ev_a_changed_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)
{
                           HandleScope scope;
                           static_cast<Simple*>(data)->ev_a_changed(event_info);
                           return EINA_TRUE;
                           (void) obj;
                           (void) desc;
                       }

Handle<Value> Simple::ev_a_changed_get() const
{
                           return cb._event_ev_a_changed;
                       }

void Simple::ev_a_changed_set(Handle<Value> val)
{
  if (!val->IsFunction())
                           return;
  if (!cb._event_ev_a_changed.IsEmpty())
                         {
                            cb._event_ev_a_changed.Dispose();
                            cb._event_ev_a_changed.Clear();
                            eo_do(eobj, eo_event_callback_del(EV_A_CHANGED, ev_a_changed_wrapper, this));
                         }
  cb._event_ev_a_changed = Persistent<Value>::New(val);
                         eo_do(eobj, eo_event_callback_add(EV_A_CHANGED, ev_a_changed_wrapper, this));
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
   PROPERTY(c),
   PROPERTY(ev_a_changed),
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
