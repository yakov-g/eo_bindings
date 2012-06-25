/**
 * generated from "/home/yakov/xml/mixin/mixin.xml"
 */
#ifndef _JS_MIXIN_H_
#define _JS_MIXIN_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "mixin.h" //eo-class include file

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class Mixin : public virtual CElmObject {
private:
protected:
   Mixin();
   virtual ~Mixin();

public:


   Handle<Value> ab_sum_get() const;



}; //end class

/* properties callbacks */
   Handle<Value> Callback_ab_sum_get(Local<String>, const AccessorInfo &info);
   void Callback_ab_sum_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* properties(events) callbacks */

/* methods callbacks */

} //end namespace elm

#endif
