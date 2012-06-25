/**
 * generated from "/home/yakov/xml/mixin/mixin.xml"
 */
#include "_mixin.h"
namespace elm {

using namespace v8;



EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(Mixin, ab_sum);
EO_GENERATE_PROPERTY_GET_CALLBACK(Mixin, ab_sum);



Mixin::Mixin(){}

Mixin::~Mixin(){} //need to add destruction of cb variables

Handle<Value> Mixin::ab_sum_get() const
{
   HandleScope scope;
   int sum;
   eo_do(eobj, mixin_ab_sum_get(&sum));
   return scope.Close(Number::New(sum));//need to put proper values
}

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(MIXIN_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(MIXIN_CLASS, eo_event_global_thaw());
 return Undefined();
}

} //end namespace elm
