import os
from string import capwords

class _const:
  class ConstError(TypeError): pass
  def __setattr__(self,name,value):
    if self.__dict__.has_key(name):
#       raise self.ConstError("Can't rebind const(%s)"%name)
      print "Can't rebind const: \"%s\""%name
      return
    self.__dict__[name]=value
  def __init__(self):
    self.C_NAME = "c_name" #check after changing in XML
    self.MODULE = "module" #check after cnaaging in XML
    self.TYPE = "type"
    self.CLASS_CONSTRUCTOR = "class_constructor"
    self.BASE_ID = "base_id"
    self.FUNCS = "funcs"
    self.FUNCS_PARAMS = "params"
    self.FUNCS_OP_MACRO = "c_macro"
    self.FUNCS_OP_ID = "op_id"

    self.GET_FUNCTION = "get_function"
    self.DEFINES = "defines"
    self.PARENTS = "parents"
    self.H_FILE = "h_file"
    self.C_FILE = "c_file"
    self.XML_FILE = "xml_file"
    self.MACRO = "macro"  #EO_CLASS
    self.OP_MACROS = "op_macros" #dict of macros from @def with parameters

    self.CLASS_TYPE_MIXIN =  "EO_CLASS_TYPE_MIXIN"
    self.CLASS_TYPE_REGULAR = "EO_CLASS_TYPE_REGULAR"
    self.CLASS_DESC_OPS = "EO_CLASS_DESCRIPTION_OPS"
    self.EO_DEFINE_CLASS = "EO_DEFINE_CLASS"
    self.EO_DEFINE_CLASS_STATIC =  "EO_DEFINE_CLASS_STATIC"
    self.EO_OP_DESCRIPTION =  "EO_OP_DESCRIPTION"
    self.EO_OP_DESCRIPTION_SENTINEL = "EO_OP_DESCRIPTION_SENTINEL"
    self.SUB_ID = "SUB_ID_"
    self.EO_TYPECHECK = "EO_TYPECHECK"

    self.SET_ONLY = 0
    self.GET_ONLY = 1
    self.SET_GET = 2
#    self.GET_SET = 3
    self.METHOD = 4



#FIXME: filename cpp, hpp,....
def isC(s):
  if s[-2:] == ".c" and s.find("eo.c") == -1:
    return True
  else:
    return False

def isH(s):
  if s[-2:] == ".h":
    return True
  else:
    return False

def isXML(s):
  if s[-4:] == ".xml":
    return True
  else:
    return False

#  dir_files_get(_directories, func, recursive)
#
#  _directories - input list of dirs,
#  recursive - recursive lookup or not
#
#  Recursively(if True) walks through directories.
#  Builds abs path for files.
#
#  Returns list of absolute paths

def dir_files_get(_directories, recursive = True):
  res = []
  if recursive:
    for d in _directories:
      for root, dirs, files in os.walk(d):
        tmp = []
        for f in files:
          tmp.append(os.path.join(root,f))
        res += tmp
  else:
    for d in _directories:
      tmp = []
      for f in os.listdir(d):
        tmp.append(os.path.join(d, f))
      res += tmp

  res = list(set(res))
  return res


#  abs_path_get(_paths)
#
#  _paths - list of dirs or files
#  _warning - boolean; exit if path doesn't exist
#
#  Builds abs path and checks if it exists for each path in list.
#
#  Returns list of abs paths
#
def abs_path_get(_paths, _warning = True):
   if type(_paths) == list:
     res = []
     lst = list(set(_paths)) #remove multiple items from list
     for d in lst:
       path_tmp = d
       path_tmp = os.path.expanduser(path_tmp)
       path_tmp = os.path.abspath(path_tmp)
       if os.path.exists(path_tmp):
         res.append(path_tmp)
       else:
         if _warning:
           print "ERROR: path %s doesn't exist... Aborting..."%path_tmp
           exit(1)
     return res


#FIXME: pass only list as parameter

#  normalize_names(_lst)
#
#  _lst - list of class names
#
#  Normalizes class names like following:
#  Some_class name --> SomeClassName
#
#  Returns list of normalized names
#
def normalize_names(_lst):
   res = []
   if type(_lst) is str:
     print "Need to change string type to list in normalize_names"
     print _lst[1000]
   for l in _lst:
     l = l.replace("-"," ")
     l = l.replace("_"," ")
     l = capwords(l)
     l = "".join(l.split())
     res.append(l)
   return res

