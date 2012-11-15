import xml.parsers.expat, os, shutil
from eoparser.helper import isXML, abs_path_get, dir_files_get
from helper import normalize_names, _const
import copy

const = _const()


def O_TYPE_CHECK(o, class_type):
  if not isinstance(o, class_type):
  #  if type(o) is not class_type:
     print "Warning: object: %s is not of class: %s"%(o, class_type.__name__)
     return False
  else:
     return True

def class_name_get(_o):
  return _o.__class__.__name__


#Wrapping class to pass Visitor object and call for visit function
class VAcceptor(object):
  def accept(self, v):
    if not O_TYPE_CHECK(v, Visitor):
      return None
    v.visit(self)

#Class to save data about each function
#This is one item from Mod.functions list
class Func(VAcceptor):
   def __init__(self, _name, _prop_name,_op_id, _c_macro, _parameters, _prop_type, _cl_obj):
     self.name = _name
     self.prop_name = _prop_name
     self.op_id = _op_id
     self.c_macro = _c_macro
     self.parameters = _parameters
     self.cl_obj = _cl_obj
     self.prop_type = _prop_type


#class to save init function data, and headers data: such as include, etc
class Init(VAcceptor):
   def __init__(self, _cl_obj):
     self.cl_obj = _cl_obj
     self.op_id = "INIT"

#class to save event data
#This is one item from Mod.ev_ids list
class Ev(VAcceptor):
   def __init__(self, _ev_id, _cl_obj):
     self.ev_id = _ev_id
     self.op_id = _ev_id
     self.cl_obj = _cl_obj

#  class to keep all data about class
#
class Mod(object):
   def __init__(self):
     self.kl_id = ""
     self.c_name = ""
     self.macro = ""
     self.eo_type = ""
     self.get_function = ""
     self.instantiateable = False
     self.includes = None
     self.mod_name = ""
     self.basemodule = ""
     self.op_ids = []
     self.ev_ids = []
     self.extern_base_id = ""
     self.extern_functions = []
     self.sub_id_function = ""
     self.source_file = ""
     self.parents = []
     self.V = None

     # dictionary to save all object which have to be visited: Func, Ev, Init
     self.visitees = {}

   def resolve(self):
     for n, o in self.visitees.items():
       o.accept(self.V)




#  Visitor Design Pattern
#  Visitor - base class for different visitors.
#  visit function implements dispatching depending on class name of object

class Visitor(object):
  def visit(self, _p):
    method_name = "visit_" + class_name_get(_p)
    method = getattr(self, method_name, False)
    if callable(method):
      method(_p)
    else:
       print "%s is not callable attribute"%(method_name)


  def cast(self, _in):
    t = _in

    for k in self.primary_types:
      if t.find(k) != -1:
        t = t.replace(k, self.primary_types[k])
    return t



  primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

  internal_types = {
                                "void*": ["void*", "object"],
                                "char*": ["char*", "object", "ToString"],
                                "Eo*":  ["Eo*", "EoDefault", "ToObject"],
                                "short" : ["int", "int", "ToInt32"],
                                "short*" : ["int", "int", "ToInt32"],
                                "int": ["int", "int", "ToInt32"],
                                "int*": ["int", "int", "ToInt32"],
                                "long": ["long", "long", "ToNumber"],
                                "long*": ["long", "long", "ToNumber"],
                                "long long" : ["long long", "long long", "ToNumber"],
                                "long long*" : ["long long", "long long", "ToNumber"],
                                "unsigned char": ["unsigned char", "int", "ToInt32"],
                                "unsigned char*" : ["unsigned char","int", "ToInt32"],
                                "bool" : ["unsigned char","int", "ToBoolean"],
                                "bool*" : ["unsigned char","int", "ToBoolean"],
                                "unsigned int": ["unsigned int", "unsigned int", "ToUint32"],
                                "unsigned int*": ["unsigned int", "unsigned int", "ToUint32"],
                                "unsigned short": ["unsigned int", "unsigned int", "ToUint32"],
                                "unsigned short*": ["unsigned int", "unsigned int", "ToUint32"],
                                "unsigned long": ["unsigned long", "unsigned long", "ToUint32"],
                                "unsigned long*": ["unsigned long", "unsigned long", "ToNumber"],
                                "unsigned long long": ["unsigned long long", "unsigned long long", "ToNumber"],
                                "unsigned long long*": ["unsigned long long", "unsigned long long", "ToNumber"],
                                "float": ["float", "float", "ToNumber"],
                                "double": ["double", "double", "ToNumber" ],
                                "long double": ["long double", "long double", "ToNumber"],
                                "float*": ["float", "float", "ToNumber"],
                                "double*": ["double", "double", "ToNumber" ],
                                "long double*": ["long double", "long double", "ToNumber"],
                                "Eo_Event_Description*":["long","long", "ToNumber"],
                                "Eo_Event_Cb":["Eo_Event_Cb","object", "ToNumber"]
                                }

# Class is used to create it's instance, and dynamically add properties
class Abstract(object):
   def __init__(self):
      pass



