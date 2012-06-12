#!/usr/bin/env python

from eo_parser.helper import isXML, filter_path, filter_path_no_warning, filter_files, normalize_names
from eo_parser.XMLparser import XMLparser
from argparse import ArgumentParser
import os, sys

def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass

def main():
  parser = ArgumentParser()
  parser.add_argument("-d", "--dir", dest="directory",
                  action="append", help="Source files")

  parser.add_argument("-o", "--outdir", dest="outdir",
                  action="store", help="Output directory")

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Print status messages to stdout. Default: False")

  parser.add_argument("-i", "--include", dest="xmldir", default=sys.path,
                  action="append", help="Include eobase directory")

  parser.add_argument("--pkg", dest="pkg", default = "elementary eo",
        action="store", help="pkg-confing libraries. Default: \"elementary eo\"")

  parser.add_argument("-m", "--module", dest="module",
                  action="store", help="Name of module to generate")

  args = parser.parse_args()

  verbose_print = verbose_true if args.verbose is True else verbose_false

  verbose_print("Options: %s"%args)

  directories = []
  outdir = ""
  sourcedir = ""
  xmldir = []

  if args.directory == None:
    print "ERROR: No source directory was provided"
    exit(1)
  elif args.outdir == None:
    print "ERROR: No out directory was provided"
    exit(1)
  elif args.module == None:
    print "ERROR: No module name was provided"
    exit(1)
  else:
    directories = filter_path(args.directory)
    if args.xmldir is not None:
      xmldir = filter_path_no_warning(args.xmldir)

    outdir = filter_path(args.outdir)

  verbose_print("Dirs: %s"%directories)
  verbose_print("Outdir: %s"%outdir)
  verbose_print("xmldir: %s"%xmldir)

  xml_files = filter_files(directories, isXML, False)
  verbose_print("In Files: %s"%xml_files)

  xp = XMLparser()
  xp.outdir_set(outdir)

  for f in xml_files:
    xp.parse(f)

  for kl in xp.cl_data:
     xp.js_parse(kl)

#  xp.print_data()

  parents_to_find =  xp.check_parents()
  verbose_print("Warning: need to find parent classes %s"%parents_to_find)

  if len(parents_to_find) != 0:

    if len(xmldir) == 0:
      print "No XML directory was provided"

    xml_files = filter_files(xmldir, isXML)

    if len(xml_files) == 0:
      print "ERROR: no include files found for %s classes... Aborting...(Use: --include=INCLUDE_DIR)"% ",".join(parents_to_find)
      exit(1)
    verbose_print( "xml_files: %s"%xml_files)

    xp_incl = XMLparser()
    for f in xml_files:
      xp_incl.parse(f)


    for k in xp_incl.cl_data:
      kl_dt = xp_incl.cl_data[k]
      if kl_dt["c_name"] in parents_to_find:
#     print "class: ", k
        n = kl_dt["c_name"]
        n = normalize_names(n)
        xp.cl_incl[n] = kl_dt
        i = parents_to_find.index(kl_dt["c_name"])
        parents_to_find.pop(i)
    del xp_incl

    if len(parents_to_find) != 0:
      print "ERROR: XML files weren't found for %s classes... Aborting"%(",".join(parents_to_find))
      exit(1)

  for d in xmldir:
    d_tmp = os.path.join(d, "eodefault.pxd")
    if os.path.exists(d_tmp):
      sourcedir = d
      break

  if sourcedir == "":
    print "ERROR: no include files were found... Aborting... (Use: --include=INCLUDE_DIR)"
    exit(1)
  xp.build_js_modules(args.module, args.pkg, sourcedir)

#  os.system("cd %s && python setup.py build_ext --inplace && rm -rf *.c build/"%outdir)

  del xp



if __name__ == "__main__":
  main()

