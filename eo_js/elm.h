#ifndef _ELM_H
#define _ELM_H

#define ELM_DBG(...) EINA_LOG_DOM_DBG(log_domain, __VA_ARGS__)
#define ELM_INF(...) EINA_LOG_DOM_INFO(log_domain, __VA_ARGS__)
#define ELM_WRN(...) EINA_LOG_DOM_WARN(log_domain, __VA_ARGS__)
#define ELM_ERR(...) EINA_LOG_DOM_ERR(log_domain, __VA_ARGS__)
#define ELM_CRT(...) EINA_LOG_DOM_CRITICAL(log_domain, __VA_ARGS__)

#include <Elementary.h>
#include <v8.h>
#include <stdarg.h>

#include "CElmObject.h"

namespace elm {

using namespace v8;

template<class T> inline T *GetObjectFromAccessorInfo(const AccessorInfo &info)
{
    return dynamic_cast<T*>(static_cast<CElmObject*>(info.This()->GetPointerFromInternalField(0)));
}

template<class T> inline T *GetObjectFromArguments(const Arguments &args)
{
     return dynamic_cast<T *>(static_cast<CElmObject*>(args.This()->GetPointerFromInternalField(0)));
}

inline void RegisterProperties(Handle<ObjectTemplate> prototype, ...)
{
   va_list arg;

   va_start(arg, prototype);
   for (const char *name = va_arg(arg, const char *); name; name = va_arg(arg, const char *))
     {
        AccessorGetter get_callback = va_arg(arg, AccessorGetter);
        AccessorSetter set_callback = va_arg(arg, AccessorSetter);
        InvocationCallback inv_callback = va_arg(arg, InvocationCallback);

        if (inv_callback)
          {
            prototype->Set(String::NewSymbol(name), FunctionTemplate::New(inv_callback));
          }
        else
        {
          prototype->SetAccessor(String::NewSymbol(name), get_callback, set_callback);
         }
     }
   va_end(arg);

}

inline Evas_Object *GetEvasObjectFromJavascript(Handle<Value> obj)
{
//   return static_cast<CElmObject*>(obj->ToObject()->GetPointerFromInternalField(0))->GetEvasObject();
   (void) obj;
   return NULL;

}

extern int log_domain;

}

#define PROPERTY(name_) \
   #name_, Callback_## name_ ##_get, Callback_## name_ ##_set, NULL

#define PROPERTY_RO(name_) \
   #name_, Callback_## name_ ##_get, NULL, NULL

#define PROPERTY_SO(name_) \
   #name_, NULL, Callback_## name_ ##_set, NULL

#define METHOD(name_) \
   #name_, NULL, NULL, Callback_## name_

#define EO_GENERATE_PROPERTY_CALLBACKS(class_,name_) \
   Handle<Value> Callback_## name_ ##_get(Local<String>, const AccessorInfo &info) { \
      HandleScope scope; \
      return scope.Close(GetObjectFromAccessorInfo<class_>(info)->__## name_ ##_get()); \
   } \
   void Callback_## name_ ##_set(Local<String>, Local<Value> value, const AccessorInfo &info) { \
      HandleScope scope; \
      GetObjectFromAccessorInfo<class_>(info)->__## name_ ##_set(value); \
   }


#define EO_GENERATE_PROPERTY_GET_CALLBACK(class_,name_) \
   Handle<Value> Callback_## name_ ##_get(Local<String>, const AccessorInfo &info) { \
      HandleScope scope; \
      return scope.Close(GetObjectFromAccessorInfo<class_>(info)->__## name_ ##_get()); \
   }

#define EO_GENERATE_PROPERTY_SET_CALLBACK(class_,name_) \
   void Callback_## name_ ##_set(Local<String>, Local<Value> value, const AccessorInfo &info) { \
      HandleScope scope; \
      GetObjectFromAccessorInfo<class_>(info)->__## name_ ##_set(value); \
   }

#define EO_GENERATE_PROPERTY_GET_EMPTY_CALLBACK(class_,name_) \
   Handle<Value> Callback_## name_ ##_get(Local<String>, const AccessorInfo &info) { \
        return Undefined();\
      }

#define EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(class_,name_) \
   void Callback_## name_ ##_set(Local<String>, Local<Value> value, const AccessorInfo &info) { \
   }

#define GENERATE_PROPERTY_CALLBACKS(class_,name_) \
   static Handle<Value> Callback_## name_ ##_get(Local<String>, const AccessorInfo &info) { \
      HandleScope scope; \
      return scope.Close(GetObjectFromAccessorInfo<class_>(info)->name_ ##_get()); \
   } \
   static void Callback_## name_ ##_set(Local<String>, Local<Value> value, const AccessorInfo &info) { \
      HandleScope scope; \
      GetObjectFromAccessorInfo<class_>(info)->name_ ##_set(value); \
   }

#define GENERATE_METHOD_CALLBACKS(class_,name_) \
   static Handle<Value> Callback_## name_(const Arguments& args) { \
      HandleScope scope; \
      return scope.Close(GetObjectFromArguments<class_>(args)->name_(args));\
   }


#define EO_GENERATE_METHOD_CALLBACKS(class_,name_) \
      Handle<Value> Callback_## name_(const Arguments& args) { \
      HandleScope scope; \
      return scope.Close(GetObjectFromArguments<class_>(args)->__## name_(args)); \
   }

#define EO_GENERATE_STATIC_METHOD(class_, name_) \
      static Handle<Value> static_## name_(const Arguments& args) { \
      return Undefined(); \
   }

#define EO_REGISTER_STATIC_METHOD(_name) \
      GetTemplate()->GetFunction()->ToObject()->Set(String::NewSymbol(#_name),   FunctionTemplate::New(_name)->GetFunction())

#define GENERATE_TEMPLATE_FULL(super_class_,this_class_,...) \
   Handle<FunctionTemplate> this_class_::GetTemplate() \
   { \
      if (!tmpl.IsEmpty()) return tmpl; \
      \
      HandleScope scope; \
  /*    Handle<FunctionTemplate> parentTmpl = super_class_::GetTemplate(); */\
      tmpl = Persistent<FunctionTemplate>::New(FunctionTemplate::New(New<this_class_>)); \
/*      tmpl->Inherit(parentTmpl); */ \
      tmpl->InstanceTemplate()->SetInternalFieldCount(1); \
      RegisterProperties(tmpl->PrototypeTemplate(), ##__VA_ARGS__, NULL); \
      return scope.Close(tmpl); \
   } \
   Persistent<FunctionTemplate> this_class_::tmpl

#define GENERATE_TEMPLATE(this_class_,...) \
   GENERATE_TEMPLATE_FULL(CElmObject, this_class_, ##__VA_ARGS__)



#define EO_GENERATE_TEMPLATE_FULL(this_class_,...) \
   Handle<FunctionTemplate> this_class_::GetTemplate() \
   { \
      if (!tmpl.IsEmpty()) return tmpl; \
      \
      HandleScope scope; \
      tmpl = Persistent<FunctionTemplate>::New(FunctionTemplate::New(New<this_class_>)); \
      tmpl->InstanceTemplate()->SetInternalFieldCount(1); \
      RegisterProperties(tmpl->PrototypeTemplate(), ##__VA_ARGS__, NULL); \
      return scope.Close(tmpl); \
   } \
   Persistent<FunctionTemplate> this_class_::tmpl



#endif
