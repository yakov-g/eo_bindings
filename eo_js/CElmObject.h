#ifndef _CELM_OBJECT_H
#define _CELM_OBJECT_H

#include "elm.h"
#include "Eo.h"

namespace elm {

using namespace v8;


class CElmObject{
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
//   Evas_Object *eo;
   Persistent<Object> jsObject;
   Eo *eobj;
/*
   struct {
      Persistent<Value> animate;
      Persistent<Value> click;
      Persistent<Value> key_down;
   } cb;

   struct {
      bool isResize;
   } cached;
*/
   Ecore_Animator *current_animator;

   CElmObject();
   CElmObject(Local<Object> _jsObject, Eo *_eobj);
   virtual ~CElmObject();

   void ApplyProperties(Handle<Object> obj);

   template <class T>
   static Handle<Value> New(const Arguments& args)
     {
        HandleScope scope;

        if (!args.IsConstructCall())
          {
             args[0]->ToObject()->SetHiddenValue(String::New("type"), T::GetTemplate()->GetFunction());
             return args[0];
          }

        CElmObject *parent = (args[1] == Undefined()) ? NULL :
           static_cast<CElmObject *>(args[1]->ToObject()->GetPointerFromInternalField(0));

        T *obj = new T(args.This(), parent);
        obj->jsObject.MakeWeak(obj, T::Delete);
/*
        Local<Array> properties = obj->jsObject->GetPropertyNames();
        for (unsigned int i = 0; i < properties->Length(); i++)
        {
           Local<String> key = properties->Get(i)->ToString();
           String::Utf8Value key_utf(key);
           printf(" obj_prop: %s\n", *key_utf);
        }
        */
        return Undefined();
     }

   static void Delete(Persistent<Value>, void *parameter);

public:
   static void Initialize(Handle<Object> target);


   Eo *GetEo() const { return eobj; }
   Handle<Object> GetJSObject() const { return jsObject; }
   virtual void DidRealiseElement(Local<Value>) {}

   static Handle<Value> Realise(const Arguments& args);
   static Local<Object> Realise(Handle<Value> desc, Handle<Value> parent);
};

Handle<Value> Callback_elements_get(Local<String>, const AccessorInfo &info);
void Callback_elements_set(Local<String>, Local<Value> value, const AccessorInfo &info);


}

#endif
