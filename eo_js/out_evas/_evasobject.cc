/**
 * generated from "/home/yakov/xml/evas/evasobject.xml"
 */
#include "_evasobject.h"
namespace elm {

using namespace v8;

EO_GENERATE_PROPERTY_CALLBACKS(EvasObject, color);
EO_GENERATE_PROPERTY_CALLBACKS(EvasObject, position);
EO_GENERATE_PROPERTY_CALLBACKS(EvasObject, visibility);
EO_GENERATE_PROPERTY_CALLBACKS(EvasObject, size);



EO_GENERATE_METHOD_CALLBACKS(EvasObject, longlongs);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, longs);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, par_by_ref);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, child_add);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, ints);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, no_par);
EO_GENERATE_METHOD_CALLBACKS(EvasObject, floats);


EvasObject::EvasObject(){}

EvasObject::~EvasObject(){} //need to add destruction of cb variables

Handle<Value> EvasObject::color_get() const
{
   HandleScope scope;
   int r;
   int g;
   int b;
   int a;
   eo_do(eobj, exevas_obj_color_get(&r, &g, &b, &a));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("r"), Number::New(r));
   obj__->Set(String::NewSymbol("g"), Number::New(g));
   obj__->Set(String::NewSymbol("b"), Number::New(b));
   obj__->Set(String::NewSymbol("a"), Number::New(a));
   return scope.Close(obj__);//need to put proper values
}

void EvasObject::color_set(Handle<Value> val)
{
   Local<Object> __o = val->ToObject();
   int r;
   r = __o->Get(String::NewSymbol("r"))->ToInt32()->Value();
   int g;
   g = __o->Get(String::NewSymbol("g"))->ToInt32()->Value();
   int b;
   b = __o->Get(String::NewSymbol("b"))->ToInt32()->Value();
   int a;
   a = __o->Get(String::NewSymbol("a"))->ToInt32()->Value();
   eo_do(eobj, exevas_obj_color_set(r, g, b, a));
}

Handle<Value> EvasObject::position_get() const
{
   HandleScope scope;
   int x;
   int y;
   eo_do(eobj, exevas_obj_position_get(&x, &y));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("x"), Number::New(x));
   obj__->Set(String::NewSymbol("y"), Number::New(y));
   return scope.Close(obj__);//need to put proper values
}

void EvasObject::position_set(Handle<Value> val)
{
   Local<Object> __o = val->ToObject();
   int x;
   x = __o->Get(String::NewSymbol("x"))->ToInt32()->Value();
   int y;
   y = __o->Get(String::NewSymbol("y"))->ToInt32()->Value();
   eo_do(eobj, exevas_obj_position_set(x, y));
}

Handle<Value> EvasObject::visibility_get() const
{
   HandleScope scope;
   unsigned char v;
   eo_do(eobj, exevas_obj_visibility_get(&v));
   return scope.Close(Boolean::New(v));//need to put proper values
}

void EvasObject::visibility_set(Handle<Value> val)
{
   unsigned char v;
   v = val->ToBoolean()->Value();
   eo_do(eobj, exevas_obj_visibility_set(v));
}

Handle<Value> EvasObject::size_get() const
{
   HandleScope scope;
   int w;
   int h;
   eo_do(eobj, evas_obj_size_get(&w, &h));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("w"), Number::New(w));
   obj__->Set(String::NewSymbol("h"), Number::New(h));
   return scope.Close(obj__);//need to put proper values
}

void EvasObject::size_set(Handle<Value> val)
{
   Local<Object> __o = val->ToObject();
   int w;
   w = __o->Get(String::NewSymbol("w"))->ToInt32()->Value();
   int h;
   h = __o->Get(String::NewSymbol("h"))->ToInt32()->Value();
   eo_do(eobj, exevas_obj_size_set(w, h));
}

static Handle<Value> event_global_freeze(const Arguments& args)
{
  eo_class_do(EXEVAS_OBJ_CLASS, eo_event_global_freeze());
 return Undefined();
}
static Handle<Value> event_global_thaw(const Arguments& args)
{
  eo_class_do(EXEVAS_OBJ_CLASS, eo_event_global_thaw());
 return Undefined();
}
Handle<Value> EvasObject::longlongs(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _x = args[0];
   unsigned long long x;
   x = _x->ToNumber()->Value();
   Local<Value> _y = args[1];
   long long y;
   y = _y->ToNumber()->Value();
   unsigned long long xx;
   long long yy;
   eo_do(eobj, exevas_obj_longlongs(x, y, &xx, &yy));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("xx"), Number::New(xx));
   obj__->Set(String::NewSymbol("yy"), Number::New(yy));
   return scope.Close(obj__);//need to put proper values
}

Handle<Value> EvasObject::longs(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _x = args[0];
   unsigned long x;
   x = _x->ToUint32()->Value();
   Local<Value> _y = args[1];
   long y;
   y = _y->ToNumber()->Value();
   unsigned long xx;
   long yy;
   eo_do(eobj, exevas_obj_longs(x, y, &xx, &yy));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("xx"), Number::New(xx));
   obj__->Set(String::NewSymbol("yy"), Number::New(yy));
   return scope.Close(obj__);//need to put proper values
}

Handle<Value> EvasObject::par_by_ref(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _x = args[0];
   int x;
   x = _x->ToInt32()->Value();
   Local<Value> _y = args[1];
   int y;
   y = _y->ToInt32()->Value();
   Local<Value> _z = args[2];
   long long z;
   z = _z->ToNumber()->Value();
   eo_do(eobj, exevas_obj_par_by_ref(&x, y, z));
   return Undefined();
}

Handle<Value> EvasObject::child_add(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _child = args[0];
   Eo* child;
   child = static_cast<CElmObject*>(_child->ToObject()->GetPointerFromInternalField(0))->GetEo();
   eo_do(eobj, exevas_obj_child_add(child));
   return Undefined();
}

Handle<Value> EvasObject::ints(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _x = args[0];
   unsigned int x;
   x = _x->ToUint32()->Value();
   Local<Value> _y = args[1];
   int y;
   y = _y->ToInt32()->Value();
   unsigned int xx;
   Local<Value> _yy = args[2];
   int yy;
   yy = _yy->ToInt32()->Value();
   eo_do(eobj, exevas_obj_ints(x, y, &xx, &yy));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("xx"), Number::New(xx));
   obj__->Set(String::NewSymbol("yy"), Number::New(yy));
   return scope.Close(obj__);//need to put proper values
}

Handle<Value> EvasObject::no_par(const Arguments& args)
{
   HandleScope scope;
   eo_do(eobj, exevas_obj_no_par());
   return Undefined();
}

Handle<Value> EvasObject::floats(const Arguments& args)
{
   HandleScope scope;
   Local<Value> _b = args[0];
   double b;
   b = _b->ToNumber()->Value();
   Local<Value> _c = args[1];
   long double c;
   c = _c->ToNumber()->Value();
   double bb;
   long double cc;
   eo_do(eobj, exevas_obj_floats(b, c, &bb, &cc));
   Local<Object> obj__ = Object::New();
   obj__->Set(String::NewSymbol("bb"), Number::New(bb));
   obj__->Set(String::NewSymbol("cc"), Number::New(cc));
   return scope.Close(obj__);//need to put proper values
}


} //end namespace elm
