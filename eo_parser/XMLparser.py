import xml.parsers.expat, os, shutil
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


#  Visitor Design Pattern
#  Visitor - base class for different visitors.
#  visit function implements dispatch depending on class name of object
#

class Visitor(object):
  def visit(self, _p):
    method_name = "visit_" + class_name_get(_p)
    method = getattr(self, method_name, False)
    if callable(method):
      method(_p)
    else:
       print "%s is not callable attribute"%(method_name)


class Abstract(object):
   def __init__(self):
      pass


class JsVisitor(Visitor):

  def __init__(self):
     self.visited_properties = []

     self.c_file = Abstract()
     self.c_file.tmpl = []
     self.c_file.cb_generate_macros = []
     self.c_file.name = ""
     self.c_file.functions = []
     self.c_file.header = []

     self.h_file = Abstract()
     self.h_file.ev_list = []
     self.h_file.name = ""
     self.h_file.header = []
     self.h_file.prop_cb_headers = []
     self.h_file.ev_cb_headers = []
     self.h_file.meth_cb_headers = []

     self.class_info = Abstract()
     self.class_info.header = ""
     self.class_info.private = []
     self.class_info.protected = []
     self.class_info.public = []


  def visit_Func(self, _o):
#     print _o.name, _o.op_id, _o.c_macro, _o.parameters
 #    print _o.prop_type

     if _o.prop_type == const.SET_GET and _o.name not in self.visited_properties:
       _oo = copy.deepcopy(_o)
       _oo.name = _oo.name[:-4]
       self.visit_prop_set_get(_oo)

       self.visited_properties.append(_o.name[:-4]+"_set")
       self.visited_properties.append(_o.name[:-4]+"_get")

     elif _o.prop_type == const.SET_ONLY:
       _oo = copy.deepcopy(_o)
       _oo.name = _oo.name[:-4]
       self.visit_prop_set_only(_oo)

     elif _o.prop_type == const.GET_ONLY:
       _oo = copy.deepcopy(_o)
       _oo.name = _oo.name[:-4]
       self.visit_prop_get_only(_oo)

     elif _o.prop_type == const.METHOD:
       self.visit_method(_o)


  def visit_Ev(self, _o):
    #defining event globals

    ev = _o.ev_id.lower()
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


  def visit_prop_set_get(self, _o):
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_CALLBACKS(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))

    self.class_info.public.append("   Handle<Value> %s_get() const;\n"%(_o.name))
    self.class_info.public.append("   void %s_set(Handle<Value> val);\n"%(_o.name))

    self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(_o.name))
    self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(_o.name))

  def visit_method(self, _o):
    if _o.name in ["event_global_freeze", "event_global_thaw"]:
       return
    self.c_file.cb_generate_macros.append("EO_GENERATE_METHOD_CALLBACKS(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.tmpl.append("   METHOD(%s)"% _o.name)
    self.h_file.meth_cb_headers.append("   Handle<Value> Callback_%s(const Arguments&);\n"%(_o.name))

  def visit_prop_set_only(self, _o):
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_SET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, _o,name))
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_GET_EMPTY_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.tmpl.append("   PROPERTY(%s)"% _o.name)
    self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(_o.name))
    self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(_o.name))

  def visit_prop_get_only(self, _o):
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.cb_generate_macros.append("EO_GENERATE_PROPERTY_GET_CALLBACK(%s, %s);\n"%(_o.cl_obj.kl_id, _o.name))
    self.c_file.tmpl.append("   PROPERTY(%s)"% _o.name)
    self.h_file.prop_cb_headers.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(_o.name))
    self.h_file.prop_cb_headers.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(_o.name))



  def visit_Init(self, _o):
    c_f = []
    h_f = []

    self.c_file.name = _o.cl_obj.js_cc_file
    self.h_file.name = _o.cl_obj.js_h_file

    self.c_file.header.append("/**\n * generated from \"%s\"\n */\n"%(_o.cl_obj.source_file))
    self.c_file.header.append("#include \"%s\"\n"%(os.path.split(_o.cl_obj.js_h_file)[1] ))
    self.c_file.header.append("namespace elm {\n\n")
    self.c_file.header.append("using namespace v8;\n\n")

    self.h_file.header.append("/**\n * generated from \"%s\"\n */\n"%(_o.cl_obj.source_file))
    self.h_file.header.append("#ifndef %s\n"%( ("_JS_"+_o.cl_obj.mod_name+"_h_").upper() ))
    self.h_file.header.append("#define %s\n"%( ("_JS_"+_o.cl_obj.mod_name+"_h_").upper() ))
    self.h_file.header.append("\n")
    self.h_file.header.append("#include \"elm.h\" //macro defines, common functions\n")
    self.h_file.header.append("#include \"CElmObject.h\" //base object\n")
    self.h_file.header.append("#include \"%s\" //eo-class include file\n"%(_o.cl_obj.includes[0]))

#FIXME have to guess about filenames to include. (need to move it into js_obj_parse and save in "includes" array)
    for l in _o.cl_obj.parents:
       self.h_file.header.append("#include \"%s\" //include generated js-wrapping classes\n"%("_" + l.lower() + ".h"))

    h_f.append("\n")
    h_f.append("namespace elm { //namespace should have the same meaning as module for python\n")
    h_f.append("\n")

    h_f.append("using namespace v8;\n")
    h_f.append("\n")

    lst = ["public virtual CElmObject"]
    for l in _o.cl_obj.parents:
      lst.append("public virtual %s"%(l))

    inherit = ", ".join(lst)
    self.class_info.header ="class %s : %s \n"%(_o.cl_obj.kl_id, inherit)

    init_f = []


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
      init_f.append("void %s::Initialize(Handle<Object> target)\n"%_o.cl_obj.kl_id)
      init_f.append("{\n")
      init_f.append("   target->Set(String::NewSymbol(\"%s\") , GetTemplate()->GetFunction());\n"%_o.cl_obj.kl_id)
      init_f.append("}\n")

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



    c_f += init_f
    c_f.append("} //end namespace elm\n")

    """
    for l in h_f:
       print l

    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5"
    for l in c_f:
      print l
      """



  #saving data to pxi file
  def js_cc_file_to_dir_save(self, _outdir):
    print "cc", self.c_file.name
