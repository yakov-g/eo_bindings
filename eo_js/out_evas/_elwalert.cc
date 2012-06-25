/**
 * generated from "/home/yakov/xml/evas/elwalert.xml"
 */
#include "_elwalert.h"
namespace elm {

using namespace v8;




EO_GENERATE_METHOD_CALLBACKS(ElwAlert, alert);


ElwAlert::ElwAlert(){}

ElwAlert::~ElwAlert(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(ELW_ALERT_INTERFACE, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(ELW_ALERT_INTERFACE, eo_event_global_thaw());
 return Undefined();
}
Handle<Value> ElwAlert::alert(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _text = args[0];
   char* text;
  text = strdup(*String::Utf8Value(_text->ToString()));
   eo_do(eobj, elw_alert_alert(text));
   return Undefined();
}


} //end namespace elm
