import xml.parsers.expat
import sys, os, re

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from string import capwords
from helper import normalize_names
from helper import _const

const = _const()


#filter func to throw out from comment everything
#but the @def, @param
def macro_filter_func(l):
  l = " ".join(l.split()) #removing more than one spaces
  if "@def" in l or "@param" in l:
    return True
  else:
    return False

print_flag = False
def verbose_print(mes):
  if print_flag:
    print mes

class Cparser(object):
  def __init__(self, _print_flag):
    global print_flag
    print_flag = _print_flag
    self.cl_data = {}
    self.cl_incl = {}

    self.op_desc = "Eo_Op_Description op_desc"
    self.ev_desc = "Eo_Event_Description *event_desc"
    self.cl_desc = "Eo_Class_Description class_desc"
    self.key_words = [self.op_desc, self.ev_desc, self.cl_desc]

    self.outdir = ""
    self.typedefs = {"Evas_Coord" : "int",
                     "Evas_Angle":"int",
                     "Evas_Font_Size" : "int",
                     "Eina_Bool" : "bool",
                     "Eo_Callback_Priority": "short"}


  #parsing function, to parse typedef file
  def typedefs_xml_parser(self, name, attrs):
      attrs_ascii = {}
      for key, val in attrs.iteritems():
         attrs_ascii[key.encode("ascii")] = val.encode("ascii")

      attrs = attrs_ascii

      if name == "type":
         fr = attrs["from"]
         to = attrs["to"]
         fr = " ".join(fr.split())
         fr = fr.replace(" *", "*")
         to = " ".join(to.split())
         to = to.replace(" *", "*")
         if fr not in self.typedefs:
           self.typedefs[fr] = to
      else:
         pass

  def typedefs_add(self, fName):
     p = xml.parsers.expat.ParserCreate()
     p.StartElementHandler = self.typedefs_xml_parser
     p.ParseFile(open(fName, 'r'))

  #typedef resolving
  # _in - in type
  # Returns resolved type
  def typedef_resolve(self, _in):
    stars = ""

    l = _in.split('*', 1)
    t_tmp = l[0]
    stars += l[1]+'*' if len(l) == 2 else ""

    while t_tmp in self.typedefs:
      t_tmp = self.typedefs[t_tmp]

      l = t_tmp.split('*', 1)
      t_tmp = l[0]
      stars += l[1]+'*' if len(l) == 2 else ""

    return t_tmp + stars

  def fetch_data(self, _in_data):
    def_list = []

    reg = "EO_DEFINE_CLASS\((.*)\).*"
    def_list += re.findall(reg, _in_data)

  #event_desc structure
  #
  #  EO_DEFINE_CLASS(elm_scrollable_interface_get, &_elm_scrollable_interface_desc, NULL, EVAS_SMART_SCROLLABLE_INTERFACE, NULL);
  #

    class_def = {}
    class_desc = {}
    ev_desc = {"NULL" : []}
    #print "def list: ", def_list
    for s in def_list:
       s = s.replace(" ", "")
       s = s.replace("\n", "")
       l_tmp = s.split(",")

       key = l_tmp[0].strip(" ")
       desc_var = l_tmp[1].strip(" &")
       parent = l_tmp[2]
       l_tmp = l_tmp[3:-1]
       l_tmp = filter(lambda l: False if l == "NULL" else True, l_tmp)

       class_def[key] = [desc_var, parent, l_tmp]
    

  #event_desc structure
  # { EV_CLICKED, EV_BUTTON_DOWN, EV_BUTTON_UP, NULL  }
  #
    reg = "Eo_Event_Description[ *]*([a-zA-Z0-9_]*)[][ =]*{([^}]*)};"
    af = _in_data.replace("\n", "")
    ev_list = re.findall(reg, af)

    for tup in ev_list:
       key = tup[0]
       lst = tup[1].replace(" ", "").split(",")
       if lst[-1] != "NULL":
         print "ERROR: last event descriptor should be NULL in class %s"%(cl_id)
         exit(1)
       lst = filter(lambda l: False if l == "NULL" else True, lst)
       ev_desc[key] = lst

   #  fetching
   #  op description
   #
    reg = "Eo_Op_Description[ ]*([a-zA-Z0-9_]*)\[\][ =]*{([^}]*)};"
    all_op_descs = re.findall(reg, af)
    op_desc = {"NULL" : []}
    for tup in all_op_descs:
      s_tmp = tup[1]
      # fetching op_ids and descriptions
      reg =  "EO_OP_DESCRIPTION[^\)]*\([ ]*([A-Z_]*)[ ]*,[ ]*\"([^\"]*)\"[ ]*\),"
      ids_and_descs = re.findall(reg, s_tmp)

      op_list = []
      for t in ids_and_descs:
         op_id = t[0] #op_id
         func_name = re.findall("SUB_ID_(.*)", op_id)
         op_list.append((op_id, func_name[0].lower()))

      op_desc[tup[0]] = op_list


    ###
    # Class desc structure:
    # {
    #[0]    EO_VERSION
    #[1]    "Evas_Object_Line",
    #[2]    EO_CLASS_TYPE_REGULAR,
    #[3]    EO_CLASS_DESCRIPTION_OPS(&EVAS_OBJ_LINE_BASE_ID, op_desc, EVAS_OBJ_LINE_SUB_ID_LAST),
    #[4]    NULL,
    #[5]    sizeof(Evas_Object_Line),
    #[6]    _class_constructor,
    #[7]    NULL
    # }
    #
    reg = "Eo_Class_Description[ ]*([a-zA-Z0-9_]*)[ =]*{([^}]*)};"
    desc_list = re.findall(reg, af)

    for tup in desc_list:
       key = tup[0]
       l_tmp = smart_split(tup[1])
       ver = l_tmp[0].strip(" ")
       name = l_tmp[1].strip(" ")
       cl_type = l_tmp[2].strip(" ")
       
       #splitting string into list
       desc_ops = l_tmp[3].replace(" ", "").replace("&", "")
       desc_ops = re.findall("\(([^)]*)\)" , desc_ops)[0].split(",")
       #mapping op_desc var name into ops list
       #if op_desc == NULL; t.e. no op_id for current class; NULL will be changed to empty list
       desc_ops[1] = op_desc[desc_ops[1]]

       ev_desc_var = l_tmp[4].strip(" ")

       if -1 == name.find("\""):
          name = name.strip(" ")
          reg = "#define[ ]*%s[ ]*(\"[^\"]*\")"%name
          ll = re.findall(reg, af)
          if len(ll):
            name = ll[0]

       name = name.strip("\"")
