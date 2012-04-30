import xml.parsers.expat, os, shutil
from helper import normalize_names


class XMLparser(object):
    def __init__(self):

        self.globals = {}
        self.cl_data = {}
        self.cl_incl = {}
        """
        self.properties = {}
        """

        #internal functions, used in eodefault.pyx
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

        self.cl_incl["EoDefault"] = self.basemodule

        self.typedefs = {"Evas_Coord" : "int",
                         "Evas_Angle":"int",
                         "Evas_Font_Size" : "int",
                         "Eina_Bool" : "unsigned char",
                         "Eo_Callback_Priority": "short"}

        self.primary_types = {"Eo**" : "Eo*",
                              "void**" : "void*",
                              "char**" : "char*"}

        self.internal_types = {
                                "void*": ["void*", "object"],
                                "char*": ["char*", "object"],
                                "Eo*":  ["Eo*", self.basemodule["name"]],
                                "short" : ["int", "int"],
                                "int": ["int", "int"],
                                "int*": ["int", "int"],
                                "long": ["long", "long"],
                                "long*": ["long", "long"],
                                "long long" : ["long long", "long long"],
                                "long long*" : ["long long", "long long"],
                                "unsigned char": ["unsigned char", "int"],
                                "unsigned char*" : ["unsigned char","int"],
                                "unsigned int": ["unsigned int", "unsigned int"],
                                "unsigned int*": ["unsigned int", "unsigned int"],
                                "unsigned long": ["unsigned long", "unsigned long"],
                                "unsigned long*": ["unsigned long", "unsigned long"],
                                "unsigned long long": ["unsigned long long", "unsigned long long"],
                                "unsigned long long*": ["unsigned long long", "unsigned long long"],
                                "float": ["float", "float"],
                                "double": ["double", "double" ],
                                "long double": ["long double", "long double"],
                                "float*": ["float", "float"],
                                "double*": ["double", "double" ],
                                "long double*": ["long double", "long double"],
                                "Eo_Event_Description*":["long","long"],
                                "Eo_Event_Cb":["Eo_Event_Cb","object"],
                                "eo_base_data_free_func" : ["", ""]
                                }

        self.string_consts = {"class_type_mixin" : "EO_CLASS_TYPE_MIXIN",
                              "class_type_regular" : "EO_CLASS_TYPE_REGULAR",
                          }


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
        self.signals = []
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
            self.functions.setdefault(self.current_func, {"op_id":attrs["op_id"]})

        elif name == "signal":
            self.signals.append((attrs["name"], attrs["op_id"]))

        elif name == "parameter":
            func_att = self.functions[self.current_func]
            par_att = func_att.setdefault('parameters', [])
            par_att.append((attrs["name"], attrs["c_typename"], attrs["direction"]))

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

    """
building __init__ function
"""
    def parse_init_func(self):

        kl = self.current_class
        kl_dt = self.cl_data[kl]

        function_lines = []
        l = "def __init__(self, EoDefault parent):"
        function_lines.append(l)

        l = "  instantiateable = %s"%(self.class_data["instantiateable"])
        function_lines.append(l)

        l = "  if not instantiateable:"
        function_lines.append(l)
        l = "    print \"Class '%s' is not instantiate-able. Aborting.\"%(self.__class__.__name__)"
        function_lines.append(l)
        l = "    exit(1)"
        function_lines.append(l)

        if self.class_data["instantiateable"] == "True":
          l = "  klass = <long>%s.%s()"%(kl_dt["module"], kl_dt["get_function"])
          function_lines.append(l)
          l = "  self.%s(klass, parent)"%self._funcs["instance_set2"]
          function_lines.append(l)
          l = "  self.data_set(EoDefault.PY_EO_NAME, self)"
          function_lines.append(l)
        function_lines.append("")


        function_lines.append("")
        self.cl_data[self.current_class]["methods_parsed"]["__init__"] = function_lines



    def cast(self, _in):
      t = _in
      for k in self.typedefs:
        if t.find(k) != -1:
          t = t.replace(k, self.typedefs[k])

      for k in self.primary_types:
        if t.find(k) != -1:
          t = t.replace(k, self.primary_types[k])
      return t

    def parse_methods(self, fname, fparams):
        kl = self.current_class
        kl_dt = self.cl_data[kl]
        in_params = []
        pass_params =[]
        ret_params = []
        function_lines = []



        if kl == "Eo Base":
          if fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD":
            function_lines.append("def event_callback_priority_add(self, long _desc, int _priority, object _cb):")
            function_lines.append("  if not callable(_cb):")
            function_lines.append("    raise TypeError(\"func must be callable\")")
            function_lines.append("  cdef Eo_Event_Cb cb = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD), _desc, _priority, cb, <void*>_cb)")
            function_lines.append("\n")
            self.cl_data[self.current_class]["methods_parsed"][fname] = function_lines
            return
          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL":
            function_lines.append("def event_callback_del(self, long _desc, object _func):")
            function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL), _desc, func, <void*>_func)")

            function_lines.append("\n")
            self.cl_data[self.current_class]["methods_parsed"][fname] = function_lines
            return
          elif fparams["op_id"] == "EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY":
            function_lines.append("def event_callback_del_lazy(self, long _desc, object _func):")
            function_lines.append("  cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback")
            function_lines.append("  cdef void * user_data")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL_LAZY), _desc, func, &user_data)")
            function_lines.append("  return None if user_data == NULL else <object>user_data")
            function_lines.append("\n")
            self.cl_data[self.current_class]["methods_parsed"][fname] = function_lines
            return
          elif fparams["op_id"] == "EO_BASE_SUB_ID_DATA_SET":
            function_lines.append("def data_set(self, object _key, object _data):")
            function_lines.append("  _key = pytext_to_utf8(_key)")
            function_lines.append("  cdef char* key = <char*> _key")
            function_lines.append("  eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)")

            function_lines.append("\n")
            self.cl_data[self.current_class]["methods_parsed"][fname] = function_lines
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
               print "Warning: type: \"%s\" wasn't found in self.internal_types. Functon \"%s\" will not be defined"%(c_t_tmp, fname)
               return

            if d == "in":
              if c_t_tmp not in self.hack_types:
                in_params.append(py_type + ' _' + n)
                if c_t_internal == "Eo*":
                  l = "  cdef %s %s = <%s> _%s"%(c_t_internal, n, c_t_internal, n + ".eo")
                elif c_t_internal == "Eo_Event_Cb":
                  l = "  cdef %s %s = <%s> %s"%(c_t_internal, n, c_t_internal, "eodefault._object_callback")