class JsVisitor(Visitor):

  def __init__(self):
     self.visited_properties = []

     self.c_file = Abstract()
     self.c_file.name = ""
     self.c_file.tmpl = []
     self.c_file.cb_generate_macros = []
     self.c_file.functions = []
     self.c_file.header = []
     self.c_file.init_f = []
     self.c_file.init_f_addition = []

     self.h_file = Abstract()
     self.h_file.name = ""
     self.h_file.ev_list = []
     self.h_file.header = []
     self.h_file.prop_cb_headers = []
     self.h_file.ev_cb_headers = []
     self.h_file.meth_cb_headers = []

     self.class_info = Abstract()
     self.class_info.header = ""
     self.class_info.private = []
     self.class_info.protected = []
     self.class_info.public = []


     self.js_types = { "ToBoolean" : "Boolean",
                          "ToString" : "String",
                          "ToUint32" : "Number",
                          "ToInt32" : "Number",
                          "ToNumber" : "Number",
                          "ToObject" : "Local <Object>"
                          }

  #Func visit function, to generate code for functions
  def visit_Func(self, _o):

     if _o.prop_type == const.SET_GET:
       _oo = copy.deepcopy(_o)
       self.visit_prop_set_get(_oo)

       prop_name = _oo.name[:-4]
       if prop_name not in self.visited_properties:
         self.visited_properties.append(prop_name)
         self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_SET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))
         self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_GET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))
         self.class_info.public.append("   Handle<Value> %s_get() const;\n"%(prop_name))
         self.class_info.public.append("   void %s_set(Handle<Value> val);\n"%(prop_name))

         self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(prop_name))
         self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(prop_name))
         self.c_file.tmpl.append("   PROPERTY(%s)"% prop_name)


     elif _o.prop_type == const.SET_ONLY:
       self.visit_prop_set_get(_o)
       prop_name = _o.name[:-4]
       self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_SET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))
       self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_GET_EMPTY_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))

       self.class_info.public.append("   Handle<Value> %s_get() const;\n"%(prop_name))
       self.class_info.public.append("   void %s_set(Handle<Value> val);\n"%(prop_name))

       self.c_file.tmpl.append("   PROPERTY(%s)"% prop_name)
       self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(prop_name))
       self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(prop_name))

     elif _o.prop_type == const.GET_ONLY:
       self.visit_prop_set_get(_o)
       prop_name = _o.name[:-4]
       self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_GET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))
       self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, prop_name))

       self.class_info.public.append("   Handle<Value> %s_get() const;\n"%(prop_name))
       self.class_info.public.append("   void %s_set(Handle<Value> val);\n"%(prop_name))

       self.c_file.tmpl.append("   PROPERTY(%s)"% prop_name)
       self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(prop_name))
       self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(prop_name))

     elif _o.prop_type == const.METHOD:
       self.visit_method(_o)

  # Ev visit function, to generate appropriate code for Ev object
  def visit_Ev(self, _o):
    #defining event globals

    ev = _o.ev_id.lower()
    ev_prefix = "_event_" + ev


    self.h_file.ev_list.append("      Persistent<Value> _event_%s;\n"%(ev))
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_CALLBACKS(%s, %s);\n"%(_o.cl_obj.kl_id, ev))
    self.c_file.tmpl.append("   PROPERTY(%s)"% ev)


    self.class_info.public.append("\n")
    self.class_info.public.append("   Handle<Value> %s_get() const;\n"%(ev))
    self.class_info.public.append("   void %s_set(Handle<Value> val);\n"%(ev))
    self.class_info.public.append("   void %s(void *event_info);\n"%(ev))
    self.class_info.public.append("   static Eina_Bool %s_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);\n"%(ev))

    self.h_file.ev_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(ev))
    self.h_file.ev_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(ev))

    #event function
    self.c_file.functions.append("void %s::%s(void *event_info) //parse of event_info need to be added \n"%(_o.cl_obj.kl_id, ev))
    self.c_file.functions.append("{\n")
    self.c_file.functions.append("  Handle<Function> callback(Function::Cast(*cb.%s));\n"%ev_prefix)
    self.c_file.functions.append("  Handle<Value> args[1] = {jsObject};\n")
    self.c_file.functions.append("  callback->Call(jsObject, 1, args);\n")
    self.c_file.functions.append("}\n")
    self.c_file.functions.append("\n")

    #event function wrapper
    self.c_file.functions.append("Eina_Bool %s::%s_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)\n"%(_o.cl_obj.kl_id, ev))
    self.c_file.functions.append("{\n\
                           HandleScope scope;\n\
                           static_cast<%s*>(data)->%s(event_info);\n\
                           return EINA_TRUE;\n\
                           (void) obj;\n\
                           (void) desc;\n\
                       }\n"%(_o.cl_obj.kl_id, ev))
    self.c_file.functions.append("\n")

     #event function get
    self.c_file.functions.append("Handle<Value> %s::%s_get() const\n"%(_o.cl_obj.kl_id, ev))
    self.c_file.functions.append("{\n\
                    return cb.%s;\n\
                }\n"%ev_prefix)
    self.c_file.functions.append("\n")

          #event function set
    self.c_file.functions.append("void %s::%s_set(Handle<Value> val)\n"%(_o.cl_obj.kl_id, ev))
    self.c_file.functions.append("{\n")
    self.c_file.functions.append("  if (!val->IsFunction())\n\
                    return;\n")
    self.c_file.functions.append("  if (!cb.%s.IsEmpty())\n\
                  {\n\
                     cb.%s.Dispose();\n\
                     cb.%s.Clear();\n\
                     eo_do(eobj, eo_event_callback_del(%s, %s_wrapper, this));\n\
                  }\n"%(ev_prefix, ev_prefix, ev_prefix, _o.ev_id, ev))
    self.c_file.functions.append("  cb.%s = Persistent<Value>::New(val);\n\
                  eo_do(eobj, eo_event_callback_add(%s, %s_wrapper, this));\n"%(ev_prefix, _o.ev_id, ev))
    self.c_file.functions.append("}\n")
    self.c_file.functions.append("\n")



  #is called by visit_Func to parse function as a property
  def visit_prop_set_get(self, _o):

    prop_type = _o.name[-4:]
    prop_name = _o.name[:-4]

    direction = "out" if prop_type == "_get" else "in"

    params_tmp = []
    add_this_func = True
    for i, (n, c_t, d, p_t) in enumerate(_o.parameters):
       if d != direction:
         print "Warning wrong direction: property: %s; parameter: %s; direction:      %s"%(prop_name + "_get", n, d)
         print "Property \"%s\" will not be defined"%(prop_name + "_get")
         add_this_func = False
         break

       c_t_tmp = self.cast(p_t)
       js_type = ""
       c_t_internal = ""

       if c_t_tmp in self.internal_types:
         c_t_internal = self.internal_types[c_t_tmp][0]
         js_type = self.internal_types[c_t_tmp][2]
         params_tmp.append((c_t, n, d, c_t_internal, js_type))
       else:
         print "Warning: type: \"%s\" wasn't found in self.internal_types. Funct ion \"%s\" will not be defined"%(c_t_tmp, prop_name + "_get")
         add_this_func = False
         break

       if not add_this_func:
         return

    if prop_type == "_get":
       self.prop_get_generate(_o, params_tmp)

    elif prop_type == "_set":
       self.prop_set_generate(_o, params_tmp)


  #is called by visit_Func to parse function as a method
  def visit_method(self, _o):

    if _o.name in ["event_global_freeze", "event_global_thaw"]:
      self.c_file.functions.append("Handle<Value> %s(const Arguments& args)\n"%_o.name)
      self.c_file.functions.append("{\n")
      self.c_file.functions.append("  eo_class_do(%s, eo_%s());\n"%(_o.cl_obj.macro,_o.name))
      self.c_file.functions.append("  return Undefined();\n")
      self.c_file.functions.append("}\n")
      return

    #do not need to 
    self.c_file.cb_generate_macros.append("EO_GENERATE_METHOD_CALLBACKS(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))
    self.class_info.public.append("   Handle<Value> %s(const Arguments&);\n"%(_o.name))

    self.c_file.tmpl.append("   METHOD(%s)"% _o.name)
    self.h_file.meth_cb_headers.append("   Handle<Value> Callback_%s(const Arguments&);\n"%(_o.name))


    self.c_file.functions.append("Handle<Value> %s::%s(const Arguments& args)\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.functions.append("{\n")
    self.c_file.functions.append("   HandleScope scope;\n")

    pass_params = []
    ret_params = []
    in_param_counter = 0
    for i, (n, c_t, d, p_t) in enumerate(_o.parameters):
      c_t_tmp = self.cast(p_t)

      js_type = ""
      c_t_internal = ""

      if c_t_tmp in self.internal_types:
        c_t_internal = self.internal_types[c_t_tmp][0]
        js_type = self.internal_types[c_t_tmp][2]
      else:
        print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, m)
        continue

      if d == "in":
        self.c_file.functions.append("   Local<Value> _%s = args[%d];\n"%(n, in_param_counter))
        in_param_counter += 1
        self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))

        if js_type == "ToString":
          self.c_file.functions.append("  %s = strdup(*String::Utf8Value(_%s->%s()));\n"%(n, n, js_type))
        elif js_type == "ToObject":
          self.c_file.functions.append("   %s = static_cast<CElmObject*>(_%s->ToObject()->GetPointerFromInternalField(0))->GetEo();\n"%(n, n))
        else:
          self.c_file.functions.append("   %s = _%s->%s()->Value();\n"%(n, n, js_type))
        if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
          pass_params.append('&' + n)
        else:
          pass_params.append(n)
      elif d == "out":
        self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))
        pass_params.append('&' + n)

        js_type = self.js_types[js_type]
        ret_params.append((n, js_type))

      elif d == "in,out":
        self.c_file.functions.append("   Local<Value> _%s = args[%d];\n"%(n, in_param_counter))
        in_param_counter += 1
        self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))

        if js_type == "ToString":
          self.c_file.functions.append("  %s = strdup(*String::Utf8Value(_%s->%s()));\n"%(n, n, js_type))
        elif js_type == "ToObject":
          self.c_file.functions.append("   %s = static_cast<CElmObject*>(_%s->ToObject()->GetPointerFromInternalField(0))->GetEo();\n"%(n, n))
        else:
          self.c_file.functions.append("   %s = _%s->%s()->Value();\n"%(n, n, js_type))

        pass_params.append('&' + n)
        js_type = self.js_types[js_type]
        ret_params.append((n, js_type))

    self.c_file.functions.append("   eo_do(eobj, %s(%s));\n"%( _o.c_macro, ", ".join(pass_params)))

    if len(ret_params) == 1:
      for par, t in ret_params:
