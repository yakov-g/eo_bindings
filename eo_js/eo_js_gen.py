#!/usr/bin/env python

from eo_parser.helper import isXML, abs_path_get, dir_files_get, normalize_names
from eo_parser.helper import _const
from eo_parser.XMLparser import XMLparser
from argparse import ArgumentParser
import os, sys

const = _const()


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
  incl_dirs = []

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
    directories = abs_path_get(args.directory)
    outdir = abs_path_get([args.outdir])[0]
    if args.xmldir is not None:
      incl_dirs = abs_path_get(args.xmldir, False)

  verbose_print("Dirs: %s"%directories)
  verbose_print("Outdir: %s"%outdir)
  verbose_print("Include dirs: %s"%incl_dirs)

  xml_files = dir_files_get(directories, False)
  xml_files = filter(isXML, xml_files)
  verbose_print("In Files: %s"%xml_files)

  xp = XMLparser()
  xp.module_parse(args.module, xml_files, incl_dirs)
  xp.js_code_generate(outdir)

  del xp

if __name__ == "__main__":
  main()

