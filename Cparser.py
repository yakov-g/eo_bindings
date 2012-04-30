import xml.parsers.expat
import sys, os

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

class Cparser(object):
  def __init__(self):
    self.cl_data = {}
    self.cl_incl = {}
    self.types = {"Evas_Coord" : "int", "Evas_Angle":"int",
                  "Evas_Font_Size" : "int", "Eina_Bool" : "unsigned char",
                  "Eobj":"EobjDefault", "void**":"void*"}


    self.string_consts = {"class_type_mixin" : "EOBJ_CLASS_TYPE_MIXIN",
                          "class_type_regular" : "EOBJ_CLASS_TYPE_REGULAR",
                          "class_desc_ops" : "EOBJ_CLASS_DESCRIPTION_OPS",
                          "class_new_func" : "EOBJ_DEFINE_CLASS",
                          "op_desc" : "EOBJ_OP_DESCRIPTION",
                          "op_desc_sent" : "EOBJ_OP_DESCRIPTION_SENTINEL",
                          "sub_id" : "SUB_ID_",
                          "typecheck" : "EOBJ_TYPECHECK"
                          }

    self.op_desc = "Eobj_Op_Description op_desc"
    self.ev_desc = "Eobj_Event_Description *event_desc"
    self.cl_desc = "Eobj_Class_Description class_desc"
    self.op_func_desc = "Eobj_Op_Func_Description func_desc"
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
    """
    for k in self.cl_data:
      f = self.cl_data[k]["get_function"]
      func_pos = allfile.find(f)
      if func_pos != -1:
        current_class = k
        self.cl_data[current_class]["c_file"] = filename
        break
    
    #this file doesn't have any class
    if current_class == "":
      return
    """

#looking for EOBJ_DEFINE_CLASS in all file to get _class_get function
#and parents
    pos_start = allfile.find(self.string_consts["class_new_func"], func_pos)
    if pos_start == -1:
      print "ERROR: %s wasn't found in %s"%(self.string_consts["class_new_func"], filename)
      return

     # print "ERROR: %s wasn't found in %s"%("eobj_class_new", self.globals["@class"]["get_function"])
     # exit()
    d = self.find_token_in_brackets(allfile, pos_start, "()")
    d = self.strip_replace(d, "() ")
    d = d.replace("\n", "")
    lst = d.split(",")
    current_class = lst[0]
    lst = lst[2:-1]

    if lst[0] == "NULL":
      lst[0] = "EOBJ_DEFAULT_CLASS"

    lst_tmp = []
    for l in lst:
      if l != "NULL":
        lst_tmp.append(l)
    lst = lst_tmp
   


    if current_class in self.cl_data:
      print "Class %s from file %s won't be added in the tree"%(current_class, filename)
      print "Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class]["c_file"])
      return
    self.cl_data[current_class] = {"parents":lst,
                                   "c_file":filename,
                                   "funcs":{}}
  
    for l in self.key_words:
      pos_start = allfile.find(l)

      if pos_start == -1:
        print "ERROR: \"%s\" wasn't found in %s"%(l, filename)
        continue
      
      else:
        tmp =self.find_token_in_brackets(allfile, pos_start, "{}")
        tmp = tmp.replace(" ", "")
        tmp = tmp.replace("\t", "")
        tmp = tmp.replace("\n", "")
        tmp = tmp.strip("{}")
        self.cl_data[current_class][l] = tmp

    #parsing class_description
    self.parse_cl_desc2(current_class)
    #parsing event_desc
    self.parse_ev_desc2(current_class)
    #parsing op_desc   
    self.parse_op_desc2(current_class)
#   self.parse_op_func_params2(current_class)


  def reorder_parents(self, cl_id):
    if len(self.cl_data[cl_id]["parents"]) == 0:
      return

    parent_l = []
    mixin_l = []
    other_l = []

    tmp_parents_list =  self.cl_data[cl_id]["parents"][:]
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

    self.cl_data[cl_id]["parents"] = lst
     

#parsing Eobj_Op_Description 
  def parse_op_desc2(self, cl_id):
    if self.op_desc not in self.cl_data[cl_id]:
        return

    in_data = self.cl_data[cl_id][self.op_desc]

    key_end = self.string_consts["op_desc_sent"] #"EOBJ_OP_DESCRIPTION_SENTINEL"
    pos = in_data.find(key_end)
    if pos == -1:
      print "ERROR: %s wasn't found in the end of Eobj_Op_Description"%(key_end)
      exit()
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
      
      self.cl_data[cl_id]["funcs"][func_name] = {"op_id" : op_id}
      pos = in_data.find(key_str, pos + 1)

    self.cl_data[cl_id][self.op_desc] = lst