#FIXME: case then we work with EO
        self.c_file.functions.append("   return scope.Close(%s::New(%s));//need to put proper values\n"%(t, par))
    elif len(ret_params) > 1:
      self.c_file.functions.append("   Local<Object> obj__ = Object::New();\n")
      for p, t in ret_params:
         self.c_file.functions.append("   obj__->Set(String::NewSymbol(\"%s\"), %s::New(%s));\n"%(p, t, p))
      self.c_file.functions.append("   return scope.Close(obj__); //need to put proper values\n")
    else:
      self.c_file.functions.append("   return Undefined();\n")

    self.c_file.functions.append("}\n")
    self.c_file.functions.append("\n")

  # is called by prop_set_get_visit, to generate body for property getter
  def prop_get_generate(self, _o, params_tmp):
    self.c_file.functions.append("Handle<Value> %s::%s() const\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.functions.append("{\n")
    self.c_file.functions.append("   HandleScope scope;\n")

    pass_params = []
    ret_params = []
    for (c_t, n, d, c_t_internal, js_type) in params_tmp:

      self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))
      pass_params.append('&' + n)

      js_type = self.js_types[js_type]
      ret_params.append((n, js_type))

    self.c_file.functions.append("   eo_do(eobj, %s(%s));\n"%(_o.c_macro, ", ".join(pass_params)))

    if len(ret_params) == 1:
      for par, t in ret_params:
        self.c_file.functions.append("   return scope.Close(%s::New(%s));//need to put proper val     ues\n"%(t, par))

    elif len(ret_params) > 1:
       self.c_file.functions.append("   Local<Object> obj__ = Object::New();\n")
       for par, t in ret_params:
         self.c_file.functions.append("   obj__->Set(String::NewSymbol(\"%s\"), %s::New(%s));\n"%     (par, t, par))
       self.c_file.functions.append("   return scope.Close(obj__);//need to put proper values\n")
    else:
       self.c_file.functions.append("   return Undefined();\n")

    self.c_file.functions.append("}\n\n")


  # is called by prop_set_get_visit, to generate body for property setter
  def prop_set_generate(self, _o, params_tmp):

    self.c_file.functions.append("void %s::%s(Handle<Value> val)\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.functions.append("{\n")

    pass_params = []
    add_end_func = []
    if len(params_tmp) > 1:
      self.c_file.functions.append("   Local<Object> __o = val->ToObject();\n")

      for (c_t, n, d, c_t_internal, js_type) in params_tmp:

        self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))
        if js_type == "ToString":
           self.c_file.functions.append("   %s = strdup(*String::Utf8Value(__o->Get(String::NewSymbol(\"%s\"))->%s()));\n"%(n, n, js_type))
        else:
           self.c_file.functions.append("   %s = __o->Get(String::NewSymbol(\"%s\"))->%s()->Value();\n"%(n, n, js_type))

        if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
          pass_params.append('&' + n)
        else:
          pass_params.append(n)

    elif len(params_tmp) == 1:
      for (c_t, n, d, c_t_internal, js_type) in params_tmp:
         self.c_file.functions.append("   %s %s;\n"%(c_t_internal, n))
         if js_type == "ToString":
           self.c_file.functions.append("   %s = strdup(*String::Utf8Value(val->%s()));\n"%(n, js_type))
           add_end_func.append("  free(%s);"%n)
         else:
           self.c_file.functions.append("   %s = val->%s()->Value();\n"%(n, js_type))

         if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
           pass_params.append('&' + n)
         else:
           pass_params.append(n)

    self.c_file.functions.append("   eo_do(eobj, %s(%s));\n"%(_o.c_macro, ", ".join(pass_params)))
    self.c_file.functions += add_end_func
    add_end_func = []
    self.c_file.functions.append("}\n")
    self.c_file.functions.append("\n")




  def visit_Init(self, _o):

    self.c_file.name = _o.cl_obj.js_cc_file
    self.h_file.name = _o.cl_obj.js_h_file

    self.c_file.header.append("/**\n * generated from \"%s\"\n */\n"%(_o.cl_obj.source_file))
    self.c_file.header.append("#include \"%s\"\n"%(os.path.split(_o.cl_obj.js_h_file)[1] ))
    self.c_file.header.append("namespace elm {\n\n")
    self.c_file.header.append("using namespace v8;\n\n")

    self.h_file.header.append("/**\n * generated from \"%s\"\n */\n"%(_o.cl_obj.source_file))
    self.h_file.header.append("#ifndef %s\n"%(("_JS_"+_o.cl_obj.mod_name+"_h_").upper() ))
    self.h_file.header.append("#define %s\n"%(("_JS_"+_o.cl_obj.mod_name+"_h_").upper() ))
    self.h_file.header.append("\n")
    self.h_file.header.append("#include \"elm.h\" //macro defines, common functions\n")
    self.h_file.header.append("#include \"CElmObject.h\" //base object\n")
    self.h_file.header.append("#include \"%s\" //eo-class include file\n"%(_o.cl_obj.includes[0]))

