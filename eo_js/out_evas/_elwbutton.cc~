/**
 * generated from "/home/yakov/xml/evas/elwbutton.xml"
 */
#include "_elwbutton.h"
namespace elm {

using namespace v8;

EO_GENERATE_PROPERTY_CALLBACKS(ElwButton, text);




EO_GENERATE_PROPERTY_CALLBACKS(ElwButton, ev_clicked);

ElwButton::ElwButton(Local<Object> _jsObject, CElmObject *parent)
 : CElmObject(_jsObject, eo_add(ELW_BUTTON_CLASS , parent ? parent->GetEo() : NULL))
{
   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));
}
void ElwButton::DidRealiseElement(Local<Value> obj)
 {
                      (void) obj; 
                      }

ElwButton::ElwButton(){}

ElwButton::~ElwButton(){} //need to add destruction of cb variables

Handle<Value> ElwButton::text_get() const
{
   HandleScope scope;
   char* text;
   eo_do(eobj, elw_button_text_get(&text));
   return scope.Close(String::New(text));//need to put proper values
}

void ElwButton::text_set(Handle<Value> val)
{
  char* text;
  text = strdup(*String::Utf8Value(val->ToString()));
   eo_do(eobj, elw_button_text_set(text));
  free(text);}

void ElwButton::ev_clicked(void *event_info) //parse of event_info need to be added 
{
  Handle<Function> callback(Function::Cast(*cb._event_ev_clicked));
  Handle<Value> args[1] = {jsObject};
  callback->Call(jsObject, 1, args);
}

Eina_Bool ElwButton::ev_clicked_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)
{
                           HandleScope scope;
                           static_cast<ElwButton*>(data)->ev_clicked(event_info);
                           return EINA_TRUE;
                           (void) obj;
                           (void) desc;
                       }

Handle<Value> ElwButton::ev_clicked_get() const
{
                           return cb._event_ev_clicked;
                       }

void ElwButton::ev_clicked_set(Handle<Value> val)
{
  if (!val->IsFunction())
                           return;
  if (!cb._event_ev_clicked.IsEmpty())
                         {
                            cb._event_ev_clicked.Dispose();
                            cb._event_ev_clicked.Clear();
                            eo_do(eobj, eo_event_callback_del(EV_CLICKED, ev_clicked_wrapper, this));
                         }
  cb._event_ev_clicked = Persistent<Value>::New(val);
                         eo_do(eobj, eo_event_callback_add(EV_CLICKED, ev_clicked_wrapper, this));
}

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(ELW_BUTTON_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(ELW_BUTTON_CLASS, eo_event_global_thaw());
 return Undefined();
}
GENERATE_TEMPLATE(ElwButton,
PROPERTY(elements),
   PROPERTY(text),
   PROPERTY(color),
   PROPERTY(position),
   PROPERTY(visibility),
   PROPERTY(size),
   PROPERTY(ev_clicked),
   PROPERTY(eo_ev_callback_add),
   PROPERTY(eo_ev_callback_del),
   PROPERTY(eo_ev_del),
   METHOD(alert),
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
void ElwButton::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("ElwButton") , GetTemplate()->GetFunction());
EO_REGISTER_STATIC_METHOD(event_global_thaw);
EO_REGISTER_STATIC_METHOD(event_global_freeze);
}
} //end namespace elm