#looking for parameters types in *.h
  def parse_op_func_params2(self, cl_id):
    #self.print_data()    
    if self.op_desc not in self.cl_data[cl_id]:
       return
    
    op_desc = self.cl_data[cl_id][self.op_desc]
    defines = self.cl_data[cl_id]["defines"]
    macros = self.cl_data[cl_id]["macro"]

    for l in defines:
       s = l

       for key in macros:
          #FIXME check if it's ok to use this #define
          
          pos = s.find("#define " + key)
          if pos != -1:
             for op_id, f in op_desc:
               pos = s.find(op_id)
               if pos != -1:
                  #print l, key , macros[key]
                  params = []

                  params_direction =  macros[key]
                  pos = s.find(self.string_consts["typecheck"], pos)
                  i = 0
                  while pos != -1:
                     d = self.find_token_in_brackets(s, pos, "()")
                     d = self.strip_replace(d, "() ")
                     lst = d.split(',')
                     lst[0] = lst[0].replace("const", "")
                     if len(lst) == 2:
                        #print i, params_direction
                        d =  ",".join(list(params_direction[i]))
                        params.append((lst[1], lst[0], d))
                     else:
                        print "ERROR: check parameters in EOBJ_TYPECHECK"
         
                     pos += len(self.string_consts["typecheck"])
                     pos = s.find(self.string_consts["typecheck"], pos)

                     self.cl_data[cl_id]["funcs"][f]["params"] = params
                     i += 1

             

  def parse_ev_desc2(self, cl_id):
    if self.ev_desc not in self.cl_data[cl_id]:
        return

    in_data = self.cl_data[cl_id][self.ev_desc]
    lst = in_data.split(',')
    if lst[-1] != "NULL":
      print "ERROR: last event descriptor should be NULL"
      exit()
        
    lst.pop(-1)
    self.cl_data[cl_id][self.ev_desc] = lst

#parsing Eobj_Class_Description
  def parse_cl_desc2(self, cl_id):
    if self.cl_desc not in self.cl_data[cl_id]:
      return 
    
    in_data = self.cl_data[cl_id][self.cl_desc]
    lst = smart_split(in_data)
    self.cl_data[cl_id][self.cl_desc] = lst

    cl_name = lst[0]
    cl_name = self.strip_replace(cl_name, "\" _")
    self.cl_data[cl_id]["name"] = cl_name
    self.cl_data[cl_id]["module"] = cl_name.lower()
    self.cl_data[cl_id]["type"] = lst[1]
    self.cl_data[cl_id]["constructor"] = lst[5]
    self.cl_data[cl_id]["destructor"] = lst[6]
    self.cl_data[cl_id]["class_constructor"] = lst[7]

    class_desc_ops = lst[2]
    pos = class_desc_ops.find(self.string_consts["class_desc_ops"])
    if pos != -1:
      s = self.find_token_in_brackets(class_desc_ops, pos, "()")
      s = s.strip("()")
      s = s.split(',')[0]
      s = s.strip("& ")
      self.cl_data[cl_id]["base_id"] = s
  

  def build_xml2(self, cl_id):
    self.cl_data[cl_id]["xml_file"] = os.path.join(self.globals["outdir"], self.cl_data[cl_id]["name"] + ".xml")