#FIXME have to guess about filenames to include. (need to move it into js_obj_parse and save in "includes" array)
    for l in _o.cl_obj.parents:
       self.h_file.header.append("#include \"%s\" //include generated js-wrapping classes\n"%("_" + l.lower() + ".h"))

    lst = ["public virtual CElmObject"]
    for l in _o.cl_obj.parents:
      lst.append("public virtual %s"%(l))

    inherit = ", ".join(lst)
    self.class_info.header ="class %s : %s\n"%(_o.cl_obj.kl_id, inherit)


    if _o.cl_obj.eo_type == const.CLASS_TYPE_REGULAR:
      self.class_info.private.append("   static Persistent<FunctionTemplate> tmpl;\n")
      self.class_info.private.append("\n")

      #implementing constructor
      self.class_info.protected.append("   %s(Local<Object> _jsObject, CElmObject *parent);\n"%(_o.cl_obj.kl_id))
      self.c_file.functions.append("%s::%s(Local<Object> _jsObject, CElmObject *parent)\n"%(_o.cl_obj.kl_id, _o.cl_obj.kl_id))
      self.c_file.functions.append(" : CElmObject(_jsObject, eo_add(%s , parent ? parent->GetEo() : NULL))\n"%(_o.cl_obj.macro))
      self.c_file.functions.append("{\n   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));\n}\n")

      self.class_info.protected.append("   static Handle<FunctionTemplate> GetTemplate();\n")
      self.class_info.protected.append("\n")

      self.class_info.public.insert(0, "   static void Initialize(Handle<Object> target);\n")


      #implementing Initialize
      self.c_file.init_f.append("void %s::Initialize(Handle<Object> target)\n"%_o.cl_obj.kl_id)
      self.c_file.init_f.append("{\n")
      self.c_file.init_f.append("   target->Set(String::NewSymbol(\"%s\") , GetTemplate()->GetFunction());\n"%_o.cl_obj.kl_id)
      self.c_file.init_f.append("}\n")

      self.class_info.public.insert(0, "   virtual void DidRealiseElement(Local<Value> obj);\n")

      #implementing DidRealise
      self.c_file.functions.append("void %s::DidRealiseElement(Local<Value> obj)\n {\n\
                  (void) obj;\n\
                  }\n"%_o.cl_obj.kl_id)

      self.class_info.public.insert(0, "   friend Handle<Value> CElmObject::New<%s>(const Arguments& args);\n"%(_o.cl_obj.kl_id))
      self.class_info.public.append("\n")


    #default constructors - destructors
    self.class_info.protected.append("   %s();\n"%(_o.cl_obj.kl_id))
    self.c_file.functions.append("%s::%s(){}\n\n"%(_o.cl_obj.kl_id, _o.cl_obj.kl_id));
    self.c_file.functions.append("%s::~%s(){} //need to add destruction of cb variables\n\n"%(_o.cl_obj.kl_id, _o.cl_obj.kl_id));

    self.class_info.protected.append("   virtual ~%s();\n"%(_o.cl_obj.kl_id))




  #saving data to pxi file
  def js_cc_file_to_dir_save(self, _outdir):
    lines = []

    for line in self.c_file.header:
      lines.append(line)

    for line in self.c_file.cb_generate_macros:
      lines.append(line)

    for line in self.c_file.functions:
      lines.append(line)

    if self.c_file.tmpl != "":
      tmpl = ",\n".join(self.c_file.tmpl)
      lines.append("\nGENERATE_TEMPLATE(%s);\n\n"%tmpl)

    if self.c_file.init_f != []:
      self.c_file.init_f.pop(-1)
      self.c_file.init_f += self.c_file.init_f_addition
      self.c_file.init_f.append("}")


      for line in self.c_file.init_f:
        lines.append(line)

    lines.append("\n} //end namespace elm\n\n")
    f = open (self.c_file.name, 'w')
    for line in lines:
      f.write(line)
    f.close()


  def js_h_file_to_dir_save(self, _outdir):
    lines = []

    for line in self.h_file.header:
      lines.append(line)

    lines.append("\n")
    lines.append("namespace elm { //namespace should have the same meaning as module for python\n")
    lines.append("\n")

    lines.append("using namespace v8;\n")
    lines.append("\n")
    lines.append(self.class_info.header)
    lines.append("{\n") # open class

    lines.append("private:\n")
    for line in self.class_info.private:
      lines.append(line)

    lines.append("protected:\n")
    for line in self.class_info.protected:
      lines.append(line)

    if len(self.h_file.ev_list) != 0:
      lines.append("\n   struct {\n")
      for line in self.h_file.ev_list:
        lines.append(line)
      lines.append("   } cb;\n\n")

    lines.append("public:\n")
    for line in self.class_info.public:
      lines.append(line)

    lines.append("}; // end class\n") # close class

    lines.append("\n/* properties callbacks*/\n") 
    for line in self.h_file.prop_cb_headers:
      lines.append(line)

    lines.append("\n/* methods callbacks*/\n") 
    for line in self.h_file.meth_cb_headers:
      lines.append(line)

    lines.append("\n/* properties(events) callbacks*/\n") 
    for line in self.h_file.ev_cb_headers:
      lines.append(line)

    lines.append("\n")
    lines.append("} //end namespace elm\n")

    lines.append("\n")
    lines.append("#endif\n")

    f = open (self.h_file.name, 'w')
    for line in lines:
      f.write(line)
    f.close()




#  PyVisitor
#  Py code generation. Generates code depending on object type(input data)
#  Under  "object type" we understand just some set of data, which has 
#  the same rules of generation
#

