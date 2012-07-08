#!/usr/bin/env python

from eo_parser.helper import filter_files, abs_path_get, isC, isH, isXML
from eo_parser.helper import _const
from eo_parser.XMLparser import XMLparser
from eo_parser.Cparser import Cparser
from argparse import ArgumentParser
import sys


const = _const()

def verbose_true(mes):
  print mes
def verbose_false(mes):
  pass

def main():

  parser = ArgumentParser()
  parser.add_argument("-d", "--dir", dest="directory",
                  action="append", help="source files")

  parser.add_argument("-o", "--outdir", dest="outdir",
                  action="store", help="output directory")

  parser.add_argument("-i", "--include", dest="xmldir", default = sys.path,
                  action="append", help="Include xml directory")

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")

  args = parser.parse_args()
  verbose_print = None

  if args.verbose is True:
    verbose_print = verbose_true
  else:
    verbose_print = verbose_false

  directories = []
  outdir = ""
  xmldir = []

  if args.directory == None:
    print "No source directory was provided"
    exit(1)
  elif args.outdir == None:
    print "No out directory was provided"
    exit(1)
  else:
    directories = abs_path_get(args.directory)
    if args.xmldir is not None:
      xmldir = abs_path_get(args.xmldir, False)# not abort if dir doesn't exist

    outdir = abs_path_get([args.outdir])[0]

  verbose_print("dirs %s"%directories)
  verbose_print("outdir %s"%outdir)

  c_files = filter_files(directories, isC)
  h_files = filter_files(directories, isH)

  cp = Cparser(args.verbose)
  cp.outdir_set(outdir)

  #fetching data from c-file
  for f in c_files:
    cp.c_file_data_get(f)

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

  #creating list of all parents for classes which are in tree
  list_of_parents = []
  for k in cp.cl_data:
    list_of_parents += cp.cl_data[k][const.PARENTS]
  list_of_parents = list(set(list_of_parents))

  #checking, if we need to find any parent and filtering it's ids
  cl_data_tmp2 = dict(cp.cl_data)
  parents_to_find = filter(lambda ll: True if ll not in cl_data_tmp2 else False, list_of_parents)

  verbose_print("parents_to_find: %s"%parents_to_find)

  #if we have parents to find
  if len(parents_to_find) != 0:
    if len(xmldir) == 0:
      print "No XML directory was provided"

    verbose_print("xmldir: %s\n"%xmldir)
    xml_files = filter_files(xmldir, isXML, False)

    if len(xml_files) == 0:
      print "ERROR: no include files found for %s classes... Aborting..."% ",".join(parents_to_find)
      exit(1)
    verbose_print("xml_files: %s\n"%xml_files)

    #parsing include XMLs
    xp = XMLparser()
    for f in xml_files:
      xp.parse(f)

    #saving data about parents we were looking for
    for k in xp.cl_data:
      kl_dt = xp.cl_data[k]
      print kl_dt[const.MACRO]
      if kl_dt[const.MACRO] in parents_to_find:
         cp.cl_incl[kl_dt[const.MACRO]] = {const.MODULE : kl_dt[const.MODULE],
                                           const.C_NAME : kl_dt[const.C_NAME]}
         i = parents_to_find.index(kl_dt[const.MACRO])
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


