import os
from string import capwords

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


def filter_files(_directories, func, recursive = True):
  res = []
  if recursive:
    for d in _directories:
      for root, dirs, files in os.walk(d):
        tmp = []
        for f in files:
          tmp.append(os.path.join(root,f))
        res += filter(func, tmp)
  else:
    for d in _directories:
      tmp = []
      for f in os.listdir(d):
        tmp.append(os.path.join(d, f))
      res += filter(func, tmp)

  res = list(set(res))
  return res

def filter_path(lst):
   if type(lst) == list:
     res = []
     lst = list(set(lst))
     for d in lst:
       path_tmp = d
       path_tmp = os.path.expanduser(path_tmp)
       path_tmp = os.path.abspath(path_tmp)
       if os.path.exists(path_tmp):
         res.append(path_tmp)
       else:
         print "ERROR: path %s doesn't exists... Aborting..."%path_tmp
         exit(1)
     return res

   elif type(lst) == str:
     path_tmp = lst
     path_tmp = os.path.expanduser(path_tmp)
     path_tmp = os.path.abspath(path_tmp)
     if not os.path.exists(path_tmp):
       print "ERROR: output path %s doesn't exists... Aborting..."%path_tmp
       exit(1)
     return path_tmp

def filter_path_no_warning(lst):
   if type(lst) == list:
     res = []
     lst = list(set(lst))
     for d in lst:
       path_tmp = d
       path_tmp = os.path.expanduser(path_tmp)
       path_tmp = os.path.abspath(path_tmp)
       if os.path.exists(path_tmp):
         res.append(path_tmp)
     return res

   elif type(lst) == str:
     path_tmp = lst
     path_tmp = os.path.expanduser(path_tmp)
     path_tmp = os.path.abspath(path_tmp)
     if not os.path.exists(path_tmp):
       path_tmp = ""
     return path_tmp

def normalize_names(_lst):
   res = []
   if type(_lst) is str:
     l = _lst
     l = l.replace("-"," ")
     l = l.replace("_"," ")
     l = capwords(l)
     l = "".join(l.split())
     return l
   for l in _lst:
     l = l.replace("-"," ")
     l = l.replace("_"," ")
     l = capwords(l)
     l = "".join(l.split())
     res.append(l)
   return res

