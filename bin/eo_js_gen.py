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

def makefile_file_generate(args, c_files, outdir):
   module_name = args.module
   pkg = args.pkg
   incl_paths = ["."]
   if args.include_paths is not None:
     incl_paths += args.include_paths
   libs = args.libraries
   lib_paths = args.library_paths
   cpp_defines = args.cpp_defines

   #if someone wants to add -DSOME_STR=\"str\"
   #I will add one more escape symbol, because I also generate Makefile
   if cpp_defines is not None:   
     lst_tmp = []
     for d in cpp_defines:
       lst_tmp.append(d.replace("\"", "\\\""))
     cpp_defines = list(lst_tmp)
     del lst_tmp

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
  # lines.append("-I. \\")
  #lines.append("-DPACKAGE_DATA_DIR=\\\"/tmp\\\" \\")
  #lines.append("-DPACKAGE_TMP_DIR=\\\"/tmp\\\" \\")

   for i in incl_paths:
     lines.append("-I%s \\"%i)

   for l in pkg.split():
     lines.append("`pkg-config --cflags %s` \\"%l)

   if cpp_defines is not None:   
     for d in cpp_defines:
       lines.append("-D%s \\"%d)
   lines[-1] = lines[-1][:-2]

   lines.append("")
   lines.append("lib_LDFLAGS = \\")
   for l in pkg.split():
      lines.append("`pkg-config --libs %s` \\"%l)

   if lib_paths is not None:
     for l in lib_paths:
       lines.append("-L%s \\"%l)

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
                  action="append", help="Path to XML descriptions", required=True)

  parser.add_argument("-o", "--outdir", dest="outdir",
                  action="store", help="Output directory", required=True)

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Verbose output")

  parser.add_argument("-X", "--xmldir", dest="xmldir", default=sys.path,
                  action="append", help="Directory to search for parent classes's XMLs")

  parser.add_argument("--pkg", dest="pkg", default = "eo",
        action="store", help="pkg-confing libraries. Default: \"eo\"")

  parser.add_argument("-m", "--module", dest="module",
                  action="store", help="Name of module", required=True)

  parser.add_argument("-I", "--include", dest="include_paths",
                  action="append", help="Pre-processor include path")

  parser.add_argument("-l", "--library", dest="libraries",
                  action="append", help="Libraries of this unit")

  parser.add_argument("-L", "--library-path", dest="library_paths",
                  action="append", help="Directories to search for libraries")

  parser.add_argument("-D", "--define", dest="cpp_defines",
                  action="append", help="Pre-processor define")


  args = parser.parse_args()

  verbose_print = verbose_true if args.verbose is True else verbose_false

  directories = []
  outdir = ""
  sourcedir = ""
  incl_dirs = []

  directories = abs_path_get(args.directory)
  outdir = abs_path_get([args.outdir])[0]
  if args.xmldir is not None:
    incl_dirs = abs_path_get(args.xmldir, False)

  xml_files = dir_files_get(directories, False)
  xml_files = filter(isXML, xml_files)

  xp = XMLparser()
  xp.module_parse(args.module, xml_files, incl_dirs)
  xp.js_code_generate(outdir)

  c_files = []
  for n, o in xp.objects.items():
    c_files.append(o.V.c_file.name)
 
  makefile_file_generate(args, c_files, outdir)

  del xp

if __name__ == "__main__":
  main()

