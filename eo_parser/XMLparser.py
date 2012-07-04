import xml.parsers.expat, os, shutil
from helper import normalize_names




def O_TYPE_CHECK(o, class_type):
  if not isinstance(o, class_type):
  #  if type(o) is not class_type:
     print "Warning: object: %s is not of class: %s"%(o, class_type.__name__)
     return False
  else:
     return True

def class_name_get(_o):
  return _o.__class__.__name__

class Visitor(object):
  def visit(self, _p):
    method_name = "visit_" + class_name_get(_p)
    method = getattr(self, method_name, False)
    if callable(method):
      method(_p)
    else:
       print "%s is not callable attribute"%(method_name)


class PyVisitor(Visitor):

  def __init__(self):

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

        self.typedefs = {"Evas_Coord" : "int",
                         "Evas_Angle":"int",
                         "Evas_Font_Size" : "int",
                         "Eina_Bool" : "bool",
                         "Eo_Callback_Priority": "short"}

        self.primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

        self.internal_types = {
                                "void*": ["void*", "object"],
                                "char*": ["char*", "object", "ToString"],
                                "Eo*":  ["Eo*", self.basemodule["name"], "ToObject"],
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



  def cast(self, _in):
    t = _in
    for k in self.typedefs:
      if t.find(k) != -1:
        t = t.replace(k, self.typedefs[k])

    for k in self.primary_types:
      if t.find(k) != -1:
        t = t.replace(k, self.primary_types[k])
    return t

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
         #self.cl_data[kl_id]["methods_parsed"][fname] = function_lines
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
         #self.cl_data[kl_id]["methods_parsed"][fname] = function_lines
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

       for i, (n, c_t, d) in enumerate(_o.parameters):
         c_t_tmp = self.cast(c_t)

         py_type = ""
         c_t_internal = ""

         if c_t_tmp in self.internal_types:
            c_t_internal = self.internal_types[c_t_tmp][0]
            py_type = self.internal_types[c_t_tmp][1]
         else:
            print "Warning: type: \"%s\" wasn't found in self.internal_types. Functon \"%s\" will not be defined"%(c_t_tmp, fname)
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
     l = "def %s(%s):"% (_o.name, ', '.join(in_params))
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
      l = '  return %s.%s + sub_id'%(cl_obj.mod_name,
                                         cl_obj.extern_base_id)
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



class VAcceptor(object):
  def accept(self, v):
    if not O_TYPE_CHECK(v, Visitor):
      return None
    v.visit(self)

class Func(VAcceptor):
   def __init__(self, _name, _op_id, _c_macro, _parameters, _cl_obj):
     self.name = _name
     self.op_id = _op_id
     self.c_macro = _c_macro
     self.parameters = _parameters
     self.cl_obj = _cl_obj

class Init(VAcceptor):
   def __init__(self, _cl_obj):
     self.cl_obj = _cl_obj


class Ev(VAcceptor):
   def __init__(self, _ev_id, _cl_obj):
     self.ev_id = _ev_id
     self.cl_obj = _cl_obj

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

        self.globals = {}
        self.cl_data = {}
        self.cl_incl = {}
        self.V = PyVisitor()
        self.objects = {}
        self.objects_incl = {}

        """
        self.properties = {}
        """

        #internal functions, used in eodefault.pyx


        self.typedefs = {"Evas_Coord" : "int",
                         "Evas_Angle":"int",
                         "Evas_Font_Size" : "int",
                         "Eina_Bool" : "bool",
                         "Eo_Callback_Priority": "short"}

        self.primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

        self.internal_types = {
                                "void*": ["void*", "object"],
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
                          "ToNumber" : "Number"
                          }

        self.string_consts = {"class_type_mixin" : "EO_CLASS_TYPE_MIXIN",
                              "class_type_regular" : "EO_CLASS_TYPE_REGULAR",
                          }
        self.python_reserved = {"pass" }


        self.outdir = ""
        self.source_file = ""
        self.includes = []
        self.ev_ids = []
        self.op_ids = []
        self.extern_funcs = []

        self.class_data = {}
        self.functions = {} #function names with parameters
        self.current_func = ""
        self.methods_parsed = {} #ready function lines
        self.hack_types = ["eo_base_data_free_func"]

        self.globals["extern_base_id"] = ""

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
            par_att.append((name, attrs["c_typename"], attrs["direction"]))

        elif name == "include":
            self.includes.append(attrs["name"])

        elif name == "class":
            self.class_data = attrs

        elif name == "sub_id":
            self.op_ids.append(attrs["name"])

        elif name == "event":
            self.ev_ids.append(attrs["name"])

        elif name == "base_id":
            self.globals["extern_base_id"] = attrs["name"]

        elif name == "extern_function":
            self.extern_funcs.append((attrs["name"], attrs["typename"]))

        else:
            pass


#changing types according to typedefs: Evas_Coord -> int
    def cast(self, _in):
      t = _in
      for k in self.typedefs:
        if t.find(k) != -1:
          t = t.replace(k, self.typedefs[k])

      for k in self.primary_types:
        if t.find(k) != -1:
          t = t.replace(k, self.primary_types[k])
      return t

    def parse_methods(self, kl_id, fname):
        kl_dt = self.cl_data[kl_id]
        fparams = kl_dt["functions"][fname]
        in_params = []
        pass_params =[]
        ret_params = []
        function_lines = []

        if kl_id == "Eo Base":
          if_ret = False
          if fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD":
            function_lines.append("def event_callback_priority_add(self, long _desc, int _priority, object _cb):")
            function_lines.append("  if not callable(_cb):")
            function_lines.append("    raise TypeError(\"func must be callable\")")
            function_lines.append("  cdef Eo_Event_Cb cb = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD), _desc, _priority, cb, <void*>_cb)")
            if_ret = True
          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL":
            function_lines.append("def event_callback_del(self, long _desc, object _func):")
            function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL), _desc, func, <void*>_func)")

            function_lines.append("\n")
            self.cl_data[kl_id]["methods_parsed"][fname] = function_lines
            if_ret = True
          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY":
            function_lines.append("def event_callback_del_lazy(self, long _desc, object _func):")
            function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  cdef void * user_data")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY), _desc, func, &user_data)")
            function_lines.append("  return None if user_data == NULL else <object>user_data")
            if_ret = True

          elif fparams["op_id"] == "EO_BASE_SUB_ID_DATA_SET":
            function_lines.append("def data_set(self, object _key, object _data):")
            function_lines.append("  _key = pytext_to_utf8(_key)")
            function_lines.append("  cdef char* key = <char*> _key")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)")
            if_ret = True

          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE":
            function_lines.append("@staticmethod")
            function_lines.append("def event_global_freeze():")
            function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE))");
            if_ret = True

          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET":
            function_lines.append("@staticmethod")
            function_lines.append("def event_global_freeze_get():")
            function_lines.append("  cdef int fcount");
            function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET), &fcount)");
            function_lines.append("  fcount_ = <object>fcount");
            function_lines.append("  return (fcount_)");

            if_ret = True

          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW":
            function_lines.append("@staticmethod")
            function_lines.append("def event_global_thaw():")
            function_lines.append("  eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_THAW))");
            if_ret = True

          if if_ret:
            function_lines.append("\n")
            self.cl_data[kl_id]["methods_parsed"][fname] = function_lines
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

        if "parameters" in fparams:

          for i, (n, c_t, d) in enumerate(fparams["parameters"]):
            c_t_tmp = self.cast(c_t)

            py_type = ""
            c_t_internal = ""

            if c_t_tmp in self.internal_types:
               c_t_internal = self.internal_types[c_t_tmp][0]
               py_type = self.internal_types[c_t_tmp][1]
            else:
               print "warning: type: \"%s\" wasn't found in self.internal_types. functon \"%s\" will not be defined"%(c_t_tmp, fname)
               return

            if d == "in":
              if c_t_tmp not in self.hack_types:
                in_params.append(py_type + ' _' + n)
                if c_t_internal == "Eo*":
                  l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n + ".eo")
                elif c_t_internal == "Eo_Event_Eb":
                  l = "  cdef %s %s = <%s> %s"%(c_t_internal, n, c_t_internal, "eodefault._object_callback")