#    f = open(os.path.join(_outdir, self.pxi["f_name"]), 'w')
    """
    lst = self.pxi["head"]
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    """


  def js_h_file_to_dir_save(self, _outdir):
    print "h", self.h_file.name

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

    lines.append("} // end_class\n") # close class

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
        self.pxi = {"f_name": "", "head" : [], "ev" : [], "funcs_parsed" : []}
        self.pxd = {"f_name": "", "head" : [], "ev" : [], }

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

        self.primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

        self.internal_types = {
                                "void*": ["void*", "object"],
                                "char*": ["char*", "object", "ToString"],
                                "Eo*":  ["Eo*", self.basemodule["name"], "ToObject"],
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
                                #"eo_base_data_free_func" : ["", ""]
                                }

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
         self.pxi["funcs_parsed"] += function_lines
         return

       """
        self.properties.setdefault(kl, {})
        fid = fparams["op_id"]
        prop = None
        if fname[-3:] == "set":
          prop = self.properties[kl].setdefault(fname[:-4], {"set":False, "get":False})
          prop["set"] = "True"

          if "parameters" in fparams:
            for n, c_t, d in fparams["parameters"]:
              if d != "in":
                prop["set"] = "True/False"
        elif fname[-3:] == "get":
          prop = self.properties[kl].setdefault(fname[:-4], {"set":False, "get":False})
          prop["get"] = "True"

        """

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
#                elif fparams["parameters"][i-1][1] == "eo_event_cb":
#                  l = ""
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
     self.pxi["funcs_parsed"] += function_lines


  #generating __init_function
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

    self.pxi["funcs_parsed"] += function_lines


    self.pxi["f_name"] = cl_obj.mod_name + ".pxi"
    self.pxd["f_name"] = cl_obj.mod_name  + ".pxd"

    pattern = "########################################################"
    l = '%s\n##\n## generated from from \"%s\"\n##\n%s'%(pattern, cl_obj.source_file, pattern)
    self.pxi["head"].append(l + '\n')
    self.pxd["head"].append(l + '\n')


    #inserting cimports
    l = "cimport %s"%cl_obj.mod_name
    self.pxi["head"].append(l)
    l = "cimport %s"%cl_obj.basemodule
    self.pxi["head"].append(l + '\n')

    #defining class
    parents = []
    if len(cl_obj.parents) != 0:
       parents = cl_obj.parents

    if cl_obj.kl_id == "EoBase":
       parents = []
       parents.append(self.basemodule["name"])
       l = "from %s import %s"%(self.basemodule["module"], self.basemodule["name"])
       self.pxi["head"].append(l + "\n")

    if "EoBase" in parents:
       l = "from %s import %s"%("eobase", "EoBase")
       self.pxi["head"].append(l + "\n")

    l = "from %s import %s"%(self.basemodule["module"], "pytext_to_utf8")
    self.pxi["head"].append(l + "\n")

    #defining _id function
    if cl_obj.extern_base_id != "":
      l = 'cdef int %s(int sub_id):'%(cl_obj.sub_id_function)
      self.pxi["head"].append(l)
      l = '  return %s.%s + sub_id'%(cl_obj.mod_name, cl_obj.extern_base_id)
      self.pxi["head"].append(l + '\n')

    #defining class
    parents = ','.join(parents)
    l = 'class %s(%s):'%(cl_obj.kl_id, parents)

    self.pxi["head"].append(l)

    #inserting cimports
    l = "from %s cimport *"%(cl_obj.basemodule)
    self.pxd["head"].append(l + '\n')

    #inserting externs from H
    l = "cdef extern from \"%s\":"%(cl_obj.includes[0])
    self.pxd["head"].append(l + '\n')


    if cl_obj.extern_base_id != "":
       l = '  %s %s'%("Eo_Op", cl_obj.extern_base_id)
       self.pxd["head"].append(l + '\n')

    enum_lines = []
    enum_lines.append("  ctypedef enum:")
    for v in cl_obj.op_ids:
      #inserting extern enums from H into temp list
      if len(enum_lines) > 1 :
        enum_lines[-1] = enum_lines[-1] + ','
      enum_lines.append('    ' + v)

    if len(enum_lines) > 1:
        for l in enum_lines:
            self.pxd["head"].append(l)
        self.pxd["head"].append('\n')

    for v in cl_obj.extern_funcs:
        l = '  %s %s'%(v[1], v[0])
        self.pxd["head"].append(l)


  #generating event defenitions
  def visit_Ev(self, _o):
    #defining event globals
    v = _o.ev_id
    pos = v.find("EV_")
    if pos == -1:
      return
    name = v[pos + 3:]
    l = "  %s = <long>%s.%s"%(name, _o.cl_obj.mod_name, v)
    self.pxi["ev"].append(l)
    l = '  %s %s'%("Eo_Event_Description *", v)
    self.pxd["ev"].append(l)


  #saving data to pxi file
  def pxi_file_to_dir_save(self, _outdir):
    f = open(os.path.join(_outdir, self.pxi["f_name"]), 'w')

    lst = self.pxi["head"]
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxi["ev"]
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxi["funcs_parsed"]
    for l in lst:
       f.write('  ' + l + '\n')
    f.write("\n")
    f.close()


  #saving data to pxd file
  def pxd_file_to_dir_save(self, _outdir):

    f = open(os.path.join(_outdir, self.pxd["f_name"]), 'w')
    lst = self.pxd["head"]
    for l in lst:
       f.write(l+'\n')
    f.write("\n")

    lst = self.pxd["ev"]
    for l in lst:
       f.write(l+'\n')
    f.write("\n")
    f.close()



