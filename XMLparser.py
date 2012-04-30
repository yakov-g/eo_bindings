import xml.parsers.expat


def print_error(s):
    print "ERROR: ",
    print s
    exit()

class XMLparser(object):
    def __init__(self):

        self.globals = {}

        self.types = {"Evas_Coord" : "int"}
        self.source_file = ""
        self.cimports = []
        self.imports = []
        self.includes = []
        self.extern_vars = []
        self.extern_funcs = []
        
        self.class_data = {}
        self.functions = {} #function names with parameters
        self.current_func = ""
        self.methods_parsed = {} #ready function lines
        self.signals = []
        self.hack_types = ["eobj_base_data_free_func"]

        self.globals["extern_base_id"] = ""

    def testall(self):
        if self.globals["module"] is "":
            s = "module name is unknown... aborting..."
            print_error(s)

        if self.globals["basemodule"] is "":
            s = "basemodule name is unknown... aborting..."
            print_error(s)
 
        if self.class_data["get_function"] is "":
            s = "class_get function name is unknown... aborting..."
            print_error(s)

        if len(self.cimports) < 2:
            s = "cimports array's len is %d; should be at least %d... aborting..."%(len(self.cimports), 2)
            print_error(s)

        if len(self.includes) < 1:
            s = "includes array's len is %d; should be at least %d... aborting..."%(len(self.includes), 1)
            print_error(s)

        if  self.globals["module"] not in self.cimports:
            s =  "%s.pxd wasn't imported into %s.pyx... aborting..."%(self.module, self.module)
            print_error(s)

        if  self.globals["basemodule"] not in self.cimports:
           s = "%s.pxd wasn't imported into %s.pyx... aborting..."%(self.globals["basemodule"], self.globals["basemodule"])
           print_error(s)

    def printall(self):   
        print "module:\t", self.globals["module"]
        print "basemodule:\t", self.globals["basemodule"]
        print "cimports:\t", self.cimports
        print "includes:\t", self.includes
        print "class_data:\t", self.class_data
        print "extern_vars:\t", self.extern_vars
        print "extern_funcs:\t", self.extern_funcs

        
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
            par_att.append((attrs["name"], attrs["typename"], attrs["c_typename"], attrs["direction"]))

        elif name == "module":
            self.globals['module'] = attrs['name']

        elif name == "basemodule":
            self.globals["basemodule"] = attrs["name"]

        elif name == "cimport":
            self.cimports.append(attrs["name"])

        elif name == "import":
            self.imports.append((attrs["module"], attrs["class"]))
        
        elif name == "include":
            self.includes.append(attrs["name"])

        elif name == "class":
            self.class_data = attrs
   
        elif name == "extern":
            self.extern_vars.append((attrs["name"], attrs["typename"])) 

        elif name == "extern_base_id":
            self.globals["extern_base_id"] = ((attrs["name"], attrs["typename"])) 

        elif name == "extern_function":
            self.extern_funcs.append((attrs["name"], attrs["typename"])) 

        else:
            #print 'Start element:', name, attrs
            pass

    def end_element_handler(self, name):
        pass
        #print 'End element:', name

    def character_data_handler(self, data):
        if data:
            data = data.encode("ascii")
        print "Character data:", repr(data)        

    """
building __init__ function
"""
    def parse_init_func(self):
        function_lines = []
        l = "def __init__(self, EobjDefault parent):"
        function_lines.append(l)
        
        l = "  instantiateable = %s"%(self.class_data["instantiateable"])
        function_lines.append(l)

        l = "  if not instantiateable:"
        function_lines.append(l)
        l = "    print \"Class '%s' is not instantiate-able. Aborting.\"%(self.__class__.__name__)"
        function_lines.append(l)
        l = "    exit()"
        function_lines.append(l)

        if self.class_data["instantiateable"] == "True":
          l = "  klass = <long>%s.%s()"%(self.globals["module"], self.class_data["get_function"])
          function_lines.append(l)
          l = "  self._eobj_instance_set2(klass, parent)"
          function_lines.append(l)
          l = "  self.data_set(\"python-eobj\", self, None)"
          function_lines.append(l)
        function_lines.append("")


        function_lines.append("")
