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
    # most of constants are used as internal dict keys,
    # but some of them are also used as tags in XML
    # Changing this constans will only spoil the view of XML
    self.PREFIX = "eorepo" #used as xml-tag

    self.NAME = "name" #used as xml-tag
    self.C_NAME = "c_name" #used as xml-tag
    self.MODIFIER = "modifier" #used as xml-tag
    self.MODULE = "module" #used as xml-tag
    self.PARSE_VERSION = "parse_version" #used as xml-tag
    self.NUM = "num" #used as xml-tag
    self.VER_NUM = "1.0.1"
    self.TYPE = "type" #used as xml-tag
    self.CLASS_CONSTRUCTOR = "class_constructor"
    self.BASE_ID = "base_id"
    self.BASE_ID_MACRO = "base_id_macro"
    self.FUNCS = "funcs"
    self.PARAMETERS = "parameters"
    self.OP_ID = "op_id"
    self.EVENT_ID = "event_id"
    self.EVENT_NAME = "event_name"

    self.OP_DESC = "op_desccc"
    self.EV_DESC = "ev_desccc"
    self.EVENT_DICT = "event_dict"
    self.IMPL_DESC = "implements_desc"
    self.SIG_DESC = "signal_desc"
    self.RETURN_TYPE = "return_type"
    self.LEGACY_NAME = "legacy"

    self.GET_FUNCTION = "get_function"#used as xml-tag
    self.DEFINES = "defines"
    self.PARENT = "parent"#used as xml-tag
    self.PARENTS = "parents"
    self.H_FILE = "h_file"
    self.C_FILE = "c_file"
    self.XML_FILE = "xml_file"
    self.MACRO = "macro"  #EO_CLASS or #define evas_obj_size_set  #used as xml-tag
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

    self.SET_ONLY = "set_only"
    self.GET_ONLY = "get_only"
    self.SET_GET = "set_get"
    self.METHOD = "method" #used as type id for property; and as xml tag

    self.EXTENSIONS = "extensions"  #used as xml-tag
    self.INSTANTIATEABLE = "instantiateable" #used as xml-tag
    self.CLASS = "class" #used as xml-tag
    self.INCLUDE = "include" #used as xml-tag
    self.TYPENAME = "typename" #used as xml-tag
    self.EXTERN_FUNCTION = "extern_function" #used as xml-tag
    self.EVENT = "event" #used as xml-tag
    self.EVENTS = "events" #used as xml-tag
    self.METHODS = "methods" #used as xml-tag
    self.XML_SUB_ID = "sub_id" #used as xml-tag
    self.PARAMETER = "parameter" #used as xml-tag
    self.C_TYPENAME = "c_typename" #used as xml-tag
    self.PRIMARY_TYPE = "primary_type" #used as xml-tag
    self.DIRECTION = "direction" #used as xml-tag
    self.COMMENT = "comment" #used as xml-tag


def isC(_path):
  #FIXME when parsing eobase we can catch "eo.c" with EO_DEFINE_CLASS
  (d, f) = os.path.split(_path)
  f_name = f.split('.')
  if len(f_name) == 2:
    return True if f_name[1] in ["c", "cc", "cpp"] else False
  else:
    return False

def isH(_path):
  (d, f) = os.path.split(_path)
  f_name = f.split('.')
  if len(f_name) == 2:
    return True if f_name[1] in ["h"] else False
  else:
    return False

def isXML(_path):
  (d, f) = os.path.split(_path)
  f_name = f.split('.')
  if len(f_name) == 2:
    return True if f_name[1] in ["xml"] else False
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
         else:
           print "Warning: path %s doesn't exist..."%path_tmp
     return res

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
   for l in _lst:
     l = l.replace("-"," ")
     l = l.replace("_"," ")
     l = capwords(l)
     l = "".join(l.split())
     res.append(l)
   return res