class VAcceptor(object):
  def accept(self, v):
    if not O_TYPE_CHECK(v, Visitor):
      return None
    v.visit(self)

#class to save function data
class Func(VAcceptor):
   def __init__(self, _name, _op_id, _c_macro, _parameters, _prop_type, _cl_obj):
     self.name = _name
     self.op_id = _op_id
     self.c_macro = _c_macro
     self.parameters = _parameters
     self.cl_obj = _cl_obj
     self.prop_type = _prop_type

#class to save init function data
class Init(VAcceptor):
   def __init__(self, _cl_obj):
     self.cl_obj = _cl_obj

#class to save event data
class Ev(VAcceptor):
   def __init__(self, _ev_id, _cl_obj):
     self.ev_id = _ev_id
     self.cl_obj = _cl_obj

#  class to keep all data about class
#  (instead of nested dictionary in parser class)
class Mod(object):
   def __init__(self):
     self.kl_id = ""
     self.c_name = ""
     self.macro = ""
     self.eo_type = ""
     self.get_function = ""
     self.instantiateable = False
     self.includes = None
     self.functions = []
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

   def resolve(self):
     for n, o in self.functions.items():
       o.accept(self.V)


class XMLparser(object):
    def __init__(self):

        self.cl_data = {}
        self.cl_incl = {}
        self.objects = {}
        self.objects_incl = {}

        self.primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

        self.internal_types = {
                                "void*": ["void*", "object", "ToObject"],#FIXME
                                "char*": ["char*", "object", "ToString"],
                                "Eo*":  ["Eo*", "EoDefault", "ToObject"],
                                "short" : ["int", "int", "ToInt32"],
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
                                "Eo_Event_Cb":["Eo_Event_Cb","object", "ToNumber"],
                                "eo_base_data_free_func" : ["", ""]
                                }
        self.js_types = { "ToBoolean" : "Boolean",
                          "ToString" : "String",
                          "ToUint32" : "Number",
                          "ToInt32" : "Number",
                          "ToNumber" : "Number",
                          "ToObject" : "Local <Object>"
                          }

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

        if name == "method":
            self.current_func = attrs["name"]
            self.functions.setdefault(self.current_func, {"op_id":attrs["op_id"], "c_macro":attrs["c_macro"], "parameters":[]})

        elif name == "parameter":
            func_att = self.functions[self.current_func]
            #par_att = func_att.setdefault('parameters', [])
            par_att = func_att["parameters"]
            name = attrs["name"]
            if name in self.python_reserved:
              name += "__"
            par_att.append((name, attrs["c_typename"], attrs["direction"], attrs["primary_type"]))

        elif name == "include":
            self.includes.append(attrs["name"])

        elif name == "class":
            self.class_data = attrs
            self.class_data["base_id"] = ""

        elif name == "sub_id":
            self.op_ids.append(attrs["name"])

        elif name == "event":
            self.ev_ids.append(attrs["name"])

        elif name == "base_id":
            self.class_data["base_id"] = attrs["name"]

        elif name == "extern_function":
            self.extern_funcs.append((attrs["name"], attrs["typename"]))

        else:
            pass


    def cast(self, _in):
      t = _in

      for k in self.primary_types:
        if t.find(k) != -1:
          t = t.replace(k, self.primary_types[k])
      return t


    #main XML parsing function
    #parses all XML, initializes field of class structure
    def parse(self, fName):
        self.source_file = fName
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element_handler
        p.ParseFile(open(fName, 'r'))

        mod_name = normalize_names([self.class_data[const.C_NAME]])[0].lower()
        #defining _id function
        if self.class_data["base_id"] != "":
          self.class_data["sub_id_function"] = '%s_sub_id'%(mod_name)
        else:
          self.class_data["sub_id_function"] = ""

        parent_list = []
        parent_list.append(self.class_data["parent"])
        parent_list += self.class_data["extensions"].split(",")

        kl_id = self.class_data["c_name"]
        self.cl_data[kl_id] = \
           {
              const.C_NAME : self.class_data["c_name"],
              const.MACRO : self.class_data["macro"],
              const.TYPE : self.class_data["type"],
              const.GET_FUNCTION : self.class_data["get_function"],
              "instantiateable": self.class_data["instantiateable"],
              "includes" : self.includes,
              "functions" : self.functions,
              const.MODULE : mod_name,
              "basemodule" : "eodefault",
              "op_ids" : self.op_ids,
              "ev_ids" : self.ev_ids,
              "extern_base_id" : self.class_data["base_id"],
              "extern_funcs" : self.extern_funcs,
              "sub_id_function" : self.class_data["sub_id_function"],
              "source_file" : self.source_file,
              const.PARENTS : parent_list
            }

        mod_o = Mod()
        mod_o.kl_id = kl_id
        mod_o.c_name = self.class_data["c_name"]
        mod_o.macro = self.class_data["macro"]
        mod_o.eo_type = self.class_data["type"]
        mod_o.get_function = self.class_data["get_function"]
        mod_o.instantiateable = self.class_data["instantiateable"]
        mod_o.includes = self.includes
        mod_o.functions = {}
        mod_o.mod_name = mod_name
        mod_o.basemodule = "eodefault"
        mod_o.op_ids = self.op_ids
        mod_o.ev_ids = self.ev_ids
        mod_o.extern_base_id = self.class_data["base_id"]
        mod_o.extern_funcs = self.extern_funcs
        mod_o.sub_id_function = self.class_data["sub_id_function"]
        mod_o.source_file = self.source_file
        mod_o.parents = parent_list