#                elif fparams["parameters"][i-1][1] == "eo_event_cb":
#                  l = ""
                else:

                  if c_t_internal == "char*" :
                    l = "  _%s = pytext_to_utf8(_%s)"%(n, n)
                    function_lines.append(l)
                  l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n)
                function_lines.append(l)
              else:
                in_params.append('_' + n)
                #l = "  assert _%s == None, \"_%s should be None\""%(n, n)
                #function_lines.append(l)
                l = "  cdef void *%s_tmp = NULL if _%s is None else <void*>_%s"%(n, n, n)
                function_lines.append(l)
                #l = "  assert tmp == NULL, \"_%s should be NULL\""%(n)
                #function_lines.append(l)
                l = "  cdef %s %s = <%s> %s_tmp"%(c_t_tmp, n, c_t_tmp, n)
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
        l = "def %s(%s):"% (fname, ', '.join(in_params))
        function_lines.insert(0, l)

        l = '%s(%s.%s)'%(kl_dt['sub_id_function'],
                                   kl_dt['module'],
                                   fparams["op_id"])

        pass_params.insert(0, l)
        l = "%s.%s(self)"%(kl_dt["basemodule"], self._funcs["instance_get"])
        pass_params.insert(0, l)
        l = '  %s.%s(%s)'% (kl_dt["basemodule"], self._funcs["do"],', '.join(pass_params))
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
        self.cl_data[kl_id]["methods_parsed"][fname] = function_lines


    def parse(self, fName):
        self.source_file = fName
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element_handler
        p.ParseFile(open(fName, 'r'))

        mod_name = normalize_names(self.class_data["c_name"]).lower()
        #defining _id function
        if self.globals["extern_base_id"] != "":
          self.globals["sub_id_function"] = '%s_sub_id'%(mod_name)
        else:
          self.globals["sub_id_function"] = ""

        parent_list = []
        parent_list.append(self.class_data["parent"])
        parent_list += self.class_data["extensions"].split(",")

        kl_id = self.class_data["c_name"]
        self.cl_data[kl_id] = \
           {
              "c_name" : self.class_data["c_name"],
              "macro" : self.class_data["macro"],
              "type" : self.class_data["type"],
              "get_function" : self.class_data["get_function"],
              "instantiateable": self.class_data["instantiateable"],
              "includes" : self.includes,
              "functions" : self.functions,
              "module" : mod_name,
              "basemodule" : "eodefault",
              "op_ids" : self.op_ids,
              "ev_ids" : self.ev_ids,
              "extern_base_id" : self.globals["extern_base_id"],
              "extern_funcs" : self.extern_funcs,
              "methods_parsed" : {},
              "sub_id_function" : self.globals["sub_id_function"],
              "source_file" : self.source_file,
              "parents" : parent_list
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
        mod_o.extern_base_id = self.globals["extern_base_id"]
        mod_o.extern_funcs = self.extern_funcs
        mod_o.sub_id_function = self.globals["sub_id_function"]
        mod_o.source_file = self.source_file
        mod_o.parents = parent_list
        mod_o.V = PyVisitor()


        for i in self.functions:
          mod_o.functions[i] = Func(i, self.functions[i]["op_id"], self.functions[i]["c_macro"], self.functions[i]["parameters"], mod_o)


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
        self.globals = {}
        self.globals["extern_base_id"] = ""

#py_parse() - makes all main job - builds funcs, etc.

    def py_parse(self, kl_id):

        #the three following parses are for python, so can be moved
        eo_base_ops = ["EO_BASE_SUB_ID_EVENT_FREEZE", "EO_BASE_SUB_ID_EVENT_FREEZE_GET", \
                       "EO_BASE_SUB_ID_EVENT_THAW", "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE", "EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET",\
                       "EO_BASE_SUB_ID_EVENT_GLOBAL_THAW", "EO_BASE_SUB_ID_DATA_SET", \
                       "EO_BASE_SUB_ID_DATA_GET", "EO_BASE_SUB_ID_DATA_DEL", \
                       "EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD", "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL", \
                       "EO_BASE_SUB_ID_EVENT_CALLBACK_CALL"]

        for key in self.cl_data[kl_id]["functions"]:
            #print self.current_class
            op_id = self.cl_data[kl_id]["functions"][key]["op_id"]

            if kl_id == "Eo Base":
              if op_id not in eo_base_ops:
                continue
            self.parse_methods(kl_id, key)

        self.parse_init_func(kl_id)


    def js_parse(self, kl_id):

       funcs = self.cl_data[kl_id]["functions"]

       self.cl_data[kl_id]["js_cpp_h"] = os.path.join(self.outdir, "_" + self.cl_data[kl_id]["module"]  + ".h")
       self.cl_data[kl_id]["js_cpp_cc"] = os.path.join(self.outdir, "_" + self.cl_data[kl_id]["module"]  + ".cc")

       self.cl_data[kl_id]["properties"] = self.cl_data[kl_id]["methods"] = \
       self.cl_data[kl_id]["properties_set"] = self.cl_data[kl_id]["properties_get"] = []

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
        # if kl_id == "Eo Base":
        #   if funcs[key]["op_id"] not in eo_base_ops:
        #     continue

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


    def check_parents(self):
       list_of_parents = []
       for k in self.cl_data:
         self.cl_data[k]["parents"] = filter(len, self.cl_data[k]["parents"])
         list_of_parents += self.cl_data[k]["parents"]

       list_of_parents = list(set(list_of_parents))

       parents_to_find = filter(lambda l: True if l not in self.cl_data else False, list_of_parents)

       return parents_to_find



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
         self.cl_data[k]["name"] =  normalize_names(self.cl_data[k]["c_name"])
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

        if kl_dt["type"] == self.string_consts["class_type_regular"]:
          priv.append("   static Persistent<FunctionTemplate> tmpl;\n")
          priv.append("\n")

          prot.append("   %s(Local<Object> _jsObject, CElmObject *parent);\n"%(kl_id))

          c_f.append("%s::%s(Local<Object> _jsObject, CElmObject *parent)\n"%(kl_id, kl_id))
          c_f.append(" : CElmObject(_jsObject, eo_add(%s , parent ? parent->GetEo() : NULL))\n"%(kl_dt["macro"]))
          c_f.append("{\n   jsObject->SetPointerInInternalField(0, static_cast<CElmObject*>(this));\n}\n")

          prot.append("   static Handle<FunctionTemplate> GetTemplate();\n")
          prot.append("\n")

          publ.append("   static void Initialize(Handle<Object> target);\n")

          """
          c_f.append("void %s::Initialize(Handle<Object> target)\n"%kl_id)
          c_f.append("{\n")
          c_f.append("   target->Set(String::NewSymbol(\"%s\") , GetTemplate()->GetFunction());\n"%kl_id)
          print "ini", kl_id
          for m in methods:
#FIXME
            print kl_id, m
            if m in ["event_global_freeze", "event_global_thaw"]:
              c_f.append("EO_REGISTER_STATIC_METHOD(%s);\n"% m)
          c_f.append("}\n")
"""

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
           #generating headers of  setter/getter in class (h file)
           ll.append("   Handle<Value> %s_get() const;\n"%(p))
           ll.append("   void %s_set(Handle<Value> val);\n"%(p))

          #generating setter/getter in cc file
           c_f.append("Handle<Value> %s::%s_get() const\n"%(kl_id, p))
           c_f.append("{\n")
           c_f.append("   HandleScope scope;\n")
#          c_f.append("   eo_do(eobj, %s);\n"%(kl_dt["functions"][p + "_get"]["c_macro"]))

           pass_params = []
           ret_params = []
           for i, (n, c_t, d) in enumerate(kl_dt["functions"][p+"_get"]["parameters"]):
             c_t_tmp = self.cast(c_t)
             c_t_internal = self.internal_types[c_t_tmp][0]

             js_type = self.internal_types[c_t_tmp][2]

             if d == "out":
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

           c_f.append("}\n")
           c_f.append("\n")

           c_f.append("void %s::%s_set(Handle<Value> val)\n"%(kl_id, p))
           c_f.append("{\n")

           pass_params = []
           add_end_func = []
           if len(kl_dt["functions"][p+"_set"]["parameters"]) > 1:
             c_f.append("   Local<Object> __o = val->ToObject();\n")

             for i, (n, c_t, d) in enumerate(kl_dt["functions"][p+"_set"]["parameters"]):
               c_t_tmp = self.cast(c_t)
               c_t_internal = self.internal_types[c_t_tmp][0]
               js_type = self.internal_types[c_t_tmp][2]

               if d != "in":
                 print "Warning wrong directiong: property: %s; parameter: %s; direction: %"%(p, n, d)
               else:
                 c_f.append("   %s %s;\n"%(c_t_internal, n))
                 if js_type == "ToString":
                    c_f.append("   %s = strdup(*String::Utf8Value(__o->Get(String::NewSymbol(\"%s\"))->%s()));\n"%(n, n, js_type))
                 else:
                   c_f.append("   %s = __o->Get(String::NewSymbol(\"%s\"))->%s()->Value();\n"%(n, n, js_type))

                 if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                   pass_params.append('&' + n)
                 else:
                   pass_params.append(n)

           elif len(kl_dt["functions"][p+"_set"]["parameters"]) == 1:
             (n, c_t, d) =  kl_dt["functions"][p+"_set"]["parameters"][0]
             c_t_tmp = self.cast(c_t)
             c_t_internal = self.internal_types[c_t_tmp][0]
             js_type = self.internal_types[c_t_tmp][2]

             if d != "in":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %"%(p, n, d)
             else:
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

        for p in kl_dt["properties_set"]:
           #generating headers of  setter/getter in class (h file)
           ll.append("   void %s_set(Handle<Value> val);\n"%(p))

          #generating setter/getter in cc file

           c_f.append("void %s::%s_set(Handle<Value> val)\n"%(kl_id, p))
           c_f.append("{\n")

           pass_params = []
           add_end_func = []
           if len(kl_dt["functions"][p+"_set"]["parameters"]) > 1:
             c_f.append("   Local<Object> __o = val->ToObject();\n")

             for i, (n, c_t, d) in enumerate(kl_dt["functions"][p+"_set"]["parameters"]):
               c_t_tmp = self.cast(c_t)
               c_t_internal = self.internal_types[c_t_tmp][0]
               js_type = self.internal_types[c_t_tmp][2]

               if d != "in":
                 print "Warning wrong direction: property: %s; parameter: %s; direction: %"%(p, n, d)
               else:
                 c_f.append("   %s %s;\n"%(c_t_internal, n))
                 #FIXME: case when we are working with EO
                 if js_type == "ToString":
                    c_f.append("   %s = strdup(*String::Utf8Value(__o->Get(String::NewSymbol(\"%s\"))->%s()));\n"%(n, n, js_type))
                 else:
                   c_f.append("   %s = __o->Get(String::NewSymbol(\"%s\"))->%s()->Value();\n"%(n, n, js_type))

                 if c_t.find(c_t_internal) != -1 and c_t.replace(c_t_internal, "") == "*":
                   pass_params.append('&' + n)
                 else:
                   pass_params.append(n)


           elif len(kl_dt["functions"][p+"_set"]["parameters"]) == 1:
             (n, c_t, d) =  kl_dt["functions"][p+"_set"]["parameters"][0]
             c_t_tmp = self.cast(c_t)
             c_t_internal = self.internal_types[c_t_tmp][0]
             js_type = self.internal_types[c_t_tmp][2]

             if d != "in":
               print "Warning wrong direction: property: %s; parameter: %s; direction: %"%(p, n, d)
             else:
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

        for p in kl_dt["properties_get"]:
           #generating headers of  setter/getter in class (h file)
           ll.append("   Handle<Value> %s_get() const;\n"%(p))

          #generating setter/getter in cc file
           c_f.append("Handle<Value> %s::%s_get() const\n"%(kl_id, p))
           c_f.append("{\n")
           c_f.append("   HandleScope scope;\n")

           pass_params = []
           ret_params = []
           for i, (n, c_t, d) in enumerate(kl_dt["functions"][p+"_get"]["parameters"]):
             c_t_tmp = self.cast(c_t)
             c_t_internal = self.internal_types[c_t_tmp][0]
             js_type = self.internal_types[c_t_tmp][2]

             if d == "out":
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
           for i, (n, c_t, d) in enumerate(kl_dt["functions"][m]["parameters"]):
             c_t_tmp = self.cast(c_t)
             c_t_internal = self.internal_types[c_t_tmp][0]
             js_type = self.internal_types[c_t_tmp][2]

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
             c_f.append("   return scope.Close(obj__);//need to put proper values\n")
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




    def outdir_set(self, _d):
      self.outdir = _d

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
        cl_type = self.objects[l].eo_type
        if cl_type == self.string_consts["class_type_mixin"]: # "EOBJ_CLASS_TYPE_MIXIN":
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
      prnts = self.cl_data[kl]["parents"]

      l = []
      for p in prnts:
        if p != "EoBase":
          l = l + self.get_parents(p)

      l = list(set(l + prnts))
#      l = filter(lambda el: el != "EoBase", l)

      return l

