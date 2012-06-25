/**
 * generated from "/home/yakov/xml/mixin/mixin2.xml"
 */
#include "_mixin2.h"
namespace elm {

using namespace v8;






Mixin2::Mixin2(){}

Mixin2::~Mixin2(){} //need to add destruction of cb variables

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(MIXIN2_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(MIXIN2_CLASS, eo_event_global_thaw());
 return Undefined();
}

} //end namespace elm
