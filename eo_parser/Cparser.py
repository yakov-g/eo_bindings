import xml.parsers.expat
import sys, os

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from string import capwords
from helper import normalize_names



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

    self.string_consts = {"class_type_mixin" : "EO_CLASS_TYPE_MIXIN",
                          "class_type_regular" : "EO_CLASS_TYPE_REGULAR",
                          "class_desc_ops" : "EO_CLASS_DESCRIPTION_OPS",
                          "class_new_func" : "EO_DEFINE_CLASS",
                          "class_new_func_static" : "EO_DEFINE_CLASS_STATIC",
                          "op_desc" : "EO_OP_DESCRIPTION",
                          "op_desc_sent" : "EO_OP_DESCRIPTION_SENTINEL",
                          "sub_id" : "SUB_ID_",
                          "typecheck" : "EO_TYPECHECK"
                          }

    self.op_desc = "Eo_Op_Description op_desc"
    self.ev_desc = "Eo_Event_Description *event_desc"
    self.cl_desc = "Eo_Class_Description class_desc"
    self.op_func_desc = "Eo_Op_Func_Description func_desc"
    self.key_words = [self.op_desc, self.ev_desc, self.cl_desc, self.op_func_desc]
    self.prefixex = {"@class" : ""}

    self.globals = {}
    self.globals["strip_string"] = "()"
    self.globals["outdir"] = os.path.abspath(os.curdir)


  #parsing c file
  def parse_description(self, filename):

    f = open(filename, 'r')
    allfile = f.read()
    f.close()

    #looking for class_get function in *.c file to find proper file for class
    current_class = ""
    func_pos = 0