#    (h, t) = os.path.split(self.cl_data[cl_id]["h_file"])
#    self.cl_data[cl_id]["xml_file"] = os.path.join(h, "python_module", self.cl_data[cl_id]["name"] + ".xml")

    cl_data = self.cl_data[cl_id]

    module = Element('module')
    module.set('name', cl_data["module"])
    #FIXME
    SubElement(module, "basemodule", {"name": "eobjdefault"})
    SubElement(module, "include", {"name": cl_data["h_file"]})

    lst = []
    lst.append(cl_data["module"])
    lst.append("eobjdefault")

    for l in lst:
        SubElement(module, "cimport", {"name": l})


    cl_parent = None
    cl_brothers = []
    for i, l in enumerate(cl_data["parents"]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit
      if i == 0:
        cl_parent = tmp[l]["name"]
      else:
        cl_brothers.append(tmp[l]["name"])

      SubElement(module, "import", {"module" : tmp[l]["module"],
                                    "class" : tmp[l]["name"]})
    
    if cl_data["base_id"] != "NULL":   
      SubElement(module, "extern_base_id", {"name":cl_data["base_id"],
                                  "typename":"Eobj_Op"})
    
    en = SubElement(module, "enum")

    SubElement(module, "extern_function", {"name":cl_data["get_function"]+"()",
                                           "typename":"Eobj_Class*"})


    if self.ev_desc in cl_data:
      lst = cl_data[self.ev_desc]
      for l in lst:
         SubElement(module, "extern",{"name":l,
                                          "typename":"Eobj_Event_Description *"})
    """
    cl_parent = cl_data["parents"][0]
    cl_parent = self.cl_data[cl_parent]["name"]

    cl_brothers = cl_data["parents"][1:]
    tmp = []
    for l in cl_brothers:
      name = self.cl_data[l]["name"]
      tmp.append(name)
    """
    cl_brothers = ",".join(cl_brothers)

    instantiateable = "False"
    if cl_data["type"] == self.string_consts["class_type_regular"]:
      instantiateable = "True"
    cl = SubElement(module, "class", {"name":cl_data["name"],
                                      "parent":cl_parent,
                                      "brothers":cl_brothers,
                                      "macro":cl_id,        
                                      "get_function": cl_data["get_function"],
                                      "instantiateable" : instantiateable})
    
    for k in cl_data["funcs"]:
        SubElement(en, "extern", {"name":cl_data["funcs"][k]["op_id"],
                                  "typename":"enum"})

        m = SubElement(cl, "method", {"name" : k,
                                      "op_id":cl_data["funcs"][k]["op_id"]})

        #defining parameter type
        if "params" in cl_data["funcs"][k]:
          params = cl_data["funcs"][k]["params"]
          for v, t, d in params:
              t_tmp = t.strip(" ")
              for key in self.types:
                 if t_tmp.find(key) != -1:
                   #replacing typedef
                   t_tmp = t_tmp.replace(key, self.types[key])
              if t_tmp != "char*" and t_tmp != "void*":
                t_tmp = t_tmp.rstrip("*")
              p = SubElement(m, "parameter", {"name":v,
                                            "typename":t_tmp,
                                            "c_typename":t, 
                                            "direction":d})

    
    if self.ev_desc in cl_data:
      lst = cl_data[self.ev_desc]
      for l in lst:
         SubElement(cl, "signal",{"name":"callback_"+l.lower()+"_add",
                                  "op_id":l})
         SubElement(cl, "signal",{"name":"callback_"+l.lower()+"_del",
                                  "op_id":l})
         

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
  def parse_prefixes2(self, filename):
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

####################################
    """
   #parsing prefixes
    prefixes = {}
    for k in self.prefixex:  
      tmp = ""
      pos = allfile.find(k) 

      if pos != -1:
        tmp = allfile[pos:]
        lst = tmp.splitlines()
        tmp = lst[0]
        tmp = tmp.replace(k, "")
        tmp = tmp.lstrip(" ")
        pos = tmp.find(" ")
        if pos != -1:
          tmp = tmp[:pos]

        tmp = tmp.rstrip("\n\t")
        self.prefixex[k] = tmp
        prefixes[k] = tmp

      else:
        print "ERROR: No tag %s in file: %s"%(k, filename)
        return
    """

    #looking for class_get function
    current_class = ""
    for k in self.cl_data:
      pos = 0
      get_func = ""
      for d in def_list:
        pos = d.find(k)
        if pos != -1:
          lst = d.split()
          current_class = lst[1]
          get_func = k
          break
      if current_class != "":
        break
    if current_class == "":
      return

    #looking for all function macros in *.h
    macro = {}
    pos = allfile.find("@def")
    while pos != -1:
      pos_start = pos
      pos_end = allfile.find("*/", pos_start)
      if pos_end != -1:
        tmp = allfile[pos_start : pos_end]

        tmp = tmp.replace("\n", "") #deleting next string
        tmp = tmp.replace("*", "") #removing *
        tmp = " ".join(tmp.split()) #removing more than one spaces
        lst = tmp.split("@")
        lst = filter(None, lst) #remove empty strings
        for i in range(len(lst)):
          lst[i] = lst[i].strip(" ")
         
        macro_name = lst[0] 
        par_lst = []
        if macro_name.find("(") != -1:
          macro_name = macro_name[macro_name.find(" ")+1:macro_name.find("(")].strip(" ")

          for l in lst:
            if l[:5] == "param":
               s = l[5:].lstrip(" ")
               s_tmp = []
               if s[0] == "[":
                  s = self.find_token_in_brackets(s, 0, "[]")
                  s = s.strip("[]").replace(" ", "")
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
                  exit()
               par_lst.append(t)
        else:
          pos = allfile.find("@def", pos_end)
          continue
        
        macro[macro_name] = par_lst
         
      pos = allfile.find("@def", pos_end)
  
    if current_class in self.cl_data:
      print "Class %s from file %s won't be added in the tree"%(current_class, filename)
      print "Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class]["h_file"])
      return


    self.cl_data[current_class] = self.cl_data[get_func]
    self.cl_data.pop(get_func)
    self.cl_data[current_class]["get_function"] = get_func
    self.cl_data[current_class]["h_file"] = filename
    self.cl_data[current_class]["defines"] = def_list
    self.cl_data[current_class]["macro"] = macro

    self.cl_data["EOBJ_DEFAULT_CLASS"] = {"get_function":"eobj_base_class_get()",
                                       "name":"EobjDefault",
                                       "basemodule":"eobjdefault",
                                       "module":"eobjdefault",
                                       "parentmodule":"NULL",
                                       "type" : "EOBJ_CLASS_TYPE_REGULAR_NO_INSTANCE",
                                       "parents" : []}
                                               


  def find_token_in_brackets(self, data, pos, brackets):

    if brackets == "{}" or  brackets == "()" or brackets == "[]":
        pos_end = pos_start = data.find(brackets[0], pos)

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
      exit()

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