class PyVisitor(Visitor):

  def __init__(self):
     #  PyVisitor generates 2 types of files: pxi and pxd
     #  head, ev, funcs_parsed - are hooks for different parts of source code

     self.visited_properties = []

     self.pxi = Abstract()
     self.pxi.name = ""
     self.pxi.head = []
     self.pxi.ev = []
     self.pxi.funcs_parsed = []


     self.pxd = Abstract()
     self.pxd.name = ""
     self.pxd.head = []
     self.pxd.ev = []

     self._funcs = {"instance_set2" : "_eo_instance_set2",
                    "instance_get" : "_eo_instance_get",
                    "do" : "eo_do"}

     self.basemodule = {"macro" : "EO_DEFAULT_CLASS",
                           "module" : "eodefault",
                           "name": "EoDefault",
                           "parentmodule": "NULL",
                           "type" :"EO_CLASS_TYPE_REGULAR_NO_INSTANCE",
                           ".pyx" : "eodefault.pyx",
                           ".pxd" : "eodefault.pxd"}

     self.python_reserved_words = ["raise", "del"]

  def cast(self, _in):
    t = _in

    for k in self.primary_types:
      if t.find(k) != -1:
        t = t.replace(k, self.primary_types[k])
    return t



  #generating function code
  def visit_Func(self, _o):