#FIXME put '!' as index ito the dictionary to make '__init__' function to be the first
        self.methods_parsed["!"] = function_lines

    def parse_methods(self, fname, fparams):
       
        in_params = []
        pass_params =[]
        ret_params = []
        function_lines = []

        if "parameters" in fparams:
          for n, t, c_t, d in fparams["parameters"]:
           
            if c_t == "Eobj*" and d == "in":
              in_params.append(t + ' _' + n)
              l = "  cdef %s %s = <%s> _%s"%(c_t, n, c_t, n + ".eobj")
              function_lines.append(l);
              pass_params.append(n)
              continue

            if d == "in":
              if t not in self.hack_types:
                in_params.append('_' + n)
                l = "  cdef %s %s = <%s> _%s"%(t, n, t, n)
                function_lines.append(l)
              else:
                in_params.append('_' + n)
                #l = "  assert _%s == None, \"_%s should be None\""%(n, n)
                #function_lines.append(l)
                l = "  cdef void *%s_tmp = NULL if _%s is None else <void*>_%s"%(n, n, n)
                function_lines.append(l)
                #l = "  assert tmp == NULL, \"_%s should be null\""%(n)
                #function_lines.append(l)
                l = "  cdef %s %s = <%s> %s_tmp"%(t, n, t, n)
                function_lines.append(l)

              if c_t.find('*') != -1 and c_t != "char*" and c_t != "void*":
                pass_params.append('&' + n)
              else:
                pass_params.append(n)


            elif d == "out":
              l = "  cdef %s %s"%(t, n)
              pass_params.append('&' + n)
              ret_params.append((n + '_', t))
              function_lines.append(l);

            elif d == "in,out":
              in_params.append('_' + n)
              pass_params.append('&' + n)
              l = "  cdef %s %s = <%s> _%s"%(t, n, t, n)
              ret_params.append((n + '_', t))
              function_lines.append(l);

        in_params.insert(0, "self")
        l = "def %s(%s):"% (fname, ', '.join(in_params))   
        function_lines.insert(0, l)

        l = '%s(%s.%s)'%(self.globals['sub_id_function'],
                                   self.globals['module'],
                                   fparams["op_id"])

        pass_params.insert(0, l)
        l = "%s._eobj_instance_get(self)"%(self.globals["basemodule"])
        pass_params.insert(0, l)
        l = '  %s.eobj_do(%s)'% (self.globals["basemodule"], ', '.join(pass_params))
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
        self.methods_parsed[fname] = function_lines


    def parse_signals(self):
        for n, sig_id in self.signals:
          function_lines = []
          if n[-4:] == "_add":
             l = "def " + n + "(self, priority, func, *args, **kwargs):"
             function_lines.append(l)
             l = "  cdef long id_desc = <long>%s.%s"%(self.globals["module"], sig_id)
             function_lines.append(l)
             l = "  self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)"
             function_lines.append(l)
             
      
          elif n[-4:] == "_del":
             l = "def " + n + "(self, func):"
             function_lines.append(l)
             l = "  cdef long id_desc = <long>%s.%s"%(self.globals["module"], sig_id)
             function_lines.append(l)
             l = "  self._object_callback_del(id_desc, func)"
             function_lines.append(l)

          function_lines.append("")
          self.methods_parsed[n] = function_lines



    def parse(self, fName):
        self.source_file = fName
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element_handler
        p.EndElementHandler = self.end_element_handler
#       p.CharacterDataHandler = self.character_data_handler
        p.ParseFile(open(fName, 'r'))

        #defining _id function
        if self.globals["extern_base_id"] != "":
          self.globals["sub_id_function"] = '%s_sub_id'%(self.globals["module"])
 
        for key in self.functions:
            self.parse_methods(key, self.functions[key])
      
        self.parse_signals()
        self.parse_init_func()

        
    def build_module(self):
#creating .pyx file
        pyx_filename = self.globals["module"] + ".pyx"
        f = open (pyx_filename, 'w')
        pattern = "########################################################"
        l = '%s\n##\n## generated from from \"%s\"\n##\n%s'%(pattern, self.source_file, pattern)
        f.write(l+'\n\n')

        #inserting cimports
        for v in self.cimports:
            l = 'cimport ' + v
            f.write(l+'\n')
        f.write('\n')  

        #inserting imports
        for m, cl in self.imports:
            l = "from %s import %s"%(m ,cl)
            f.write(l+'\n')
        f.write('\n')  
        
        #defining _id function
        if self.globals["extern_base_id"] != "":
          l = 'cdef int %s(int sub_id):'%(self.globals["sub_id_function"])          
          f.write(l+'\n')
          l = '  return %s.%s + sub_id'%(self.globals["module"],
                                         self.globals["extern_base_id"][0])          
          f.write(l+'\n\n')

        #defining class
        l = 'class %s(%s,%s):'%(self.class_data['name'], self.class_data['parent'], self.class_data["brothers"])          
        f.write(l+'\n\n')

        #inserting class methods
        for key in self.methods_parsed:
            func = self.methods_parsed[key]
            for l in func:
               f.write('  '+l+'\n')
              # print l
        f.close()

  
        #creating .pxd file
        pxd_filename = self.globals["module"] + ".pxd"
        f = open (pxd_filename, 'w')
        pattern = "########################################################"
        l = "%s\n##\n## generated from from \"%s\"\n##\n%s"%(pattern, self.source_file, pattern)
        f.write(l+'\n\n')

        #inserting cimports
        l = "from %s cimport *"%(self.globals["basemodule"])
        f.write(l+'\n\n')

        #inserting externs from H
        l = "cdef extern from \"%s\":"%(self.includes[0])
        f.write(l+'\n\n')  
        
        if self.globals["extern_base_id"] != "":
          l = '  %s %s'%(self.globals["extern_base_id"][1], self.globals["extern_base_id"][0])
          f.write(l+'\n\n')  

        enum_lines = []
        enum_lines.append("  ctypedef enum:")
        for v in self.extern_vars:
            #inserting extern enums from H into temp list
            if v[1] == "enum":
                if len(enum_lines) > 1 :
                    enum_lines[-1] = enum_lines[-1] + ','
                enum_lines.append('    '+v[0])
                continue
           
            #writing  extern from H into file
            l = '  %s %s'%(v[1], v[0])
            f.write(l+'\n')
        f.write('\n')  

        if len(enum_lines) > 1:
            for l in enum_lines:
                f.write(l+'\n')
            f.write('\n')

        for v in self.extern_funcs:
            l = '  %s %s'%(v[1], v[0])
            f.write(l+'\n')
        f.write('\n')  

        f.close()

    def strip_replace(self, data, s):
      data = data.strip(s)
      data = data.replace(" ", "")    
      return data







