#include "elm.h"
#include "CElmObject.h"

namespace elm {

using namespace v8;

//Persistent<FunctionTemplate> CElmObject::tmpl;

Handle<Value> Callback_elements_get(Local<String>, const AccessorInfo &info)
{
   HandleScope scope;
   return info.This()->GetHiddenValue(String::NewSymbol("elements"));
}

void Callback_elements_set(Local<String>, Local<Value> value, const AccessorInfo &info)
{
   HandleScope scope;

   Local<Object> obj = value->ToObject();
   Local<Array> props = obj->GetOwnPropertyNames();
   Handle<Object> elements = Object::New();

   for (unsigned int i = 0; i < props->Length(); i++)
     {
        Local<String> key = props->Get(i)->ToString();
        Local<Object> val = obj->Get(key)->ToObject();
        Local<Value> type = val->GetHiddenValue(String::NewSymbol("type"));
        Local<Object> realisedObject;

        if (!type.IsEmpty())
          realisedObject = CElmObject::Realise(val, info.This());
        else
          {
             Local<String> elementstr = String::NewSymbol("element");
             if (!val->Has(elementstr))
               {
                  ELM_ERR("Need an object with 'element' property");
                  continue;
               }

             realisedObject = val->Clone();
             realisedObject->Set(elementstr,
                                 CElmObject::Realise(val->Get(elementstr), info.This()));
          }

        elements->Set(key, realisedObject);
        GetObjectFromAccessorInfo<CElmObject>(info)->DidRealiseElement(realisedObject);
     }
   info.This()->SetHiddenValue(String::NewSymbol("elements"), elements);
}


void CElmObject::Delete(Persistent<Value>, void *parameter)
{
   delete static_cast<CElmObject *>(parameter);
}

CElmObject::CElmObject()
{

}
/*
CElmObject::CElmObject(Local<Object> _jsObject, Evas_Object *_eo)
   : eo(_eo)
   , current_animator(NULL)
{
   jsObject = Persistent<Object>::New(_jsObject);
   jsObject->SetPointerInInternalField(0, this);
   jsObject->SetHiddenValue(String::NewSymbol("elements"), Undefined());
}
*/

CElmObject::CElmObject(Local<Object> _jsObject, Eo *_eobj)
   : eobj(_eobj)
{
   jsObject = Persistent<Object>::New(_jsObject);
   jsObject->SetPointerInInternalField(0, this);
   jsObject->SetHiddenValue(String::NewSymbol("elements"), Undefined());
   if (eobj)
     eo_do(eobj, eo_base_data_set("js-obj", this, NULL));
}

CElmObject::~CElmObject()
{
   jsObject.Dispose();
   jsObject.Clear();
}

void CElmObject::ApplyProperties(Handle<Object> obj)
{
   HandleScope scope;

   Local<Array> props = obj->GetOwnPropertyNames();
   for (unsigned int i = 0; i < props->Length(); i++)
     {
        Local<String> key = props->Get(i)->ToString();
        jsObject->Set(key, obj->Get(key));
     }
}

void CElmObject::Initialize(Handle<Object> target)
{
   target->Set(String::NewSymbol("realise"),
               FunctionTemplate::New(Realise)->GetFunction());
}

/*
Handle<FunctionTemplate> CElmObject::GetTemplate()
{
   if (!tmpl.IsEmpty())
     return tmpl;

   HandleScope scope;
   tmpl = Persistent<FunctionTemplate>::New(FunctionTemplate::New());
   tmpl->InstanceTemplate()->SetInternalFieldCount(1);

   RegisterProperties(tmpl->PrototypeTemplate(),
                      PROPERTY(x),
                      PROPERTY(y),
                      PROPERTY(width),
                      PROPERTY(height),
                      PROPERTY(align),
                      PROPERTY(weight),
                      PROPERTY(pos),
                      PROPERTY(text),
                      PROPERTY(scale),
                      PROPERTY(style),
                      PROPERTY(visible),
                      PROPERTY(enabled),
                      PROPERTY(hint_min),
                      PROPERTY(hint_max),
                      PROPERTY(hint_req),
                      PROPERTY(focus),
                      PROPERTY(layer),
                      PROPERTY(label),
                      PROPERTY(padding),
                      PROPERTY(pointer_mode),
                      PROPERTY(antialias),
                      PROPERTY(static_clip),
                      PROPERTY(size_hint_aspect),
                      PROPERTY(name),
                      PROPERTY(resize),
                      PROPERTY(pointer),
                      PROPERTY(on_animate),
                      PROPERTY(on_click),
                      PROPERTY(on_key_down),
                      PROPERTY(elements),
                      NULL);

   return tmpl;
}

*/

Local<Object> CElmObject::Realise(Handle<Value> descValue, Handle<Value> parent)
{
   HandleScope scope;
   Local<Object> desc = descValue->ToObject();

   if (!desc->GetHiddenValue(String::NewSymbol("elm::realised")).IsEmpty())
      return scope.Close(desc);

   Local<Array> props = desc->GetOwnPropertyNames();
   Local<Value> func = desc->GetHiddenValue(String::NewSymbol("type"));

   Handle<Value> params[] = { descValue, parent };
   Local<Object> obj = Local<Function>::Cast(func)->NewInstance(2, params);


   Local<Array> properties = obj -> GetPropertyNames();

   for (unsigned int i = 0; i < props->Length(); i++)
     {
        Local<String> key = props->Get(i)->ToString();
        String::Utf8Value key_utf(key);
        Local<Value> val = desc->Get(key);
        obj->Set(key, val);
     }
/*
   Local<Value> visible = desc->Get(String::NewSymbol("visible"));
   if (visible->IsUndefined())
     obj->Set(String::New("visible"), Boolean::New(true));
*/

   Local<Value> visible = desc->Get(String::NewSymbol("visibility"));
   if (visible->IsUndefined())
     obj->Set(String::New("visibility"), Boolean::New(true));

   obj->SetHiddenValue(String::NewSymbol("elm::realised"), Boolean::New(true));
   return scope.Close(obj);
}

Handle<Value> CElmObject::Realise(const Arguments& args)
{
   if (args.Length() != 1)
     {
        ELM_ERR("Realise needs object description");
        return Undefined();
     }

   return Realise(args[0], Undefined());
}


}