#     print "func Func: ", _o.name, _o.op_id, _o.c_macro, _o.parameters
     eo_base_ops = ["EO_BASE_SUB_ID_EVENT_FREEZE", "EO_BASE_SUB_ID_EVENT_FREEZE_GET", \
                       "EO_BASE_SUB_ID_EVENT_THAW", "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE",
                       "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET",\
                       "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW", "EO_BASE_SUB_ID_DATA_SET", \
                       "EO_BASE_SUB_ID_DATA_GET", "EO_BASE_SUB_ID_DATA_DEL", \
                       "EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD",
                       "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL", \
                       "EO_BASE_SUB_ID_EVENT_CALLBACK_CALL"]

     in_params = []
     pass_params =[]
     ret_params = []
     function_lines = []
     cl_obj = _o.cl_obj

     #Hardcoded generation of functions fo Eo Base class
     if cl_obj.kl_id == "EoBase":
       if_ret = False
       if _o.op_id not in eo_base_ops:
          return
       if _o.op_id == "EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD":
         function_lines.append("def event_callback_priority_add(self, long _desc, int _priority, object _cb):")
         function_lines.append("  if not callable(_cb):")
         function_lines.append("    raise TypeError(\"func must be callable\")")
         function_lines.append("  cdef Eo_Event_Cb cb = <Eo_Event_Cb> eodefault._object_callback")
         function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD), _desc, _priority, cb, <void*>_cb)")
         if_ret = True

       elif _o.op_id == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL":
         function_lines.append("def event_callback_del(self, long _desc, object _func):")
         function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
         function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL), _desc, func, <void*>_func)")

         function_lines.append("\n")
         if_ret = True
       elif _o.op_id == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY":
         function_lines.append("def event_callback_del_lazy(self, long _desc, object _func):")
         function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
         function_lines.append("  cdef void * user_data")
         function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY), _desc, func, &user_data)")
         function_lines.append("  return None if user_data == NULL else <object>user_data")
         if_ret = True

       elif _o.op_id == "EO_BASE_SUB_ID_DATA_SET":
         function_lines.append("def data_set(self, object _key, object _data):")
         function_lines.append("  _key = pytext_to_utf8(_key)")
         function_lines.append("  cdef char* key = <char*> _key")
         function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)")

         function_lines.append("")
         function_lines.append("def _data_set(self, object _key, object _data):")
         function_lines.append("  _key = pytext_to_utf8(_key)")
         function_lines.append("  cdef char* key = <char*> _key")
         function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)")

         if_ret = True

       elif _o.op_id == "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE":
         function_lines.append("@staticmethod")
         function_lines.append("def event_global_freeze():")
         function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE))");
         if_ret = True

       elif _o.op_id == "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET":
         function_lines.append("@staticmethod")
         function_lines.append("def event_global_freeze_get():")
         function_lines.append("  cdef int fcount");
         function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET), &fcount)");
         function_lines.append("  fcount_ = <object>fcount");
         function_lines.append("  return (fcount_)");

         if_ret = True

       elif _o.op_id == "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW":
         function_lines.append("@staticmethod")
         function_lines.append("def event_global_thaw():")
         function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_THAW))");
         if_ret = True

       if if_ret:
         function_lines.append("\n")
         self.pxi.funcs_parsed += function_lines
         return


     if True:#"parameters" in fparams:

       for i, (n, c_t, d, p_t) in enumerate(_o.parameters):
         c_t_tmp = self.cast(p_t)

         py_type = ""
         c_t_internal = ""

         if c_t_tmp in self.internal_types:
            c_t_internal = self.internal_types[c_t_tmp][0]
            py_type = self.internal_types[c_t_tmp][1]
         else:
            print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, _o.name)
            return

         if d == "in":
           in_params.append(py_type + ' _' + n)
           if c_t_internal == "Eo*":
             l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n + ".eo")
           elif c_t_internal == "Eo_Event_Cb":
             l = "  cdef %s %s = <%s> %s"%(c_t_internal, n, c_t_internal, "eodefault._object_callback")
           else:
             if c_t_internal == "char*" :
               l = "  _%s = pytext_to_utf8(_%s)"%(n, n)
               function_lines.append(l)
             l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n)
           function_lines.append(l)


           if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
             pass_params.append('&' + n)
           else:
             pass_params.append(n)

         elif d == "out":
           l = "  cdef %s %s"%(c_t_internal, n)
           pass_params.append('&' + n)
           ret_params.append((n + '_', c_t_internal))
           function_lines.append(l);

         elif d == "in,out":
           in_params.append('_' + n)
           pass_params.append('&' + n)
           if c_t_internal == "Eo*":
             l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n + ".eo")
           else:
             l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n)
           ret_params.append((n + '_', c_t_internal))
           function_lines.append(l);

     in_params.insert(0, "self")


     if _o.name in self.python_reserved_words:
        func_name = _o.name + "_"
        print "Warning: method name: \"%s\" for class : \"%s\" has been changed to \"%s\""%(_o.name,  cl_obj.kl_id, func_name)
     else:
        func_name = _o.name

     l = "def %s(%s):"% (func_name, ', '.join(in_params))
     function_lines.insert(0, l)

     l = '%s(%s.%s)'%(cl_obj.sub_id_function,
                                   cl_obj.mod_name,
                                   _o.op_id)

     pass_params.insert(0, l)
     l = "%s.%s(self)"%(cl_obj.basemodule, self._funcs["instance_get"])
     pass_params.insert(0, l)
     l = '  %s.%s(%s)'% (cl_obj.basemodule, self._funcs["do"],', '.join(pass_params))
     function_lines.append(l);

     ret_params_tmp = []
     if len(ret_params) > 0:
       for p, t in ret_params:
         if t.find('*') != -1:
           l = '  %s = None if %s == NULL else <object>%s'%(p, p[:-1], p[:-1])
           function_lines.append(l)
         else:
           l = '  %s = <object>%s'% (p, p[:-1])
           function_lines.append(l)
         ret_params_tmp.append(p)

       l = '  return (%s)'% (', '.join(ret_params_tmp))
       function_lines.append(l)

     function_lines.append("")
     self.pxi.funcs_parsed += function_lines


  #generating __init_function, and all header data for files
  def visit_Init(self, _o):
    cl_obj = _o.cl_obj

    function_lines = []
    l = "def __init__(self, EoDefault parent):"
    function_lines.append(l)

    l = "  instantiateable = %s"%(cl_obj.instantiateable)
    function_lines.append(l)

    l = "  if not instantiateable:"
    function_lines.append(l)
    l = "    print \"Class '%s' is not instantiate-able. Aborting.\"%(self.__class__.__name__)"

    function_lines.append(l)
    l = "    exit(1)"
    function_lines.append(l)

    if cl_obj.instantiateable == "True":
      l = "  klass = <long>%s.%s()"%(cl_obj.mod_name, cl_obj.get_function)
      function_lines.append(l)
      l = "  self.%s(klass, parent)"%self._funcs["instance_set2"]
      function_lines.append(l)
      l = "  self.data_set(EoDefault.PY_EO_NAME, self)"
      function_lines.append(l)
    function_lines.append("")

    function_lines.append("")

    self.pxi.funcs_parsed += function_lines


    self.pxi.name = cl_obj.mod_name + ".pxi"
    self.pxd.name = cl_obj.mod_name  + ".pxd"

    pattern = "########################################################"
    l = '%s\n##\n## generated from from \"%s\"\n##\n%s'%(pattern, cl_obj.source_file, pattern)
    self.pxi.head.append(l + '\n')
    self.pxd.head.append(l + '\n')


    #inserting cimports
    l = "cimport %s"%cl_obj.mod_name
    self.pxi.head.append(l)
    l = "cimport %s"%cl_obj.basemodule
    self.pxi.head.append(l + '\n')

    #defining class
    parents = []
    if len(cl_obj.parents) != 0:
       parents = cl_obj.parents

    if cl_obj.kl_id == "EoBase":
       parents = []
       parents.append(self.basemodule["name"])
       l = "from %s import %s"%(self.basemodule["module"], self.basemodule["name"])
       self.pxi.head.append(l + "\n")

    if "EoBase" in parents:
       l = "from %s import %s"%("eobase", "EoBase")
       self.pxi.head.append(l + "\n")

    l = "from %s import %s"%(self.basemodule["module"], "pytext_to_utf8")
    self.pxi.head.append(l + "\n")

    #defining _id function
    if cl_obj.extern_base_id != "":
      l = 'cdef int %s(int sub_id):'%(cl_obj.sub_id_function)
      self.pxi.head.append(l)
      l = '  return %s.%s + sub_id'%(cl_obj.mod_name, cl_obj.extern_base_id)
      self.pxi.head.append(l + '\n')

    #defining class
    parents = ','.join(parents)
    l = 'class %s(%s):'%(cl_obj.kl_id, parents)

    self.pxi.head.append(l)

    #inserting cimports
    l = "from %s cimport *"%(cl_obj.basemodule)
    self.pxd.head.append(l + '\n')

    #inserting externs from H
    l = "cdef extern from \"%s\":"%(cl_obj.includes[0])
    self.pxd.head.append(l + '\n')


    if cl_obj.extern_base_id != "":
       l = '  %s %s'%("Eo_Op", cl_obj.extern_base_id)
       self.pxd.head.append(l + '\n')

    enum_lines = []
    enum_lines.append("  ctypedef enum:")
    for v in cl_obj.op_ids:
      #inserting extern enums from H into temp list
      if len(enum_lines) > 1 :
        enum_lines[-1] = enum_lines[-1] + ','
      enum_lines.append('    ' + v)

    if len(enum_lines) > 1:
        for l in enum_lines:
            self.pxd.head.append(l)
        self.pxd.head.append('\n')

    for v in cl_obj.extern_funcs:
        l = '  %s %s'%(v[1], v[0])
        self.pxd.head.append(l)


  #generating event defenitions
  def visit_Ev(self, _o):
    #defining event globals
    v = _o.ev_id
    pos = v.find("EV_")
    if pos == -1:
      return
    name = v[pos + 3:]
    l = "  %s = <long>%s.%s"%(name, _o.cl_obj.mod_name, v)
    self.pxi.ev.append(l)
    l = '  %s %s'%("Eo_Event_Description *", v)
    self.pxd.ev.append(l)


  #saving data to pxi file
  def pxi_file_to_dir_save(self, _outdir):
    f = open(os.path.join(_outdir, self.pxi.name), 'w')

    lst = self.pxi.head
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxi.ev
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxi.funcs_parsed
    for l in lst:
       f.write('  ' + l + '\n')
    f.write("\n")
    f.close()


  #saving data to pxd file
  def pxd_file_to_dir_save(self, _outdir):

    f = open(os.path.join(_outdir, self.pxd.name), 'w')
    lst = self.pxd.head
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxd.ev
    for l in lst:
       f.write(l+'\n')
    f.write("\n")
    f.close()