#        mod_o.V = PyVisitor()


        for i in self.functions:
          T = ""
          if i[-4:] == "_set":
            if i[:-4]+"_get" in self.functions:
              T = const.SET_GET
            else:
              T = const.SET_ONLY
          elif i[-4:] == "_get":
            if i[:-4]+"_set" in self.functions:
              T = const.SET_GET
            else:
              T = const.GET_ONLY
          else:
            T = const.METHOD
          mod_o.functions[i] = Func(i, self.functions[i]["op_id"], self.functions[i]["c_macro"], self.functions[i]["parameters"], T, mod_o)



        for i in self.ev_ids:
          mod_o.functions[i] = Ev(i, mod_o)

        mod_o.functions["__init__"] = Init(mod_o)

        self.objects[kl_id] = mod_o
        del mod_o

        self.functions = {}
        self.includes = []
        self.op_ids = []
        self.ev_ids = []
        self.extern_funcs = []


    def js_parse(self, kl_id, outdir):

       funcs = self.cl_data[kl_id]["functions"]

       self.cl_data[kl_id]["js_cpp_h"] = os.path.join(outdir, "_" + self.cl_data[kl_id]["module"]  + ".h")
       self.cl_data[kl_id]["js_cpp_cc"] = os.path.join(outdir, "_" + self.cl_data[kl_id]["module"]  + ".cc")

       self.cl_data[kl_id]["properties"] = []
       self.cl_data[kl_id]["methods"] = []
       self.cl_data[kl_id]["properties_set"] = []
       self.cl_data[kl_id]["properties_get"] = []

       eo_base_ops = ["EO_BASE_SUB_ID_EVENT_FREEZE", "EO_BASE_SUB_ID_EVENT_FREEZE_GET", "EO_BASE_SUB_ID_EVENT_THAW", "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE", "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW"]

       properties = []
       properties_set = []
       properties_get = []
       methods = []
       prop_tmp = []

       for l in funcs:
         if kl_id == "Eo Base":
           if funcs[l]["op_id"] not in eo_base_ops:
             continue
         i = l.rfind("_")
         if i != -1:
           s = l[i + 1:]
           if s != "set" and s != "get":
             methods.append(l)
           else:
             prop_tmp.append(l)
         else:
           methods.append(l)

       for key in prop_tmp:
         l = key[:-4]

         if l + "_set" in prop_tmp and l + "_get" in prop_tmp and l not in methods:
            properties.append(l)
         elif l + "_set" in prop_tmp and l not in methods:
            properties_set.append(l)
         elif l + "_get" in prop_tmp and l not in methods:
            properties_get.append(l)
         else:
            methods.append(key)

       self.cl_data[kl_id]["properties"] = list(set(properties))
       self.cl_data[kl_id]["methods"] = methods
       self.cl_data[kl_id]["properties_set"] = properties_set
       self.cl_data[kl_id]["properties_get"] = properties_get


    def js_obj_parse(self, outdir):
      for n, o in self.objects.items():
         o.js_h_file = os.path.join(outdir, "_" + o.mod_name + ".h")
         o.js_cc_file = os.path.join(outdir, "_" + o.mod_name + ".cc")



    def check_parents(self):
       list_of_parents = []
       for k in self.cl_data:
         self.cl_data[k]["parents"] = filter(len, self.cl_data[k]["parents"])
         list_of_parents += self.cl_data[k]["parents"]

       list_of_parents = list(set(list_of_parents))

       parents_to_find = filter(lambda l: True if l not in self.cl_data else False, list_of_parents)

       return parents_to_find


    #parents
    def check_parents2(self):
       list_of_parents = []

       for n, o in self.objects.items():
         o.parents = filter(len, o.parents)
         list_of_parents += o.parents

       list_of_parents = list(set(list_of_parents))

       parents_to_find = filter(lambda l: True if l not in self.objects else False, list_of_parents)

       return parents_to_find

    def build_js_modules(self, module_name, pkg):
       cl_data_tmp = {}

       for k in self.cl_data:
         self.cl_data[k]["name"] =  normalize_names([self.cl_data[k]["c_name"]])[0]
         self.cl_data[k]["parents"] = normalize_names(self.cl_data[k]["parents"])
         cl_data_tmp[self.cl_data[k]["name"]] = self.cl_data[k]

     #    self.cl_data[k]["js_cpp_h"] = os.path.join(self.outdir, "_" + self.cl_data[k]["module"]  + ".h")
     #    self.cl_data[k]["js_cpp_cc"] = os.path.join(self.outdir, "_" + self.cl_data[k]["module"]  + ".cc")


       self.cl_data = cl_data_tmp
       del cl_data_tmp

       if module_name == "eobase":
         if "EoBase" in self.cl_data:
           cl_data_tmp = dict(self.cl_data)
           self.cl_data = {}
           self.cl_data["EoBase"] = cl_data_tmp["EoBase"]
           del cl_data_tmp
         else:
           print "ERROR: source files for module \"EoBase\" not found"
           exit(1)
       else:
          if "EoBase" in self.cl_data:
             self.cl_data.pop("EoBase")
             print("Warning: EoBase module was removed from building tree")

       for k in self.cl_data:
         self.build_cpp_class(k)

    def build_cpp_class(self, kl_id):

        ll = []
        c_f = []
        kl_dt = self.cl_data[kl_id]

        lst = self.get_parents(kl_id)
        lst.insert(0, kl_id)

        methods = []
        properties = []
        event_ids = []
        for p in lst:
          if p in self.cl_data:
            parent_data = self.cl_data[p]
          else:
            parent_data = self.cl_incl[p]
          methods += parent_data["methods"]
          properties += parent_data["properties"]
          properties += parent_data["properties_set"]
          properties += parent_data["properties_get"]
          event_ids += parent_data["ev_ids"]