#       l_tmp = tup[1].split(",")
       class_desc[key] = [name, cl_type, desc_ops, ev_desc[ev_desc_var]]

    #mapping class_desc_var_name to content
    for key, data in class_def.iteritems():
       class_def[key] += class_desc[data[0]]
       class_def[key].pop(0)
    """
    for key, data in class_def.iteritems():
       print key, " -> ", data
       """



    return class_def

  def c_file_data_get2(self, filename):

    f = open(filename, 'r')
    allfile = f.read()
    f.close()
    ttt = self.fetch_data(allfile)

    #for each class which was found it c-file
    for key, data in ttt.iteritems():

       func_pos = 0

       cl_id = key
       lst = []
       lst.append(data[0]) 
       lst += data[1]
       lst = filter(lambda l: False if l == "NULL" else True, lst)

       if cl_id in self.cl_data:
         verbose_print("Class %s from file %s won't be added in the tree"%(cl_id, filename))
         verbose_print("Class %s from file %s will be used as parent in inheritance"%(cl_id, self.cl_data[cl_id][const.C_FILE]))
         return

       self.cl_data[cl_id] = {const.PARENTS:lst,
                                      const.C_FILE:filename,
                                      const.FUNCS:{}}

       cl_name = data[2]
       self.cl_data[cl_id][const.C_NAME] = cl_name

       self.cl_data[cl_id][const.MODULE] = normalize_names([cl_name])[0].lower()
       self.cl_data[cl_id][const.TYPE] = data[3]
       self.cl_data[cl_id][const.EV_DESC] = data[5]
   #   self.cl_data[cl_id][const.CLASS_CONSTRUCTOR] = lst[5]

       class_desc_ops = data[4]
       self.cl_data[cl_id][const.OP_DESC] = class_desc_ops[1]

       for tup in class_desc_ops[1]:
          self.cl_data[cl_id][const.FUNCS][tup[1]] = {const.OP_ID : tup[0], const.C_MACRO: ""}

       s = class_desc_ops[0]
       if s == "NULL" and cl_name == "Eo Base":