class XMLparser(object):
    def __init__(self):

        self.objects = {}
        self.objects_incl = {}

        self.python_reserved = {"pass"}

        self.source_file = ""
        self.includes = []
        self.ev_ids = []
        self.op_ids = []
        self.extern_funcs = []

        self.class_data = {}
        self.functions = {} #function names with parameters
        self.current_func = ""

    #parsing function for expat parser
    def start_element_handler(self, name, attrs):
        #converting unicode to ascii
        attrs_ascii = {}
        for key, val in attrs.iteritems():
            attrs_ascii[key.encode("ascii")] = val.encode("ascii")
        attrs = attrs_ascii

        if name == const.METHOD:
            self.current_func = attrs[const.NAME]
            self.functions.setdefault(self.current_func, {const.OP_ID : attrs[const.OP_ID], const.C_MACRO : attrs[const.C_MACRO], const.PARAMETERS:[]})

        elif name == const.PARAMETER:
            func_att = self.functions[self.current_func]
            #par_att = func_att.setdefault('parameters', [])
            par_att = func_att[const.PARAMETERS]
            name = attrs[const.NAME]
            if name in self.python_reserved:
              name += "__"
            par_att.append((name, attrs[const.C_TYPENAME], attrs[const.DIRECTION], attrs[const.PRIMARY_TYPE]))

        elif name == const.INCLUDE:
            self.includes.append(attrs[const.NAME])

        elif name == const.CLASS:
            self.class_data = attrs
            self.class_data[const.BASE_ID] = ""

        elif name == const.XML_SUB_ID:
            self.op_ids.append(attrs[const.NAME])

        elif name == const.EVENT:
            self.ev_ids.append(attrs[const.NAME])

        elif name == const.BASE_ID:
            self.class_data[const.BASE_ID] = attrs[const.NAME]

        elif name == const.EXTERN_FUNCTION:
            self.extern_funcs.append((attrs[const.NAME], attrs[const.TYPENAME]))

        else:
            pass


    #main XML parsing function
    #parses all XML, initializes field of class structure
    def parse(self, fName):
        self.source_file = fName
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element_handler
        p.ParseFile(open(fName, 'r'))

        if self.class_data == {}:
           return
        mod_name = normalize_names([self.class_data[const.C_NAME]])[0].lower()
        #defining _id function
        if self.class_data[const.BASE_ID] != "":
          self.class_data["sub_id_function"] = '%s_sub_id'%(mod_name)
        else:
          self.class_data["sub_id_function"] = ""

        parent_list = []
        parent_list.append(self.class_data[const.PARENT])
        parent_list += self.class_data["extensions"].split(",")

        mod_o = Mod()
        mod_o.kl_id = self.class_data[const.C_NAME]
        mod_o.c_name = self.class_data[const.C_NAME]
        mod_o.macro = self.class_data[const.MACRO]
        mod_o.eo_type = self.class_data[const.TYPE]
        mod_o.get_function = self.class_data[const.GET_FUNCTION]
        mod_o.instantiateable = self.class_data[const.INSTANTIATEABLE]
        mod_o.includes = self.includes
        mod_o.visitees = {}
        mod_o.mod_name = mod_name
        mod_o.basemodule = "eodefault"
        mod_o.op_ids = self.op_ids
        mod_o.ev_ids = self.ev_ids
        mod_o.extern_base_id = self.class_data["base_id"]
        mod_o.extern_funcs = self.extern_funcs
        mod_o.sub_id_function = self.class_data["sub_id_function"]
        mod_o.source_file = self.source_file
        mod_o.parents = parent_list

        # Saving function's description as Func object
        # Defining if current function can be set/get property, property type is saved in seperate field
        # Properties are relevant only for JS
        for i in self.functions:
          T = ""
          prop_name = i
          if mod_o.kl_id == "Eo Base":
            T = const.METHOD
            mod_o.visitees[i] = Func(i, prop_name, self.functions[i][const.OP_ID], self.functions[i][const.C_MACRO], self.functions[i][const.PARAMETERS], T, mod_o)
            continue
          if i[-4:] == "_set":
            prop_name = i[:-4]
            if i[:-4]+"_get" in self.functions:
              T = const.SET_GET
            else:
              T = const.SET_ONLY
          elif i[-4:] == "_get":
            prop_name = i[:-4]
            if i[:-4]+"_set" in self.functions:
              T = const.SET_GET
            else:
              T = const.GET_ONLY
          else:
            T = const.METHOD
          mod_o.visitees[i] = Func(i, prop_name, self.functions[i][const.OP_ID], self.functions[i][const.C_MACRO], self.functions[i][const.PARAMETERS], T, mod_o)


        for i in self.ev_ids:
          mod_o.visitees[i] = Ev(i, mod_o)

        mod_o.visitees["__init__"] = Init(mod_o)

        self.objects[mod_o.kl_id] = mod_o
        del mod_o

        self.functions = {}
        self.includes = []
        self.op_ids = []
        self.ev_ids = []
        self.extern_funcs = []
        self.class_data = {}


    #For each class(object) in current tree, checks if parent is also in current tree.
    #Returns list of all perents which are not in current tree


    def module_parse(self, _module_name, _xml_files, _incl_dirs):

      for f in _xml_files:
        self.parse(f)

      #excluding everything, but the "eobase", if building eobse
      #excluding "eobase" module, if building non-eobase module
      if _module_name == "eobase":
        if "Eo Base" in self.objects:
          cl_data_tmp = dict(self.objects)
          self.objects = {}
          self.objects["Eo Base"] = cl_data_tmp["Eo Base"]
          del cl_data_tmp
        else:
          print "ERROR: source files for module \"EoBase\" not found"
          exit(1)
      else:
        if "Eo Base" in self.objects:
          self.objects.pop("Eo Base")
          print("Warning: EoBase module was removed from building tree")

      parents_to_find =  self.parents_to_find_get()

      if parents_to_find:

        if len(_incl_dirs) == 0:
          print "No XML directory was provided"

        xml_files = dir_files_get(_incl_dirs)
        xml_files = filter(isXML, xml_files)

        if len(xml_files) == 0:
          print "ERROR: no include files found for %s classes... Aborting...(Use: --include=INCLUDE_DIR)"% ",".join(parents_to_find)
          exit(1)

    #Creating temp parser to look for parents in include files.
        xp_incl = XMLparser()
        for f in xml_files:
          xp_incl.parse(f)

        #Looking for parents, and saving proper object in include dictionary
        #FIXME: but later I never use it ??
        for n, o in xp_incl.objects.items():
          if n in parents_to_find:
            i = parents_to_find.index(n)
            parents_to_find.pop(i)
            n = normalize_names([n])[0]
            self.objects_incl[n] = o

        del xp_incl

        if len(parents_to_find) != 0:
          print "ERROR: XML files weren't found for %s classes... Aborting"%(",".join(parents_to_find))
          exit(1)




    def parents_to_find_get(self):
       list_of_parents = []

       for n, o in self.objects.items():
         o.parents = filter(len, o.parents)
         list_of_parents += o.parents

       list_of_parents = list(set(list_of_parents))

       parents_to_find = filter(lambda l: True if l not in self.objects else False, list_of_parents)
       return parents_to_find

    """
    def print_data(self):
      for n, o in self.objects.items():
        print ""
        print n
        for kk in self.cl_data[klass]:
          print "  ", kk, " : ", type(self.cl_data[klass][kk])
          d = self.cl_data[klass][kk]
          spaces = " " * 15
          if type(d) == str:
            print spaces, d
          elif type(d) == dict:
            for key in d:
              print spaces, key, " : ", d[key]
          elif type(d) == list:
            for l in d:
              print spaces, l
"""