#        kl_dt[".h"] = os.path.join(self.outdir, "_" + kl_dt["module"]  + ".h")
#        kl_dt[".cc"] = os.path.join(self.outdir, "_" + kl_dt["module"]  + ".cc")

        c_f.append("/**\n * generated from \"%s\"\n */\n"%(kl_dt["source_file"]))
        c_f.append("#include \"%s\"\n"%(os.path.split(kl_dt["js_cpp_h"])[1] ))
        c_f.append("namespace elm {\n\n")
        c_f.append("using namespace v8;\n\n")

        for p in kl_dt["properties"]:
           c_f.append("EO_GENERATE_PROPERTY_CALLBACKS(%s, %s);\n"%(kl_id, p))
        c_f.append("\n")

        for p in kl_dt["properties_set"]:
           c_f.append("EO_GENERATE_PROPERTY_SET_CALLBACK(%s, %s);\n"%(kl_id, p))
           c_f.append("EO_GENERATE_PROPERTY_GET_EMPTY_CALLBACK(%s, %s);\n"%(kl_id, p))
        c_f.append("\n")

        for p in kl_dt["properties_get"]:
           c_f.append("EO_GENERATE_PROPERTY_SET_EMPTY_CALLBACK(%s, %s);\n"%(kl_id, p))
           c_f.append("EO_GENERATE_PROPERTY_GET_CALLBACK(%s, %s);\n"%(kl_id, p))
        c_f.append("\n")

        for m in kl_dt["methods"]:
#FIXME
           if m in ["event_global_freeze", "event_global_thaw"]:
             continue
           c_f.append("EO_GENERATE_METHOD_CALLBACKS(%s, %s);\n"%(kl_id, m))
        c_f.append("\n")

        for e in kl_dt["ev_ids"]:
           c_f.append("EO_GENERATE_PROPERTY_CALLBACKS(%s, %s);\n"%(kl_id, e.lower()))
        c_f.append("\n")

        #creating .h file
        f = open (kl_dt["js_cpp_h"], 'w')
        ll.append("/**\n * generated from \"%s\"\n */\n"%(kl_dt["source_file"]))

        ll.append("#ifndef %s\n"%( ("_JS_"+kl_dt["module"]+"_h_").upper() ))
        ll.append("#define %s\n"%( ("_JS_"+kl_dt["module"]+"_h_").upper() ))
        ll.append("\n")
        ll.append("#include \"elm.h\" //macro defines, common functions\n")
        ll.append("#include \"CElmObject.h\" //base object\n")
        ll.append("#include \"%s\" //eo-class include file\n"%(kl_dt["includes"][0]))


        for l in kl_dt["parents"]:
          if l in self.cl_data:
            parent_data = self.cl_data[l]
          else:
            parent_data = self.cl_incl[l]

          ll.append("#include \"%s\" //include generated js-wrapping classes\n"%( os.path.split(parent_data["js_cpp_h"])[1]))

        ll.append("\n")
        ll.append("namespace elm { //namespace should have the same meaning as module for python\n")
        ll.append("\n")

        ll.append("using namespace v8;\n")
        ll.append("\n")

        lst = ["public virtual CElmObject"]
        for l in kl_dt["parents"]:
           lst.append("public virtual %s"%(l))

        inherit = ", ".join(lst)
        ll.append("class %s : %s {\n"%(kl_id, inherit))

        priv = []
        prot = []
        publ = []
        init_f = []
        tmpl = ""

        if kl_dt["type"] == const.CLASS_TYPE_REGULAR:
          priv.append("   static Persistent<FunctionTemplate> tmpl;\n")
          priv.append("\n")

          prot.append("   %s(Local<Object> _jsObject, CElmObject *parent);\n"%(kl_id))

          c_f.append("%s::%s(Local<Object> _jsObject, CElmObject *parent)\n"%(kl_id, kl_id))
          c_f.append(" : CElmObject(_jsObject, eo_add(%s , parent ? parent->GetEo() : NULL))\n"%(kl_dt["macro"]))
          c_f.append("{\n   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));\n}\n")

          prot.append("   static Handle<FunctionTemplate> GetTemplate();\n")
          prot.append("\n")

          publ.append("   static void Initialize(Handle<Object> target);\n")


          init_f.append("void %s::Initialize(Handle<Object> target)\n"%kl_id)
          init_f.append("{\n")
          init_f.append("   target->Set(String::NewSymbol(\"%s\") , GetTemplate()->GetFunction());\n"%kl_id)
          for m in methods:
#FIXME
            if m in ["event_global_freeze", "event_global_thaw"]:
              init_f.append("EO_REGISTER_STATIC_METHOD(%s);\n"% m)
          init_f.append("}\n")


          publ.append("   virtual void DidRealiseElement(Local<Value> obj);\n")

          c_f.append("void %s::DidRealiseElement(Local<Value> obj)\n {\n\
                      (void) obj;\n\
                      }\n"%kl_id)

          publ.append("   friend Handle<Value> CElmObject::New<%s>(const Arguments& args);\n"%(kl_id))
          publ.append("\n")

