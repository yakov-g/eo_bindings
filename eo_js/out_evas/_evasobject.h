/**
 * generated from "/home/yakov/xml/evas/evasobject.xml"
 */
#ifndef _JS_EVASOBJECT_H_
#define _JS_EVASOBJECT_H_

#include "elm.h" //macro defines, common functions
#include "CElmObject.h" //base object
#include "evas_obj.h" //eo-class include file
#include "_eobase.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class EvasObject : public virtual CElmObject, public virtual EoBase {
private:
protected:
   EvasObject();
   virtual ~EvasObject();

public:
   Handle<Value> color_get() const;
   void color_set(Handle<Value> val);
   Handle<Value> position_get() const;
   void position_set(Handle<Value> val);
   Handle<Value> visibility_get() const;
   void visibility_set(Handle<Value> val);
   Handle<Value> size_get() const;
   void size_set(Handle<Value> val);




   Handle<Value> longlongs(const Arguments&);
   Handle<Value> longs(const Arguments&);
   Handle<Value> par_by_ref(const Arguments&);
   Handle<Value> child_add(const Arguments&);
   Handle<Value> ints(const Arguments&);
   Handle<Value> no_par(const Arguments&);
   Handle<Value> floats(const Arguments&);

}; //end class

/* properties callbacks */
   Handle<Value> Callback_color_get(Local<String>, const AccessorInfo &info);
   void Callback_color_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_position_get(Local<String>, const AccessorInfo &info);
   void Callback_position_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_visibility_get(Local<String>, const AccessorInfo &info);
   void Callback_visibility_set(Local<String>, Local<Value> val, const AccessorInfo &info);
   Handle<Value> Callback_size_get(Local<String>, const AccessorInfo &info);
   void Callback_size_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* properties(events) callbacks */

/* methods callbacks */
   Handle<Value> Callback_longlongs(const Arguments&);
   Handle<Value> Callback_longs(const Arguments&);
   Handle<Value> Callback_par_by_ref(const Arguments&);
   Handle<Value> Callback_child_add(const Arguments&);
   Handle<Value> Callback_ints(const Arguments&);
   Handle<Value> Callback_no_par(const Arguments&);
   Handle<Value> Callback_floats(const Arguments&);

} //end namespace elm

#endif
