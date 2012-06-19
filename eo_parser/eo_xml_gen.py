#!/usr/bin/env python

from eo_parser.helper import filter_files, filter_path, filter_path_no_warning, isC, isH, isXML
from eo_parser.XMLparser import XMLparser
from eo_parser.Cparser import Cparser
from argparse import ArgumentParser
import sys

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

  verbose_print( "start.py %s"%args)

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
    directories = filter_path(args.directory)
    if args.xmldir is not None:
      xmldir = filter_path_no_warning(args.xmldir)
    outdir = filter_path(args.outdir)

  verbose_print( "dirs %s"%directories)
  verbose_print( "outdir %s"%outdir)

  c_files = filter_files(directories, isC)
  h_files = filter_files(directories, isH)

  cp = Cparser(args.verbose)
  cp.outdir_set(outdir)

  for f in c_files:
    cp.parse_description(f)

  for f in h_files:
    cp.parse_prefixes(f)


  cl_data_tmp = dict(cp.cl_data)
  for k in cl_data_tmp:
    if "get_function" not in cp.cl_data[k]:
      print "Warning: no define for class: %s. Record will be excluded from tree"%k
      cp.cl_data.pop(k)
#  cp.print_data()
  del cl_data_tmp

  list_of_parents = []
  for k in cp.cl_data:
    cp.parse_op_func_params(k)
    list_of_parents += cp.cl_data[k]["parents"]

  list_of_parents = list(set(list_of_parents))

  cl_data_tmp2 = dict(cp.cl_data)
  parents_to_find = filter(lambda ll: True if ll not in cl_data_tmp2 else False, list_of_parents)

  verbose_print( "parents_to_find: %s"%parents_to_find)
#####################################################

  if len(parents_to_find) != 0:

    if len(xmldir) == 0:
      print "No XML directory was provided"


    verbose_print("xmldir: %s\n"%xmldir)
    xml_files = filter_files(xmldir, isXML, False)

    if len(xml_files) == 0:
      print "ERROR: no include files found for %s classes... Aborting..."% ",".join(parents_to_find)
      exit(1)
    verbose_print("xml_files: %s\n"%xml_files)

    xp = XMLparser()
    for f in xml_files:
      xp.parse(f)

    for k in xp.cl_data:
      kl_dt = xp.cl_data[k]
      if kl_dt["macro"] in parents_to_find:

         cp.cl_incl[kl_dt["macro"]] = {"module" : kl_dt["module"],
                                     "c_name" : kl_dt["c_name"]}
         i = parents_to_find.index(kl_dt["macro"])
         parents_to_find.pop(i)
    del xp


    if len(parents_to_find) != 0:
      print "ERROR: XML files weren't found for %s classes... Aborting"%(",".join(parents_to_find))
      exit(1)


  for k in cp.cl_data:
    cp.build_xml2(k)

  del cp

if __name__ == "__main__":
  main()