#generating list of all parents, to get all properties and methods
          """
          lst = self.get_parents(kl_id)
          lst.insert(0, kl_id)

          methods = []
          properties = []
          event_ids = []
          for p in lst:
            if p in self.cl_data:
              parent_data = self.cl_data[p]
            else:
              parent_data = self.cl_incl[p]
            methods += parent_data["methods"]
            properties += parent_data["properties"]
            properties += parent_data["properties_set"]
            properties += parent_data["properties_get"]
            event_ids += parent_data["ev_ids"]

          print kl_id, properties
          print kl_id, methods
          """

          l_tmp = []
          l_tmp.append("%s"%kl_id)
          l_tmp.append("%s"%"PROPERTY(elements)")
          for p in properties:
            l_tmp.append("   PROPERTY(%s)"%p)
          for e in event_ids:
            l_tmp.append("   PROPERTY(%s)"%e.lower())
          for m in methods:
             #FIXME
            if m in ["event_global_freeze", "event_global_thaw"]:
               continue
            l_tmp.append("   METHOD(%s)"%m)
          tmpl = ",\n".join(l_tmp)
          tmpl = "GENERATE_TEMPLATE(%s);"%tmpl
          c_f.append("\n")
          del l_tmp
        #  del methods
          del properties

        if len(kl_dt["ev_ids"]):
          prot.append("   struct {\n")
          for e in kl_dt["ev_ids"]:
             ev = e.lower()
             prot.append("      Persistent<Value> _event_%s;\n"%(ev))
          prot.append("   } cb;\n")
          prot.append("\n")


        ll.append("private:\n")
        #generating constructors and destructor
        ll += priv

        ll.append("protected:\n")
        #generating constructors and destructor
        ll.append("   %s();\n"%(kl_id))
        c_f.append("%s::%s(){}\n\n"%(kl_id, kl_id));
        c_f.append("%s::~%s(){} //need to add destruction of cb variables\n\n"%(kl_id, kl_id));
        ll += prot
        ll.append("   virtual ~%s();\n"%(kl_id))

        ll.append("\n")
        ll.append("public:\n")
        ll += publ


        for p in kl_dt["properties"]:


           params_tmp = []
           add_this_func = True
           for i, (n, c_t, d, p_t) in enumerate(kl_dt["functions"][p+"_get"]["parameters"]):
             if d != "out":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %s"%(p + "_get", n, d)
               print "Property \"%s\" will not be defined"%(p + "_get")
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
               print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, p + "_get")
               add_this_func = False
               break

           if not add_this_func:
             continue

           #generating getter header  in class (h file)
           ll.append("   Handle<Value> %s_get() const;\n"%(p))

          #generating getter in cc file
           c_f.append("Handle<Value> %s::%s_get() const\n"%(kl_id, p))
           c_f.append("{\n")
           c_f.append("   HandleScope scope;\n")

           pass_params = []
           ret_params = []
           for (c_t, n, d, c_t_internal, js_type) in params_tmp:

             c_f.append("   %s %s;\n"%(c_t_internal, n))
             pass_params.append('&' + n)

             js_type = self.js_types[js_type]
             ret_params.append((n, js_type))

           c_f.append("   eo_do(eobj, %s(%s));\n"%(kl_dt["functions"][p+"_get"]["c_macro"], ", ".join(pass_params)))

           if len(ret_params) == 1:
             for par, t in ret_params:
               c_f.append("   return scope.Close(%s::New(%s));//need to put proper values\n"%(t, par))

           elif len(ret_params) > 1:
             c_f.append("   Local<Object> obj__ = Object::New();\n")
             for par, t in ret_params:
                c_f.append("   obj__->Set(String::NewSymbol(\"%s\"), %s::New(%s));\n"%(par, t, par))
             c_f.append("   return scope.Close(obj__);//need to put proper values\n")
           else:
             c_f.append("   return Undefined();\n")

           c_f.append("}\n\n")



           params_tmp = []
           add_this_func = True
           for i, (n, c_t, d, p_t) in enumerate(kl_dt["functions"][p+"_set"]["parameters"]):
             if d != "in":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %s"%(p, n, d)
               print "Property \"%s\" will not be defined"%(p + "_set")
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
               print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, p + "_set")
               add_this_func = False
               break

           if not add_this_func:
             continue

           #generating setter header in class (h file)
           ll.append("   void %s_set(Handle<Value> val);\n"%(p))

           #generating setter in cc file
           c_f.append("void %s::%s_set(Handle<Value> val)\n"%(kl_id, p))
           c_f.append("{\n")

           pass_params = []
           add_end_func = []
           if len(params_tmp) > 1:
             c_f.append("   Local<Object> __o = val->ToObject();\n")

             for (c_t, n, d, c_t_internal, js_type) in params_tmp:

               c_f.append("   %s %s;\n"%(c_t_internal, n))
               if js_type == "ToString":
                  c_f.append("   %s = strdup(*String::Utf8Value(__o->Get(String::NewSymbol(\"%s\"))->%s()));\n"%(n, n, js_type))
               else:
                 c_f.append("   %s = __o->Get(String::NewSymbol(\"%s\"))->%s()->Value();\n"%(n, n, js_type))

               if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                 pass_params.append('&' + n)
               else:
                 pass_params.append(n)

           elif len(params_tmp) == 1:
             for (c_t, n, d, c_t_internal, js_type) in params_tmp:

               c_f.append("   %s %s;\n"%(c_t_internal, n))
               if js_type == "ToString":
                 c_f.append("   %s = strdup(*String::Utf8Value(val->%s()));\n"%(n, js_type))
                 add_end_func.append("  free(%s);"%n)
               else:
                 c_f.append("   %s = val->%s()->Value();\n"%(n, js_type))

               if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                 pass_params.append('&' + n)
               else:
                 pass_params.append(n)

           c_f.append("   eo_do(eobj, %s(%s));\n"%(kl_dt["functions"][p + "_set"]["c_macro"], ", ".join(pass_params)))
           c_f += add_end_func
           add_end_func = []
           c_f.append("}\n")
           c_f.append("\n")

        ll.append("\n")



###############################################################################
###############################################################################

        for p in kl_dt["properties_set"]:
           #generating headers of  setter/getter in class (h file)

           params_tmp = []
           add_this_func = True
           for i, (n, c_t, d, p_t) in enumerate(kl_dt["functions"][p+"_set"]["parameters"]):
             if d != "in":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %"%(p, n, d)
               print "Property \"%s\" will not be defined"%(p + "_set")
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
               print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, p + "_set")
               add_this_func = False
               break

           if not add_this_func:
             continue

           ll.append("   void %s_set(Handle<Value> val);\n"%(p))

          #generating setter/getter in cc file
           c_f.append("void %s::%s_set(Handle<Value> val)\n"%(kl_id, p))
           c_f.append("{\n")

           pass_params = []
           add_end_func = []
           if len(params_tmp) > 1:
             c_f.append("   Local<Object> __o = val->ToObject();\n")

             for (c_t, n, d, c_t_internal, js_type) in params_tmp:
               c_f.append("   %s %s;\n"%(c_t_internal, n))
               #FIXME: case when we are working with EO
               if js_type == "ToString":
                 c_f.append("   %s = strdup(*String::Utf8Value(__o->Get(String::NewSymbol(\"%s\"))->%s()));\n"%(n, n, js_type))
                 add_end_func.append("   free(%s);"%n)
               else:
                 c_f.append("   %s = __o->Get(String::NewSymbol(\"%s\"))->%s()->Value();\n"%(n, n, js_type))

               if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                 pass_params.append('&' + n)
               else:
                 pass_params.append(n)


           elif len(params_tmp) == 1:
             for (c_t, n, d, c_t_internal, js_type) in params_tmp:

               c_f.append("   %s %s;\n"%(c_t_internal, n))
               #FIXME: case for EO
               if js_type == "ToString":
                 c_f.append("   %s = strdup(*String::Utf8Value(val->%s()));\n"%(n, js_type))
                 add_end_func.append("   free(%s);"%n)
               else:
                 c_f.append("   %s = val->%s()->Value();\n"%(n, js_type))

               if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                 pass_params.append('&' + n)
               else:
                 pass_params.append(n)

           c_f.append("   eo_do(eobj, %s(%s));\n"%(kl_dt["functions"][p + "_set"]["c_macro"], ", ".join(pass_params)))
           c_f += add_end_func
           add_end_func = []
           c_f.append("}\n")
           c_f.append("\n")

        ll.append("\n")