#                elif fparams["parameters"][i-1][1] == "Eo_Event_Cb":
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
                #l = "  assert tmp == NULL, \"_%s should be null\""%(n)
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
        self.cl_data[self.current_class]["methods_parsed"][fname] = function_lines

    def parse_signals(self):
        kl = self.current_class
        kl_dt = self.cl_data[kl]
        for n, sig_id in kl_dt["signals"]:
          function_lines = []
          if n[-4:] == "_add":
             l = "def " + n + "(self, priority, func, *args, **kwargs):"
             function_lines.append(l)
             l = "  cdef long id_desc = <long>%s.%s"%(kl_dt["module"], sig_id)
             function_lines.append(l)
             l = "  self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)"
             function_lines.append(l)

          elif n[-4:] == "_del":
             l = "def " + n + "(self, func):"
             function_lines.append(l)
             l = "  cdef long id_desc = <long>%s.%s"%(kl_dt["module"], sig_id)
             function_lines.append(l)
             l = "  self._object_callback_del(id_desc, func)"
             function_lines.append(l)

          function_lines.append("")
          self.cl_data[self.current_class]["methods_parsed"][n] = function_lines


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

        self.current_class = self.class_data["c_name"]
        self.cl_data[self.current_class] = \
           {
              "c_name" : self.class_data["c_name"],
              "macro" : self.class_data["macro"],
              "type" : self.class_data["type"],
              "get_function" : self.class_data["get_function"],
              "instantiateable": self.class_data["instantiateable"],
              "includes" : self.includes,
              "functions" : self.functions,
              "signals" : self.signals,
              "module" : mod_name,
              "basemodule" : self.basemodule["module"],
              "op_ids" : self.op_ids,
              "ev_ids" : self.ev_ids,
              "extern_base_id" : self.globals["extern_base_id"],
              "extern_funcs" : self.extern_funcs,
              "methods_parsed" : {},
              "sub_id_function" : self.globals["sub_id_function"],
              "source_file" : self.source_file,
              "parents" : parent_list
            }
        self.functions = {}
        self.signals = []
        self.includes = []
        self.op_ids = []
        self.ev_ids = []
        self.extern_funcs = []
        self.globals = {}
        self.globals["extern_base_id"] = ""

        #the three following parses are for python, so can be moved
        for key in self.cl_data[self.current_class]["functions"]:
            self.parse_methods(key, self.cl_data[self.current_class]["functions"][key])

        self.parse_signals()
        self.parse_init_func()

    def check_parents(self):
       list_of_parents = []
       for k in self.cl_data:
         self.cl_data[k]["parents"] = filter(len, self.cl_data[k]["parents"])
         list_of_parents += self.cl_data[k]["parents"]

       list_of_parents = list(set(list_of_parents))

       parents_to_find = filter(lambda l: True if l not in self.cl_data else False, list_of_parents)

       return parents_to_find

    def build_python_modules(self, module_name, pkg, sourcedir):
       cl_data_tmp = {}
       module_file = module_name + ".pyx"

       for k in self.cl_data:
         self.cl_data[k]["name"] =  normalize_names(self.cl_data[k]["c_name"])
         self.cl_data[k]["parents"] = normalize_names(self.cl_data[k]["parents"])
         cl_data_tmp[self.cl_data[k]["name"]] = self.cl_data[k]

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
         self.build_module(k)

       lines = []
       lines.append("from distutils.core import setup")
       lines.append("from distutils.extension import Extension")
       lines.append("from Cython.Distutils import build_ext")
       lines.append("import commands, os")
       lines.append("")

       lines.append("def pkgconfig(_libs):")
       lines.append("  cf = commands.getoutput(\"pkg-config --cflags %s\"%_libs).split()")
       lines.append("  ldf = commands.getoutput(\"pkg-config --libs %s\"%_libs).split()")
       lines.append("  return (cf, ldf)")
       lines.append("")

       lines.append("(e_compile_args, e_link_args) = pkgconfig(\"%s\")"%pkg)
       lines.append("")

       lines.append("e_include_dirs = [\".\"]")
       lines.append("e_library_dirs = []")
       lines.append("e_libraries = []")
       lines.append("")