#FIXME move this function to eo_py_gen

    #Changes order of parents for python inheritance.
    #This is made to support C3 MRO algorithm
    def reorder_parents(self, p_list):
      if len(p_list) < 2:
        return p_list
      parent_l = []
      mixin_l = []
      other_l = []

      tmp_parents_list =  p_list[:]
      parent_l.append(tmp_parents_list[0])
      tmp_parents_list.pop(0)

      for l in tmp_parents_list:
         #FIXME: where to look for included classes
        cl_type = self.objects[l].eo_type if l in self.objects else self.objects_incl[l].eo_type
#        cl_type = self.objects[l].eo_type
        if cl_type == const.CLASS_TYPE_MIXIN: # "EOBJ_CLASS_TYPE_MIXIN":
          mixin_l.append(l)
        else:
          other_l.append(l)

      mixin_l.reverse()
      other_l.reverse()

      del tmp_parents_list
      lst = []
      lst = mixin_l + other_l + parent_l

      return lst


    #Creates list all all parents in current tree, for kl - class
    def get_parents(self, kl):
      prnts = self.objects[kl].parents
      l = []
      for p in prnts:
        if p != "EoBase":
          l = l + self.get_parents(p)

      l = list(set(l + prnts))
      return l


    #normalize all names and ids, which depend in C class name.
    #T.e. Some_Class name -> SomeClassName
    def normalize_module_names(self):
      objects_tmp = {}
      for n, o in self.objects.items():
        o.c_name = normalize_names([o.c_name])[0]
        o.kl_id = normalize_names([o.kl_id])[0]
        o.parents = normalize_names(o.parents)
        objects_tmp[o.kl_id] = o
      self.objects = objects_tmp


    def py_code_generate(self, module_name ,outdir):
      #normalizing names for each class object (Evas_Object Class -> EvasObjectClass)
      self.normalize_module_names()

      #reodering parents and generating source code
      for n, o in self.objects.items():
        o.parents = self.reorder_parents(o.parents)

        o.V = PyVisitor()
        o.resolve()

      #saving files
      for n, o in self.objects.items():
        o.V.pxi_file_to_dir_save(outdir)
        o.V.pxd_file_to_dir_save(outdir)

      #generating  "pyx" module file,
      #which simply includes source files "pxi" of each class
      #building right order of including files
      cl_parents = {}
      lst = []
      for n, o in self.objects.items():
        cl_parents[n] = o.parents

      tmp = dict(cl_parents)

      cont = True
      while cont:
        cont = False
        for k in cl_parents:
          can_add = True
          for p in cl_parents[k]:
            if p in tmp:
              can_add = False
          if can_add is True:
            lst.append(k)
            tmp.pop(k)
            cont = True
        cl_parents = dict(tmp)
      if len(tmp) > 0:
        print "ERROR: can't resolve classes include order"
        exit(1)

      lines = []
      lines.append("from eodefault cimport *\n")
      for k in lst:
        lines.append("include \"%s\""%self.objects[k].V.pxi.name)
        #FIXME adding filenames of include modules?

      f = open (os.path.join(outdir, module_name + ".pyx"), 'w')
      for l in lines:
        f.write(l + "\n")
      f.close()

    def js_code_generate(self, outdir):

      self.normalize_module_names()
      for n, o in self.objects.items():
         o.js_h_file = os.path.join(outdir, "_" + o.mod_name + ".h")
         o.js_cc_file = os.path.join(outdir, "_" + o.mod_name + ".cc")

      eo_base_ops = ["INIT", "EO_BASE_SUB_ID_EVENT_FREEZE", "EO_BASE_SUB_ID_EVENT_FREEZE_GET", "EO_BASE_SUB_ID_EVENT_THAW", "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE", "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW"]

      for n, o in self.objects.items():
        if n == "EoBase":
          funcs_tmp = dict(o.visitees)
          for f_n, f in funcs_tmp.items():
            if f.__class__.__name__ == "Func" and  f.op_id not in eo_base_ops:
              o.visitees.pop(f_n)

      #Iterating through each object. Assigning Visitor object
      for n, o in self.objects.items():

        o.V = JsVisitor()
        par = self.get_parents(o.kl_id)
        #elements - it's internal property, to be able to nest objects
        o.V.c_file.tmpl.append("   %s"%"PROPERTY(elements)")

      #For each class object template should be generated.
      #Template must include each parent's property.(or maybe not, if this prop is private)
      #As soon as I do it without auto inheritance, because JS supports only single inheritance,
      #I have to manually iterate through all parents and add properties and methods into template
      #
        for p in par:
          if p in self.objects:
             parent_obj = self.objects[p]
          else:
             parent_obj = self.objects_incl[p]

          for n, f in parent_obj.visitees.items():
            if f.__class__.__name__ == "Func":
               if parent_obj.kl_id == "Eo Base":
                  if f.op_id not in eo_base_ops    :
                    continue
                  else:
                    if f.name in ["event_global_freeze","event_global_thaw"]:
                       o.V.c_file.init_f_addition.append("EO_REGISTER_STATIC_METHOD(%s);\n"%f.name)
                       o.V.c_file.functions.append("static Handle<Value> %s(const Arguments& args)\n"%f.name)
                       o.V.c_file.functions.append("{\n")
                       o.V.c_file.functions.append("  eo_class_do(%s, eo_%s());\n"%(o.macro, f.name))
                       o.V.c_file.functions.append("  return Undefined();\n")
                       o.V.c_file.functions.append("}\n")
                       continue
                    else:
                      o.V.c_file.tmpl.append("   METHOD(%s)"%f.name)
                      continue
               if f.prop_type == const.METHOD:
                 o.V.c_file.tmpl.append("   METHOD(%s)"%f.prop_name)
               else:
                 o.V.c_file.tmpl.append("   PROPERTY(%s)"%f.prop_name)
            elif f.__class__.__name__ == "Ev":
               o.V.c_file.tmpl.append("   PROPERTY(%s)"%f.ev_id.lower())

        o.V.c_file.tmpl = list(set(o.V.c_file.tmpl))
        o.V.c_file.tmpl.insert(0, "%s"%o.kl_id)
        o.resolve()

        #if class is not instantiateable, remove template. 
        #It's made here, because I don't want to add this check 
        #on each iteration during property parsing
        if o.instantiateable == "False":
          o.V.c_file.tmpl = ""

      #saving files
      for n, o in self.objects.items():
        o.V.js_cc_file_to_dir_save(outdir)
        o.V.js_h_file_to_dir_save(outdir)