###############################################################################
###############################################################################

        for p in kl_dt["properties_get"]:

           params_tmp = []
           add_this_func = True
           for i, (n, c_t, d, p_t) in enumerate(kl_dt["functions"][p+"_get"]["parameters"]):
             if d != "out":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %s"%(p + "_get", n, d)
               print "Property \"%s\" will not be defined"%(p + "_get")
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
               print "Warning: type: \"%s\" wasn't found in self.internal_types. Function \"%s\" will not be defined"%(c_t_tmp, p + "_get")
               add_this_func = False
               break

           if not add_this_func:
             continue


           #generating headers of  setter/getter in class (h file)
           ll.append("   Handle<Value> %s_get() const;\n"%(p))

          #generating setter/getter in cc file
           c_f.append("Handle<Value> %s::%s_get() const\n"%(kl_id, p))
           c_f.append("{\n")
           c_f.append("   HandleScope scope;\n")

           pass_params = []
           ret_params = []
#           for i, (n, c_t, d) in enumerate(kl_dt["functions"][p+"_get"]["parameters"]):
           for (c_t, n, d, c_t_internal, js_type) in params_tmp:
             c_f.append("   %s %s;\n"%(c_t_internal, n))
             pass_params.append('&' + n)

             js_type = self.js_types[js_type]
             ret_params.append((n, js_type))

           c_f.append("   eo_do(eobj, %s(%s));\n"%(kl_dt["functions"][p+"_get"]["c_macro"], ", ".join(pass_params)))


           if len(ret_params) == 1:
             for par, t in ret_params:
#FIXME: case then we work with EO
               c_f.append("   return scope.Close(%s::New(%s));//need to put proper values\n"%(t, par))

           elif len(ret_params) > 1:
             c_f.append("   Local<Object> obj__ = Object::New();\n")
             for par, t in ret_params:
                c_f.append("   obj__->Set(String::NewSymbol(\"%s\"), %s::New(%s));\n"%(par, t, par))
             c_f.append("   return scope.Close(obj__);//need to put proper values\n")
           else:
             c_f.append("   return Undefined();\n")

           c_f.append("}\n")
           c_f.append("\n")

        ll.append("\n")


###############################################################################
###############################################################################

        for e in kl_dt["ev_ids"]:
           #generating headers of events in class (h file)
           ev = e.lower()
           ev_prefix = "_event_" + ev
           ll.append("   Handle<Value> %s_get() const;\n"%(ev))
           ll.append("   void %s_set(Handle<Value> val);\n"%(ev))
           ll.append("   void %s(void *event_info);\n"%(ev))
           ll.append("   static Eina_Bool %s_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);\n"%(ev))

           #event function
           c_f.append("void %s::%s(void *event_info) //parse of event_info need to be added \n"%(kl_id, ev))
           c_f.append("{\n")
           c_f.append("  Handle<Function> callback(Function::Cast(*cb.%s));\n"%ev_prefix)
           c_f.append("  Handle<Value> args[1] = {jsObject};\n")
           c_f.append("  callback->Call(jsObject, 1, args);\n")
           c_f.append("}\n")
           c_f.append("\n")

           #event function wrapper
           c_f.append("Eina_Bool %s::%s_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info)\n"%(kl_id, ev))
           c_f.append("{\n\
                           HandleScope scope;\n\
                           static_cast<%s*>(data)->%s(event_info);\n\
                           return EINA_TRUE;\n\
                           (void) obj;\n\
                           (void) desc;\n\
                       }\n"%(kl_id, ev))
           c_f.append("\n")

           #event function get
           c_f.append("Handle<Value> %s::%s_get() const\n"%(kl_id, ev))
           c_f.append("{\n\
                           return cb.%s;\n\
                       }\n"%ev_prefix)
           c_f.append("\n")

           #event function set
           c_f.append("void %s::%s_set(Handle<Value> val)\n"%(kl_id, ev))
           c_f.append("{\n")
           c_f.append("  if (!val->IsFunction())\n\
                           return;\n")
           c_f.append("  if (!cb.%s.IsEmpty())\n\
                         {\n\
                            cb.%s.Dispose();\n\
                            cb.%s.Clear();\n\
                            eo_do(eobj, eo_event_callback_del(%s, %s_wrapper, this));\n\
                         }\n"%(ev_prefix, ev_prefix, ev_prefix, e, ev))
           c_f.append("  cb.%s = Persistent<Value>::New(val);\n\
                         eo_do(eobj, eo_event_callback_add(%s, %s_wrapper, this));\n"%(ev_prefix, e, ev))
           c_f.append("}\n")
           c_f.append("\n")
        ll.append("\n")

        if kl_id != "EoBase":
           for m in ["event_global_freeze", "event_global_thaw"]:
             c_f.append("static Handle<Value> %s(const Arguments& args)\n"%m)
             c_f.append("{\n")
             c_f.append("  eo_class_do(%s, eo_%s());\n"%(kl_dt["macro"],m))
             c_f.append("  return Undefined();\n")
             c_f.append("}\n")
             continue