#       if module_name == "eobase":
#         lines.append("os.system(\"rm __init__.py*\")")
#       lines.append("")

       lines.append("setup(")
       lines.append("  cmdclass = {'build_ext': build_ext},")
       lines.append("  ext_modules = [")

       if "EoBase" in self.cl_data:
         lines.append("  Extension(\"%s\", ['%s'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),"%(self.basemodule["module"], self.basemodule[".pyx"]))

       lines.append("  Extension(\"%s\", ['%s'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),"%(module_name, module_name + ".pyx"))

       lines.append("   ])\n")

 #      if module_name == "eobase":
 #        lines.append("f = open('__init__.py', 'w')")
 #        lines.append("f.write('import eodefault\\n')")
 #        lines.append("f.write('eodefault.init()\\n')")
 #        lines.append("f.close()")

       lines.append("\n")


       f = open (os.path.join(self.outdir, "setup.py"), 'w')
       for l in lines:
         f.write(l + "\n")
       f.close()

#building right order of including files
       cl_parents = {}
       lst = []
       for k in self.cl_data:
          cl_parents[k] = self.cl_data[k]["parents"]

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
       lines.append("from eodefault cimport *")
       lines.append("\n")
       for k in lst:
         lines.append("include \"%s\""%os.path.split(self.cl_data[k][".pxi"])[1])

       f = open (os.path.join(self.outdir, module_file), 'w')
       for l in lines:
         f.write(l + "\n")
       f.close()

       f_pyx = os.path.join(sourcedir, self.basemodule[".pyx"])
       f_pxd = os.path.join(sourcedir, self.basemodule[".pxd"])
       f_init = os.path.join(sourcedir, "__init__.py")
       try:
         shutil.copy(f_pyx, self.outdir)
         shutil.copy(f_pxd, self.outdir)
         shutil.copy(f_init, self.outdir)
       except IOError as ex:
          print "%s"%ex
          print "Aborting"
          exit(1)
       except shutil.Error as er:
          print "Warning: %s"%er


    def build_module(self, kl_id):