#FIXME: hardcoded EO_BASE_BASE_ID
         print cl_name, "Warning: hardcoded EO_BASE_BASE_ID"
         s = "EO_BASE_BASE_ID"
       self.cl_data[cl_id][const.BASE_ID] = s

 # Parsing c-file: get data from class description, op description, event description
  def c_file_data_get(self, filename):

    f = open(filename, 'r')
    allfile = f.read()
    f.close()

    current_class = ""
    func_pos = 0

    #looking for EO_DEFINE_CLASS in all file to get _class_get function and parents
    static_class = False
    pos_start = allfile.find(const.EO_DEFINE_CLASS_STATIC, func_pos)
    if pos_start != -1:
      static_class = True

    if not static_class:
      pos_start = allfile.find(const.EO_DEFINE_CLASS, func_pos)
      if pos_start == -1:
      #verbose_print("Warning: %s wasn't found in %s"%(self.string_consts["class_new_func"], filename))
        return

    # splitting EO_DEFINE_CLASS macro
    d = self.find_token_in_brackets(allfile, pos_start, "()")
    d = d.replace(" ","")
    d = d.replace("\n", "")
    lst = d.split(",")
    current_class = lst[0]
    if static_class:
      lst = lst[3:-1]
    else:
      lst = lst[2:-1]

    lst = filter(lambda l: False if l == "NULL" else True, lst)
    if current_class in self.cl_data:
      verbose_print("Class %s from file %s won't be added in the tree"%(current_class, filename))
      verbose_print("Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class][const.C_FILE]))
      return
    self.cl_data[current_class] = {const.PARENTS:lst,
                                   const.C_FILE:filename,
                                   const.FUNCS:{}}
    #FIXME: need to fetch foolowing parameters according to data in EO_DEFINE_CLASS
    #feching class description, event_desc, and op_desc.
    for l in self.key_words:
      pos_start = allfile.find(l)

      if pos_start == -1:
        #verbose_print("Warning: \"%s\" wasn't found in %s"%(l, filename))
        continue
      else:
        tmp =self.find_token_in_brackets(allfile, pos_start, "{}")
        tmp = tmp.replace("\t", "")
        tmp = tmp.replace("\n", "")
        self.cl_data[current_class][l] = tmp

    #parsing class_description
    self.parse_cl_desc(current_class)
    #parsing event_desc
    self.parse_ev_desc(current_class)
    #parsing op_desc
    self.parse_op_desc(current_class)



  #parsing Eo_Op_Description:
  #generating function name and mapping it to id
  #op_id structure
  #{
  #   EO_OP_FUNC(EO_BASE_ID(EO_BASE_SUB_ID_CONSTRUCTOR), _constructor),
  #   EO_OP_FUNC(EO_BASE_ID(EO_BASE_SUB_ID_DESTRUCTOR), _destructor),
  #   EO_OP_FUNC(EVAS_OBJ_LINE_ID(EVAS_OBJ_LINE_SUB_ID_XY_SET), _line_xy_set),
  #   EO_OP_FUNC(EVAS_OBJ_LINE_ID(EVAS_OBJ_LINE_SUB_ID_XY_GET), _line_xy_get),
  #   EO_OP_FUNC_SENTINEL
  #}
  def parse_op_desc(self, cl_id):
    if self.op_desc not in self.cl_data[cl_id]:
        return

    in_data = self.cl_data[cl_id][self.op_desc]

    key_end = const.EO_OP_DESCRIPTION_SENTINEL #"EOBJ_OP_DESCRIPTION_SENTINEL"
    pos = in_data.find(key_end)
    if pos == -1:
      print "Warning: %s wasn't found in the end of Eo_Op_Description"%(key_end)
      exit(1)
    in_data = in_data[:pos]

    key_str = const.EO_OP_DESCRIPTION#"EOBJ_OP_DESCRIPTION"

    pos = in_data.find(key_str)
    lst = []
    while pos != -1:
      s = self.find_token_in_brackets(in_data, pos, "()")
      s = s.split(",")
      op_id = s[0].strip(" ")
      sub_id_str = const.SUB_ID
      func_name = op_id[op_id.find(sub_id_str)+len(sub_id_str):].lower()
      lst.append((op_id, func_name))

      self.cl_data[cl_id][const.FUNCS][func_name] = {const.OP_ID : op_id, const.C_MACRO: ""}
      pos = in_data.find(key_str, pos + 1)

    self.cl_data[cl_id][self.op_desc] = lst
    #self.cl_data[cl_id].pop(self.op_desc)

  #  resolving parameters's types and names according to
  #  #define, @def and op_ids
  def parse_op_func_params(self, cl_id):
    if const.OP_DESC not in self.cl_data[cl_id]:
       print "Not found: %s"%const.OP_DESC
       exit()
       return

    op_desc = self.cl_data[cl_id][const.OP_DESC]
    defines = self.cl_data[cl_id][const.DEFINES]
    macros = self.cl_data[cl_id][const.OP_MACROS]


    #looking for op_id in define; if found, cutting op_macro from define
    #and checking if it is in macros list. If not - we forgot to add comment
    #if yes - cutting types from define
    for op, f in op_desc:
       for d in defines:
         pos = d.find(op)
         if pos != -1 and d[pos : d.find(")", pos)] == op:
           s_tmp = d[d.find(' ') + 1:]
           s_tmp = s_tmp.replace(" ", "")
           s_tmp = s_tmp.split('(')[0]
           if s_tmp not in macros:
              print "Warning: no comments for \"%s\"; file: \"%s\" "%(s_tmp, self.cl_data[cl_id][const.H_FILE])
           else:

             params = []
             params_direction =  macros[s_tmp]
             pos = d.find(const.EO_TYPECHECK, pos)
             i = 0
             while pos != -1:
                tok = self.find_token_in_brackets(d, pos, "()")
                lst = tok.split(',')
                lst[0] = lst[0].replace("const", "")
                lst[0] = " ".join(lst[0].split())
                lst[0] = lst[0].replace(" *", "*")
                lst[1] = lst[1].replace(" ", "")
                if len(lst) == 2:
                   try:
                     tok =  ",".join(list(params_direction[i]))
                     params.append((lst[1], lst[0], tok))
                   except IndexError:
                     print "Warning: error in description %s in  %s"%(s_tmp,self.cl_data[cl_id][const.H_FILE])

                else:
                   print "ERROR: check parameters in EO_TYPECHECK"
                   exit(1)

                pos += len(const.EO_TYPECHECK)
                pos = d.find(const.EO_TYPECHECK, pos)

                i += 1

             self.cl_data[cl_id][const.FUNCS][f][const.PARAMETERS] = params
             self.cl_data[cl_id][const.FUNCS][f][const.C_MACRO] = s_tmp



  #fetching event ids
  #
  #event_desc structure
  # { EV_CLICKED, EV_BUTTON_DOWN, EV_BUTTON_UP, NULL  }
  #
  def parse_ev_desc(self, cl_id):
    if self.ev_desc not in self.cl_data[cl_id]:
        return

    in_data = self.cl_data[cl_id][self.ev_desc]
    in_data = in_data.replace(" ","")

    lst = in_data.split(',')
    if lst[-1] != "NULL":
      print "ERROR: last event descriptor should be NULL in class %s"%(cl_id)
      exit(1)

    lst.pop(-1)
    self.cl_data[cl_id][self.ev_desc] = lst
    #self.cl_data[cl_id].pop(self.ev_desc)



#parsing Eo_Class_Description
  def parse_cl_desc(self, cl_id):
    if self.cl_desc not in self.cl_data[cl_id]:
      return

    in_data = self.cl_data[cl_id][self.cl_desc]
    #splitting class desc
    lst = smart_split(in_data)

    lst_tmp = []
    for l in lst:
       lst_tmp.append(l.strip(" ").strip("\""))
    lst = lst_tmp
    del lst_tmp

    #self.cl_data[cl_id][self.cl_desc] = lst
    self.cl_data[cl_id].pop(self.cl_desc)

    ###
    # Class desc structure:
    # {
    #[0]    EO_VERSION
    #[1]    "Evas_Object_Line",
    #[2]    EO_CLASS_TYPE_REGULAR,
    #[3]    EO_CLASS_DESCRIPTION_OPS(&EVAS_OBJ_LINE_BASE_ID, op_desc, EVAS_OBJ_LINE_SUB_ID_LAST),
    #[4]    NULL,
    #[5]    sizeof(Evas_Object_Line),
    #[6]    _class_constructor,
    #[7]    NULL
    # }
    #

    lst.pop(0) #throwing out version

    cl_name = lst[0]
    self.cl_data[cl_id][const.C_NAME] = cl_name

    self.cl_data[cl_id][const.MODULE] = normalize_names([cl_name])[0].lower()
    self.cl_data[cl_id][const.TYPE] = lst[1]
    self.cl_data[cl_id][const.CLASS_CONSTRUCTOR] = lst[5]

    class_desc_ops = lst[2]
    pos = class_desc_ops.find(const.CLASS_DESC_OPS)
    if pos != -1:
      s = self.find_token_in_brackets(class_desc_ops, pos, "()")
      s = s.split(',')[0]
      s = s.strip("& ")
      if s == "NULL" and cl_name == "Eo Base":
#FIXME: hardcoded EO_BASE_BASE_ID
        print cl_name, "Warning: hardcoded EO_BASE_BASE_ID"
        s = "EO_BASE_BASE_ID"
      self.cl_data[cl_id][const.BASE_ID] = s





  #generating XML
  def build_xml(self, cl_id):
    #FIXME: because i don't parse several EO_DEFINE_CLASS in file
    #if const.C_NAME not in self.cl_data[cl_id]:
     # return
    self.cl_data[cl_id][const.XML_FILE] = os.path.join(self.outdir, normalize_names([self.cl_data[cl_id][const.C_NAME]])[0] + ".xml")

    cl_data = self.cl_data[cl_id]

    module = Element(const.MODULE)
    module.set(const.NAME, cl_data[const.C_NAME])
    SubElement(module, const.INCLUDE, {const.NAME: os.path.split(cl_data[const.H_FILE])[1]})

    cl_parent = ""
    cl_brothers = []
    for i, l in enumerate(cl_data[const.PARENTS]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit(1)
      if i == 0:
        cl_parent = tmp[l][const.C_NAME]
      else:
        cl_brothers.append(tmp[l][const.C_NAME])

    SubElement(module, const.EXTERN_FUNCTION, {const.NAME:cl_data[const.GET_FUNCTION]+"()",
                                           const.TYPENAME:"Eo_Class*"})

    cl_brothers = ",".join(cl_brothers)

    instantiateable = "False"
    if cl_data[const.TYPE] == const.CLASS_TYPE_REGULAR:
      instantiateable = "True"
    cl = SubElement(module, const.CLASS, {
                                      const.C_NAME : cl_data[const.C_NAME],
                                      const.PARENT:cl_parent,
                                      const.EXTENSIONS:cl_brothers,
                                      const.MACRO:cl_id,
                                      const.GET_FUNCTION: cl_data[const.GET_FUNCTION],
                                      const.TYPE : cl_data[const.TYPE],
                                      const.INSTANTIATEABLE : instantiateable})

    op_tag = SubElement(cl, const.OP_ID)
    ev_tag = SubElement(cl, const.EVENTS)
    m_tag = SubElement(cl, const.METHODS)

    if cl_data[const.BASE_ID] != "NULL":
      SubElement(op_tag, const.BASE_ID, {const.NAME:cl_data[const.BASE_ID]})

    for k in cl_data[const.FUNCS]:
        SubElement(op_tag, const.XML_SUB_ID, {const.NAME:cl_data[const.FUNCS][k][const.OP_ID]})


        m = SubElement(m_tag, const.METHOD, {const.NAME : k,
                                      const.OP_ID:cl_data[const.FUNCS][k][const.OP_ID],
                                      const.C_MACRO:cl_data[const.FUNCS][k][const.C_MACRO]})

        #defining parameter type
        if const.PARAMETERS in cl_data[const.FUNCS][k]:
          params = cl_data[const.FUNCS][k][const.PARAMETERS]
          for v, t, d in params:
             p = SubElement(m, const.PARAMETER, {const.NAME:v, const.C_TYPENAME:t, const.PRIMARY_TYPE : self.typedef_resolve(t),const.DIRECTION:d})


    if self.ev_desc in cl_data:
      lst = cl_data[self.ev_desc]
      for l in lst:
         SubElement(ev_tag, const.EVENT,{const.NAME:l})

    res = tostring(module, "utf-8")
    res = minidom.parseString(res)
    res = res.toprettyxml(indent="  ")

    (h, t) = os.path.split(self.cl_data[cl_id][const.XML_FILE])
    if not os.path.isdir(h):
      os.makedirs(h)
    f = open (self.cl_data[cl_id][const.XML_FILE], 'w')
    f.write(res)
    f.close()

  #parsing header file
  def h_file_data_get(self, filename):
    f = open (filename, 'r')
    allfile = f.read()
    f.close()

   #fetch all "#define" from file
    pos = pos_d = allfile.find("#define")
    def_list = []
    while pos != -1:
       pos_end = allfile.find("\n", pos)
       pos_end2 = allfile.find("\\", pos)
       if pos_end < pos_end2 or pos_end2 == -1:
         s = allfile[pos_d:pos_end]
         s = s.replace("\n", "")
         s = s.replace("\\", "")
         s = " ".join(s.split())
         def_list.append(s)
         pos = pos_d = allfile.find("#define", pos_end)
       else:
          pos = pos_end + 1
          continue

   #fetch all data from "@def" comments
    macro = {}
    pos = allfile.find("@def")
    while pos != -1:
      pos_start = pos
      pos_end = allfile.find("*/", pos_start)
      if pos_end != -1:
        tmp = allfile[pos_start : pos_end]
        #tmp = tmp.replace("\n", "") #deleting next string
        tmp = tmp.replace("*", "") #removing *
        lst = tmp.split("\n")

        lst = filter(macro_filter_func, lst)

        for i in range(len(lst)):
          lst[i] = " ".join(lst[i].split()) #removing more than one spaces


        macro_name = lst[0]
        par_lst = []
        macro_name = macro_name.split("(")[0]

        macro_name = macro_name[macro_name.find(" ")+1:].strip(" ")
        for l in lst:
          if l.startswith("@param"):
             s = self.find_token_in_brackets(l, 0, "[]")
             s = s.replace(" ", "")
             s_tmp = []
             if s != "":
                s = s.split(",")
                if "in" in s:
                   s_tmp.append("in")
                if "out" in s:
                   s_tmp.append("out")
             else:
                s_tmp.append("in")
                s_tmp.append("out")
             t = tuple(s_tmp)
             if len(t) == 0:
                print "ERROR: check parameter's description in #define %s"%(macro_name)
                exit(1)
             par_lst.append(t)

      macro[macro_name] = par_lst

      pos = allfile.find("@def", pos_end)


    #looking for class_get function to get class macro
    current_class = ""
    cl_macro = []
    cl_id_copy = []

    for k in self.cl_data:
      pos = 0
      get_func = ""

      for d in def_list:

        pos = d.find(k)
        reg = '#define[ ]*[a-zA-Z_]*[ ]*%s\(\)'%k

        res = re.findall(reg, d)
        if re.match(reg, d):
          lst = d.split()
          current_class = lst[1]
          get_func = k
          cl_macro.append((get_func, current_class))

          if current_class in self.cl_data:
            verbose_print("Class %s from file %s won't be added in the tree"%(current_class, filename))
            verbose_print("Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class][const.H_FILE]))
            return

    if current_class == "":
      return

    for gf, cl_id in cl_macro:
      self.cl_data[cl_id] = self.cl_data[gf]
      self.cl_data.pop(gf)
      self.cl_data[cl_id][const.GET_FUNCTION] = gf
      self.cl_data[cl_id][const.H_FILE] = filename
      self.cl_data[cl_id][const.DEFINES] = def_list
      self.cl_data[cl_id][const.OP_MACROS] = macro

  #Returns token from first found bracket to closing bracket
  #not including brackets
  def find_token_in_brackets(self, data, pos, brackets):

    if brackets == "{}" or  brackets == "()" or brackets == "[]":
        pos_end = pos_start = data.find(brackets[0], pos)
        if pos_end == -1:
          return ""

        brackets_count = 1
        while brackets_count != 0:
          pos_end += 1
          if data[pos_end] == brackets[0]:
            brackets_count += 1
          elif data[pos_end] == brackets[1]:
            brackets_count -= 1

        res = data[pos_start:pos_end + 1]
        res = res.strip(brackets)
        return res

    else:
      print "ERROR: brackets should be {} or () or []"
      exit(1)


  #print out data from each class in parser object
  def print_data(self):
    for klass in self.cl_data:
      print ""
      print klass
      for kk in self.cl_data[klass]:
        print "  ", kk, " : ", type(self.cl_data[klass][kk])# " : ", cp.cl_data[klass][kk]
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

  #set internal variable for outdir
  def outdir_set(self, _d):
    self.outdir = _d


# smart_split(tmp)
#
# tmp - string to split
# Splits string with delimeter ',', but doesn't split data in brackets
#
# Returns list of tokens
#

def smart_split(tmp):
  bracket = 0
  pos_start = 0
  l = []
  for i in range(len(tmp)):
    if tmp[i] == ',' and bracket == 0:
      l.append(tmp[pos_start:i])
      pos_start = i + 1
    elif tmp[i] == '(':
      bracket += 1
    elif tmp[i] == ')':
      bracket -= 1
  l.append(tmp[pos_start : ])

  return l

