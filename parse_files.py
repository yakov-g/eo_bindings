from XMLparser import XMLparser
from Cparser import Cparser
from optparse import OptionParser
import getopt, sys, os

def isC(s): 
  if s[-2:] == ".c" and s.find("eobj.c") == -1:
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

def filter_files(_directories, func):
  res = []
  for d in _directories:
    for root, dirs, files in os.walk(d):
      tmp = []
      for f in files:
        tmp.append(os.path.join(root,f))
      res += filter(func, tmp)
  res = list(set(res))
  return res


parser = OptionParser()
parser.add_option("-d", "--dir", dest="directory",
                  action="append", help="source files")

parser.add_option("-o", "--outdir", dest="outdir",
                  action="store", help="output directory")


parser.add_option("-x", "--xmldir", dest="xmldir",
                  action="append", help="include xml directory")
"""
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
"""

(options, args) = parser.parse_args()

print "start.py :", options

verbose = False
directories = []
outdir = ""
xml_dirs = []

if options.directory == None:
  print "No source directory was provided"
  exit(1)
elif options.outdir == None:
  print "No out directory was provided"
  exit(1)


else:
   for d in options.directory:
     dir_tmp = d
     dir_tmp = os.path.expanduser(dir_tmp)
     dir_tmp = os.path.abspath(dir_tmp)
     if os.path.exists(dir_tmp):
       directories.append(dir_tmp)
     else:
       print "ERROR: directory %s doesn't exists... Aborting..."%dir_tmp
       exit(1)

   if options.xmldir is not None:
     for d in options.xmldir:
       dir_tmp = d
       dir_tmp = os.path.expanduser(dir_tmp)
       dir_tmp = os.path.abspath(dir_tmp)
       if os.path.exists(dir_tmp):
         xml_dirs.append(dir_tmp)
       else:
         print "ERROR: directory %s doesn't exists... Aborting"%dir_tmp
         exit()

   outdir = options.outdir
   outdir = os.path.expanduser(outdir)
   outdir = os.path.abspath(outdir)
   if not os.path.exists(outdir):
     print "ERROR: output directory %s doesn't exists... Aborting..."%outdir
     exit(1)

print "dirs",directories
print "outdir",outdir

c_files = filter_files(directories, isC)
h_files = filter_files(directories, isH)
#print "c: ", c_files
#print "h: ", h_files


cp = Cparser()
cp.outdir_set(outdir)

for f in c_files:
  cp.parse_description(f)

for f in h_files:
  cp.parse_prefixes2(f)

list_of_parents = []
for k in cp.cl_data:
  cp.parse_op_func_params2(k)
  cp.reorder_parents(k)
  list_of_parents += cp.cl_data[k]["parents"]

list_of_parents = list(set(list_of_parents))

parents_to_find = []
for l in list_of_parents: 
  if l not in cp.cl_data:
    parents_to_find.append(l)

print "parents_to_find", parents_to_find
#####################################################

if len(parents_to_find) != 0:

  if len(xml_dirs) == 0:
    print "No XML directory was provided"

  print "xml_dirs", xml_dirs
  xml_files = filter_files(xml_dirs, isXML)

  if len(xml_files) == 0:
    print "ERROR: no include files found for %s classes... Aborting..."% ",".join(parents_to_find)
    exit()
#  print "xml_files: ", xml_files


  for f in xml_files:
    xp = XMLparser()
    xp.parse(f)
    if xp.class_data["macro"] in parents_to_find:
      print "file: ", f
      cp.cl_incl[xp.class_data["macro"]] = {"module":xp.globals["module"],
                                          "name" : xp.class_data["name"]}
      i = parents_to_find.index(xp.class_data["macro"])
      parents_to_find.pop(i)
    del xp

  if len(parents_to_find) != 0:
    print "ERROR: XML files weren't found for %s classes... Aborting"%(",".join(parents_to_find))
    exit(1)
  print cp.cl_incl



for k in cp.cl_data:
  if k != "EOBJ_DEFAULT_CLASS":
    cp.build_xml2(k)
    xp = XMLparser()
    xp.parse(cp.cl_data[k]["xml_file"])
    xp.testall()
    xp.build_module()
    del xp

#cp.print_data()