#creating .pyx file

        kl_dt = self.cl_data[kl_id]

        kl_dt[".pyx"] = os.path.join(self.outdir, kl_dt["module"]  + ".pyx")
        kl_dt[".pxd"] = os.path.join(self.outdir, kl_dt["module"]  + ".pxd")
        kl_dt[".pxi"] = os.path.join(self.outdir, kl_dt["module"]  + ".pxi")

        f = open (kl_dt[".pxi"], 'w')
        pattern = "########################################################"
        l = '%s\n##\n## generated from from \"%s\"\n##\n%s'%(pattern, kl_dt["source_file"], pattern)
        f.write(l+'\n\n')

        #inserting cimports
        l = "cimport %s"%kl_dt["module"]
        f.write(l+'\n')
        l = "cimport %s"%kl_dt["basemodule"]
        f.write(l+'\n\n')

        #defining class
        parents = []
        if len(kl_dt["parents"]) != 0:
          parents = kl_dt["parents"]


        if kl_dt["name"] == "EoBase":
           parents = []
           parents.append(self.basemodule["name"])
           l = "from %s import %s"%(self.basemodule["module"], self.basemodule["name"])
           f.write(l + "\n")

        if "EoBase" in parents:
          l = "from %s import %s"%("eobase", "EoBase")
          f.write(l + "\n")

        l = "from %s import %s"%(self.basemodule["module"], "pytext_to_utf8")
        f.write(l + "\n")

        f.write("\n")

        #defining _id function
        if kl_dt["extern_base_id"] != "":
          l = 'cdef int %s(int sub_id):'%(kl_dt["sub_id_function"])          
          f.write(l+'\n')
          l = '  return %s.%s + sub_id'%(kl_dt["module"],
                                         kl_dt["extern_base_id"])          
          f.write(l+'\n\n')
        parents = ",".join(self.reorder_parents(parents))
        #defining class
        l = 'class %s(%s):'%(kl_dt["name"], parents)
        f.write(l+'\n\n')

        #defining event globals
        for v in kl_dt["ev_ids"]:
          pos = v.find("EV_")
          if pos == -1:
            continue
          name = v[pos + 3:]
          l = "  %s = <long>%s.%s"%(name, kl_dt["module"], v)
          f.write(l + '\n')
        f.write('\n')

        methods_parsed = kl_dt["methods_parsed"]
        #inserting class methods
        for key in methods_parsed:
            func = methods_parsed[key]
            for l in func:
               f.write('  '+l+'\n')
        f.close()
        del methods_parsed

        #creating .pxd file
        f = open (kl_dt[".pxd"], 'w')
        pattern = "########################################################"
        l = "%s\n##\n## generated from from \"%s\"\n##\n%s"%(pattern, kl_dt["source_file"], pattern)
        f.write(l+'\n\n')

        #inserting cimports
        l = "from %s cimport *"%(kl_dt["basemodule"])
        f.write(l+'\n\n')

        #inserting externs from H
        l = "cdef extern from \"%s\":"%(kl_dt["includes"][0])
        f.write(l+'\n\n')

        if kl_dt["extern_base_id"] != "":
          l = '  %s %s'%("Eo_Op", kl_dt["extern_base_id"])
          f.write(l+'\n\n')
        enum_lines = []
        enum_lines.append("  ctypedef enum:")
        for v in kl_dt["op_ids"]:
          #inserting extern enums from H into temp list
          if len(enum_lines) > 1 :
            enum_lines[-1] = enum_lines[-1] + ','
          enum_lines.append('    ' + v)
          continue

        for v in kl_dt["ev_ids"]:
          l = '  %s %s'%("Eo_Event_Description *", v)
          f.write(l+'\n')
        f.write('\n')

        if len(enum_lines) > 1:
            for l in enum_lines:
                f.write(l+'\n')
            f.write('\n')

        for v in kl_dt["extern_funcs"]:
            l = '  %s %s'%(v[1], v[0])
            f.write(l+'\n')
        f.write('\n')

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
        cl_type = self.cl_data[l]["type"]
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


