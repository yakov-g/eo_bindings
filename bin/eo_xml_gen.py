#!/usr/bin/env python

from eoparser.helper import dir_files_get, abs_path_get, isC, isH, isXML
from eoparser.helper import _const
from eoparser.xmlparser import XMLparser
from eoparser.cparser import Cparser
from eoparser.cparser import LOCAL_CPARSER
from argparse import ArgumentParser
import sys

#creating instance to handle constants
const = _const()

def verbose_true(mes):
  print mes
def verbose_false(mes):
  pass

def main():

  if not LOCAL_CPARSER:
     print "Wrong cparser imported:"
     exit()
  parser = ArgumentParser()
  parser.add_argument("-d", "--dir", dest="directory",
                  action="append", help="Source C-files to introspect", required=True)

  parser.add_argument("-o", "--outdir", dest="outdir",
                  action="store", help="Output directory", required=True)

  parser.add_argument("-t", "--typedefs", dest="typedefs",
                  action="store", help="Additional typedefs for parser")

  parser.add_argument("-X", "--xmldir", dest="xmldir", default = sys.path,
                  action="append", help="Directory to search for parent classes's XMLs")

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Verbose output")

  parser.add_argument("-E", "--eo",
                  action="store_true", dest="eoformat", default=False,
                  help="Generate *.eo description files")

  parser.add_argument("-E2", "--eo2",
                  action="store_true", dest="eoformat2", default=False,
                  help="Generate *.eo description files")

  args = parser.parse_args()
  verbose_print = None

  if args.verbose is True:
    verbose_print = verbose_true
  else:
    verbose_print = verbose_false

  directories = []
  outdir = ""
  typedefs = ""
  xmldir = []

  directories = abs_path_get(args.directory)
  outdir = abs_path_get([args.outdir])[0]

  if args.xmldir is not None:
    xmldir = abs_path_get(args.xmldir, False)# not abort if dir doesn't exist

  if args.typedefs != None:
    typedefs = abs_path_get([args.typedefs])[0]

  files = dir_files_get(directories)
  c_files = filter(isC, files)
  h_files = filter(isH, files)

  cp = Cparser(args.verbose)
  cp.outdir_set(outdir)

  #adding typedefs from extern file
  if typedefs:
    cp.typedefs_add(typedefs)

  #fetching data from c-file
  for f in c_files:
  #  cp.c_file_data_get(f)
    cp.c_file_data_get2(f)

  #fetching data from h-file
  for f in h_files:
    cp.h_file_data_get(f)

  #remove records, which are not class, t.e. they don't have GET_FUNCTION key
  cl_data_tmp = dict(cp.cl_data) #deep copy of dictionary
  for k in cl_data_tmp:
    if const.GET_FUNCTION not in cp.cl_data[k]:
      print "Warning: no define for class: %s. Record will be excluded from tree"%k
      cp.cl_data.pop(k)
  del cl_data_tmp

  #mapping #defines, comments(@def) and op_ids together, to parse parameters
  for k in cp.cl_data:
    cp.parse_op_func_params(k)

  #if we want to generate Eo format we don't need parents
  # because we only generate description
  if args.eoformat:
     #generatinf .eo file in C-style
     for k in cp.cl_data:
       cp.build_eo(k)
     exit(0)

  if args.eoformat2:
     #building XMLs
     for k in cp.cl_data:
       cp.build_eo2(k)
     exit(0)

  # here starts parent dependency search and XML build

  #creating list of all parents for classes which are in tree
  list_of_parents = []
  for k in cp.cl_data:
    list_of_parents += cp.cl_data[k][const.PARENTS]
  list_of_parents = list(set(list_of_parents))

  #checking, if we need to find any parent and filtering it's ids
  cl_data_tmp2 = dict(cp.cl_data)
  parents_to_find = filter(lambda ll: True if ll not in cl_data_tmp2 else False, list_of_parents)

  #if we have parents to find
  if len(parents_to_find) != 0:
    if len(xmldir) == 0:
      print "No XML directory was provided"

    verbose_print("xmldir: %s\n"%xmldir)
    xml_files = dir_files_get(xmldir)
    xml_files = filter(isXML, xml_files)

    if len(xml_files) == 0:
      print "ERROR: no include files found for %s classes... Aborting..."% ",".join(parents_to_find)
      exit(1)

    #parsing include XMLs
    xp = XMLparser()
    for f in xml_files:
      xp.parse(f)

    #saving data about parents we were looking for
    for n, o in xp.objects.items():
      if o.macro in parents_to_find:
         cp.cl_incl[o.macro] = {const.MODULE : o.mod_name,
                                const.C_NAME : o.c_name}
         i = parents_to_find.index(o.macro)
         parents_to_find.pop(i)
    del xp

    #if there are still parents, which we need to find - exit
    if len(parents_to_find) != 0:
      print "ERROR: XML files weren't found for %s classes... Aborting"%(",".join(parents_to_find))
      exit(1)

  #building XMLs
  for k in cp.cl_data:
    cp.build_xml(k)

  del cp

if __name__ == "__main__":
  main()


