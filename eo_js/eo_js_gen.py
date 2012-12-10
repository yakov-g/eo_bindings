#!/usr/bin/env python

from eoparser.helper import isXML, abs_path_get, dir_files_get, normalize_names
from eoparser.helper import _const
from eoparser.xmlparser import XMLparser
from argparse import ArgumentParser
import os, sys

const = _const()


def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass

def makefile_file_generate(module_name, args, c_files, outdir):
   pkg = args.pkg
   libs = args.libraries
   incl = args.includedirs

   makefile_file = "Makefile"
   default_c_files = ['main.cc', 'CElmObject.cc', '_eobase.cc', '_module.cc']
   c_files = default_c_files + c_files

   lines = []
   lines.append("CC=g++")
   lines.append("all: lib%s.so"%module_name)
   lines.append("\n")
   lines.append("lib_SOURCES = \\")
   for f in c_files:
      lines.append("%s \\"%f)
   lines[-1] = lines[-1][:-2]

   lines.append("")
   lines.append("lib_OBJECTS = $(lib_SOURCES:.cc=.o)")

   lines.append("")
   lines.append("lib_CFLAGS = \\")
   lines.append("-I. \\")
   lines.append("-DPACKAGE_DATA_DIR=\\\"/tmp\\\" \\")
   lines.append("-DPACKAGE_TMP_DIR=\\\"/tmp\\\" \\")
   for l in pkg.split():
      lines.append("`pkg-config --cflags %s` \\"%l)
   if incl is not None:   
     for i in incl:
       lines.append("-I%s \\"%i)
   lines[-1] = lines[-1][:-2]

   lines.append("")
   lines.append("lib_LDFLAGS = \\")
   for l in pkg.split():
      lines.append("`pkg-config --libs %s` \\"%l)

   if libs is not None:
     for l in libs:
       lines.append("-l%s \\"%l)
   lines[-1] = lines[-1][:-2]

   lines.append("")
   lines.append("lib%s.so: $(lib_OBJECTS)"%module_name)
   lines.append("\t$(CC) -shared -Wl,-soname,$@ -o $@ $^ $(lib_LDFLAGS)")

   lines.append("")
   lines.append("%.o : %.cc $(libjse_HEADERS)")
   lines.append("\t$(CC) -fPIC $(lib_CFLAGS) -c $< -o $@")

   lines.append("")
   lines.append("clean:")
   lines.append("\trm -f *~ *.o *.so")


   f = open(os.path.join(outdir, makefile_file), 'w')
   for l in lines:
     f.write(l + "\n")
   f.close()




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

  parser.add_argument("-I", "--some", dest="includedirs",
                  action="append", help="Include paths")

  parser.add_argument("-l", "--lib", dest="libraries",
                  action="append", help="Libraries to compile with")

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

  c_files = []
  for n, o in xp.objects.items():
    c_files.append(o.V.c_file.name)
 
  makefile_file_generate(args.module, args, c_files, outdir)

  del xp

if __name__ == "__main__":
  main()

