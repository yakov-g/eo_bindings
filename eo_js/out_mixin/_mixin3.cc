/**
 * generated from "/home/yakov/xml/mixin/mixin3.xml"
 */
#include "_mixin3.h"
namespace elm {

using namespace v8;






Mixin3::Mixin3(){}

Mixin3::~Mixin3(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(MIXIN3_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(MIXIN3_CLASS, eo_event_global_thaw());
 return Undefined();
}

} //end namespace elm