#####################################################################
#####################################################################


        for m in kl_dt["methods"]:
           if m in ["event_global_freeze", "event_global_thaw"]:
             c_f.append("Handle<Value> %s(const Arguments& args)\n"%m)
             c_f.append("{\n")
             c_f.append("  eo_class_do(%s, eo_%s());\n"%(kl_dt["macro"],m))
             c_f.append("  return Undefined();\n")
             c_f.append("}\n")
             continue

           ll.append("   Handle<Value> %s(const Arguments&);\n"%(m))

           c_f.append("Handle<Value> %s::%s(const Arguments& args)\n"%(kl_id, m))
           c_f.append("{\n")
           c_f.append("   HandleScope scope;\n")

           pass_params = []
           ret_params = []
           in_param_counter = 0
           for i, (n, c_t, d, p_t) in enumerate(kl_dt["functions"][m]["parameters"]):
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
               c_f.append("   Local<Value> _%s = args[%d];\n"%(n, in_param_counter))
               in_param_counter += 1
               c_f.append("   %s %s;\n"%(c_t_internal, n))

               if js_type == "ToString":
                 c_f.append("  %s = strdup(*String::Utf8Value(_%s->%s()));\n"%(n, n, js_type))
               elif js_type == "ToObject":
                 c_f.append("   %s = static_cast<CElmObject*>(_%s->ToObject()->GetPointerFromInternalField(0))->GetEo();\n"%(n, n))
               else:
                 c_f.append("   %s = _%s->%s()->Value();\n"%(n, n, js_type))
               if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                 pass_params.append('&' + n)
               else:
                 pass_params.append(n)
             elif d == "out":
               c_f.append("   %s %s;\n"%(c_t_internal, n))
               pass_params.append('&' + n)

               js_type = self.js_types[js_type]
               ret_params.append((n, js_type))

             elif d == "in,out":
               c_f.append("   Local<Value> _%s = args[%d];\n"%(n, in_param_counter))
               in_param_counter += 1
               c_f.append("   %s %s;\n"%(c_t_internal, n))

               if js_type == "ToString":
                 c_f.append("  %s = strdup(*String::Utf8Value(_%s->%s()));\n"%(n, n, js_type))
               elif js_type == "ToObject":
                 c_f.append("   %s = static_cast<CElmObject*>(_%s->ToObject()->GetPointerFromInternalField(0))->GetEo();\n"%(n, n))
               else:
                 c_f.append("   %s = _%s->%s()->Value();\n"%(n, n, js_type))

               pass_params.append('&' + n)
               js_type = self.js_types[js_type]
               ret_params.append((n, js_type))

           c_f.append("   eo_do(eobj, %s(%s));\n"%(kl_dt["functions"][m]["c_macro"], ", ".join(pass_params)))

           if len(ret_params) == 1:
             for par, t in ret_params:
#FIXME: case then we work with EO
               c_f.append("   return scope.Close(%s::New(%s));//need to put proper values\n"%(t, par))
           elif len(ret_params) > 1:
             c_f.append("   Local<Object> obj__ = Object::New();\n")
             for p, t in ret_params:
                c_f.append("   obj__->Set(String::NewSymbol(\"%s\"), %s::New(%s));\n"%(p, t, p))
             c_f.append("   return scope.Close(obj__); //need to put proper values\n")
           else:
             c_f.append("   return Undefined();\n")

           c_f.append("}\n")
           c_f.append("\n")
        ll.append("\n")


        ll.append("}; //end class\n");
        ll.append("\n")

        ll.append("/* properties callbacks */\n");
        for p in kl_dt["properties"] + kl_dt["properties_set"] + kl_dt["properties_get"]:
           ll.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(p))
           ll.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(p))


        ll.append("\n")
        ll.append("/* properties(events) callbacks */\n");
        for e in kl_dt["ev_ids"]:
           ev = e.lower()
           ll.append("   Handle<Value> Callback_%s_get(Local<String>, const AccessorInfo &info);\n"%(ev))
           ll.append("   void Callback_%s_set(Local<String>, Local<Value> val, const AccessorInfo &info);\n"%(ev))

        ll.append("\n")
        ll.append("/* methods callbacks */\n");
        for p in kl_dt["methods"]:
           ll.append("   Handle<Value> Callback_%s(const Arguments&);\n"%(p))


        ll.append("\n")
        ll.append("} //end namespace elm\n")

        c_f.append("%s\n"%tmpl)
        c_f += init_f
        c_f.append("} //end namespace elm\n")
        ll.append("\n")
        ll.append("#endif\n")

        for line in ll:
          f.write(line)

        f.close()

        f = open (kl_dt["js_cpp_cc"], 'w')
        for line in c_f:
          f.write(line)
        f.close()


    def print_data(self):
      for klass in self.cl_data:
        print ""
        print klass
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


#FIXME move this function to eo_py_gen
    def reorder_parents2(self, p_list):
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


    def get_parents(self, kl):
      prnts = self.objects[kl].parents
      l = []
      for p in prnts:
        if p != "EoBase":
          l = l + self.get_parents(p)

      l = list(set(l + prnts))
      return l


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
        o.parents = self.reorder_parents2(o.parents)

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
        lines.append("include \"%s\""%self.objects[k].V.pxi["f_name"])
        #FIXME adding filenames of include modules?

      f = open (os.path.join(outdir, module_name + ".pyx"), 'w')
      for l in lines:
        f.write(l + "\n")
      f.close()


    def js_code_generate(self, outdir):

      #reodering parents and generating source code
      for n, o in self.objects.items():

        o.V = JsVisitor()
        o.resolve()

      #saving files
      for n, o in self.objects.items():
        o.V.js_cc_file_to_dir_save(outdir)
        o.V.js_h_file_to_dir_save(outdir)