#looking for EO_DEFINE_CLASS in all file to get _class_get function
#and parents

    static_class = False
    pos_start = allfile.find(self.string_consts["class_new_func_static"], func_pos)
    if pos_start != -1:
      static_class = True

    if not static_class:
      pos_start = allfile.find(self.string_consts["class_new_func"], func_pos)
      if pos_start == -1:
      #verbose_print("Warning: %s wasn't found in %s"%(self.string_consts["class_new_func"], filename))
        return

    d = self.find_token_in_brackets(allfile, pos_start, "()")
    d = self.strip_replace(d, "() ")
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
      verbose_print("Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class]["c_file"]))
      return
    self.cl_data[current_class] = {"parents":lst,
                                   "c_file":filename,
                                   "funcs":{}}

    for l in self.key_words:
      pos_start = allfile.find(l)

      if pos_start == -1:
        #verbose_print("Warning: \"%s\" wasn't found in %s"%(l, filename))
        continue
      else:
        tmp =self.find_token_in_brackets(allfile, pos_start, "{}")
        tmp = tmp.replace("\t", "")
        tmp = tmp.replace("\n", "")
        tmp = tmp.strip("{}")
        self.cl_data[current_class][l] = tmp

    #parsing class_description
    self.parse_cl_desc(current_class)
    #parsing event_desc
    self.parse_ev_desc(current_class)
    #parsing op_desc
    self.parse_op_desc(current_class)


#parsing Eo_Op_Description
  def parse_op_desc(self, cl_id):
    if self.op_desc not in self.cl_data[cl_id]:
        return

    in_data = self.cl_data[cl_id][self.op_desc]

    key_end = self.string_consts["op_desc_sent"] #"EOBJ_OP_DESCRIPTION_SENTINEL"
    pos = in_data.find(key_end)
    if pos == -1:
      print "Warning: %s wasn't found in the end of Eo_Op_Description"%(key_end)
      exit(1)
    in_data = in_data[:pos]

    key_str = self.string_consts["op_desc"]#"EOBJ_OP_DESCRIPTION"

    pos = in_data.find(key_str)
    lst = []
    while pos != -1:
      s = self.find_token_in_brackets(in_data, pos, "()")
      s = s.strip("() ")
      s = s.split(",")
      op_id = s[0].strip(" ")
      sub_id_str = self.string_consts["sub_id"]
      func_name = op_id[op_id.find(sub_id_str)+len(sub_id_str):].lower()
      lst.append((op_id, func_name))

      self.cl_data[cl_id]["funcs"][func_name] = {"op_id" : op_id, "c_macro" : ""}
      pos = in_data.find(key_str, pos + 1)

    self.cl_data[cl_id][self.op_desc] = lst

#looking for parameters types in *.h
  def parse_op_func_params(self, cl_id):
    if self.op_desc not in self.cl_data[cl_id]:
       return

    op_desc = self.cl_data[cl_id][self.op_desc]
    defines = self.cl_data[cl_id]["defines"]
    macros = self.cl_data[cl_id]["macro"]


    for l in defines:
       s = l

       for key in macros:
          pos = s.find("#define " + key)
          if pos == -1:
            continue

          s_tmp = s[s.find(' ') + 1:]
          s_tmp = s_tmp.replace(" ", "")
          s_tmp = s_tmp.split('(')[0]
          if key == s_tmp:
#          if pos != -1:
             for op_id, f in op_desc:
               pos = s.find(op_id)
               if pos != -1 and s[pos : s.find(")", pos)] == op_id:

                  params = []
                  params_direction =  macros[key]
                  pos = s.find(self.string_consts["typecheck"], pos)
                  i = 0
                  while pos != -1:
                     d = self.find_token_in_brackets(s, pos, "()")
                     d = d.strip("()")
                     lst = d.split(',')
                     lst[0] = lst[0].replace("const", "")
                     lst[0] = " ".join(lst[0].split())
                     lst[0] = lst[0].replace(" *", "*")
                     lst[1] = lst[1].replace(" ", "")
                     if len(lst) == 2:
                        try:
                          d =  ",".join(list(params_direction[i]))
                          params.append((lst[1], lst[0], d))
                        except IndexError:
                          print "Warning: error in description %s in  %s"%(key,self.cl_data[cl_id]["h_file"])

                     else:
                        print "ERROR: check parameters in EO_TYPECHECK"
                        exit(1)

                     pos += len(self.string_consts["typecheck"])
                     pos = s.find(self.string_consts["typecheck"], pos)

                     i += 1

                  self.cl_data[cl_id]["funcs"][f]["params"] = params
                  self.cl_data[cl_id]["funcs"][f]["c_macro"] = key

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

#parsing Eo_Class_Description
  def parse_cl_desc(self, cl_id):
    if self.cl_desc not in self.cl_data[cl_id]:
      return

    in_data = self.cl_data[cl_id][self.cl_desc]
    lst = smart_split(in_data)

    lst_tmp = []
    for l in lst:
       lst_tmp.append(l.strip(" ").strip("\""))

    lst = lst_tmp

    self.cl_data[cl_id][self.cl_desc] = lst

    cl_name = lst[0]
    self.cl_data[cl_id]["c_name"] = cl_name
    self.cl_data[cl_id]["module"] = normalize_names(cl_name).lower()
    self.cl_data[cl_id]["type"] = lst[1]
#    self.cl_data[cl_id]["constructor"] = lst[5]
 #   self.cl_data[cl_id]["destructor"] = lst[6]
    self.cl_data[cl_id]["class_constructor"] = lst[5]

    class_desc_ops = lst[2]
    pos = class_desc_ops.find(self.string_consts["class_desc_ops"])
    if pos != -1:
      s = self.find_token_in_brackets(class_desc_ops, pos, "()")
      s = s.strip("()")
      s = s.split(',')[0]
      s = s.strip("& ")
      if s == "NULL" and cl_name == "Eo Base":
#FIXME: hardcoded EO_BASE_BASE_ID
        print cl_name, "Warning: hardcoded EO_BASE_BASE_ID"
        s = "EO_BASE_BASE_ID"
      self.cl_data[cl_id]["base_id"] = s


  def build_xml2(self, cl_id):
    self.cl_data[cl_id]["xml_file"] = os.path.join(self.globals["outdir"], self.cl_data[cl_id]["module"] + ".xml")

    cl_data = self.cl_data[cl_id]

    module = Element('module')
    module.set('name', cl_data["c_name"])
    SubElement(module, "include", {"name": os.path.split(cl_data["h_file"])[1]})


    cl_parent = ""
    cl_brothers = []
    for i, l in enumerate(cl_data["parents"]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit(1)
      if i == 0:
        cl_parent = tmp[l]["c_name"]
      else:
        cl_brothers.append(tmp[l]["c_name"])


    SubElement(module, "extern_function", {"name":cl_data["get_function"]+"()",
                                           "typename":"Eo_Class*"})


    cl_brothers = ",".join(cl_brothers)

    instantiateable = "False"
    if cl_data["type"] == self.string_consts["class_type_regular"]:
      instantiateable = "True"
    cl = SubElement(module, "class", {#"name":cl_data["name"],
                                      "c_name" : cl_data["c_name"],
                                      "parent":cl_parent,
                                      "extensions":cl_brothers,
                                      "macro":cl_id,
                                      "get_function": cl_data["get_function"],
                                      "type" : cl_data["type"],
                                      "instantiateable" : instantiateable})

    op_tag = SubElement(cl, "op_id")
    ev_tag = SubElement(cl, "events")
    m_tag = SubElement(cl, "methods")


    if cl_data["base_id"] != "NULL":
      SubElement(op_tag, "base_id", {"name":cl_data["base_id"]})

    for k in cl_data["funcs"]:
        SubElement(op_tag, "sub_id", {"name":cl_data["funcs"][k]["op_id"]})


        m = SubElement(m_tag, "method", {"name" : k,
                                      "op_id":cl_data["funcs"][k]["op_id"],
                                      "c_macro":cl_data["funcs"][k]["c_macro"]})

        #defining parameter type
        if "params" in cl_data["funcs"][k]:
          params = cl_data["funcs"][k]["params"]
          for v, t, d in params:
             p = SubElement(m, "parameter", {"name":v,
                                            "c_typename":t,
                                            "direction":d})


    if self.ev_desc in cl_data:
      lst = cl_data[self.ev_desc]
      for l in lst:
         SubElement(ev_tag, "event",{"name":l})

    #inserting signals into XML
    """
    if self.ev_desc in cl_data:
      lst = cl_data[self.ev_desc]
      for l in lst:
         SubElement(cl, "signal",{"name":"callback_"+l.lower()+"_add",
                                  "op_id":l})
         SubElement(cl, "signal",{"name":"callback_"+l.lower()+"_del",
                                  "op_id":l})
    """

    res = tostring(module, "utf-8")
    res = minidom.parseString(res)
    res = res.toprettyxml(indent="  ")

    (h, t) = os.path.split(self.cl_data[cl_id]["xml_file"])
    if not os.path.isdir(h):
      os.makedirs(h)
    f = open (self.cl_data[cl_id]["xml_file"], 'w')
    f.write(res)
    f.close()

  #parsing header file
  def parse_prefixes(self, filename):
    f = open (filename, 'r')
    allfile = f.read()
    f.close()

   #list of #define strings
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

####################################################################
    #looking for all function macros in *.h
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

        """
        lst = tmp.split("@")
        lst = filter(None, lst) #remove empty strings
        print lst
        print 


        for i in range(len(lst)):
          lst[i] = lst[i].strip(" ")
        """

        macro_name = lst[0]
        par_lst = []
        macro_name = macro_name.split("(")[0]
        if True:
          macro_name = macro_name[macro_name.find(" ")+1:].strip(" ")
          for l in lst:
            if l.startswith("@param"):
               s = self.find_token_in_brackets(l, 0, "[]")
               s = s.strip("[]").replace(" ", "")
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
        else:
          pos = allfile.find("@def", pos_end)
          continue

        macro[macro_name] = par_lst

      pos = allfile.find("@def", pos_end)
 #####################################################################


####################################
    #looking for class_get function
    current_class = ""
    cl_macro = []

    for k in self.cl_data:
      pos = 0
      get_func = ""

      for d in def_list:

        pos = d.find(k)
        if pos != -1:
          lst = d.split()
          current_class = lst[1]
          get_func = k
          cl_macro.append((get_func, current_class))

          if current_class in self.cl_data:
            verbose_print("Class %s from file %s won't be added in the tree"%(current_class, filename))
            verbose_print("Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class]["h_file"]))
            return

    if current_class == "":
      return

    for gf, cl_id in cl_macro:
      self.cl_data[cl_id] = self.cl_data[gf]
      self.cl_data.pop(gf)
      self.cl_data[cl_id]["get_function"] = gf
      self.cl_data[cl_id]["h_file"] = filename
      self.cl_data[cl_id]["defines"] = def_list
      self.cl_data[cl_id]["macro"] = macro


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

        return data[pos_start:pos_end + 1]

    else:
      print "ERROR: brackets should be {} or () or []"
      exit(1)

  def strip_replace(self, data, s):
    data = data.strip(s)
    data = data.replace(" ", "")
    return data

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


  def outdir_set(self, _d):
    self.globals["outdir"] = _d

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

