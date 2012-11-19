#!/usr/bin/env python

from eoparser.helper import isXML, abs_path_get, dir_files_get, normalize_names
from eoparser.xmlparser import XMLparser
from argparse import ArgumentParser
import os, sys, shutil

def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass


def setup_file_generate(module_name, pkg, outdir):
   module_file = module_name + ".pyx"

   lines = []
   lines.append("from distutils.core import setup")
   lines.append("from distutils.extension import Extension")
   lines.append("from Cython.Distutils import build_ext")
   lines.append("import commands, os")
   lines.append("")

   lines.append("def pkgconfig(_libs):")
   lines.append("  cf = commands.getoutput(\"pkg-config --cflags %s\"%_libs).split()")
   lines.append("  ldf = commands.getoutput(\"pkg-config --libs %s\"%_libs).split()")
   lines.append("  return (cf, ldf)")
   lines.append("")

   lines.append("(e_compile_args, e_link_args) = pkgconfig(\"%s\")"%pkg)
   lines.append("")

   lines.append("e_include_dirs = [\".\"]")
   lines.append("e_library_dirs = []")
   lines.append("e_libraries = []")
   lines.append("")

   lines.append("setup(")
   lines.append("  cmdclass = {'build_ext': build_ext},")
   lines.append("  ext_modules = [")

   if module_name == "eobase":
     lines.append("  Extension(\"%s\", ['%s'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),"%("eodefault", "eodefault.pyx"))

   lines.append("  Extension(\"%s\", ['%s'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),"%(module_name, module_name + ".pyx"))

   lines.append("   ])\n\n")


   f = open(os.path.join(outdir, "setup.py"), 'w')
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
  xp.py_code_generate(args.module ,outdir)

  setup_file_generate(args.module, args.pkg, outdir)

  #Looking for "eodefault.pxd" module. Needed to include
  for d in incl_dirs:
    d_tmp = os.path.join(d, "eodefault.pxd")
    if os.path.exists(d_tmp):
      sourcedir = d
      break

  if sourcedir == "":
    print "ERROR: no include files were found... Aborting... (Use: --include=INCLUDE_DIR)"
    exit(1)

  #copying eodefault module into source dir
  f_pyx = os.path.join(sourcedir, "eodefault.pyx")
  f_pxd = os.path.join(sourcedir, "eodefault.pxd")
  f_init = os.path.join(sourcedir, "__init__.py")
  try:
    #this file is needed only to build eodefault.
    if args.module  == "eobase":
      shutil.copy(f_pyx, outdir)
    shutil.copy(f_pxd, outdir)
    shutil.copy(f_init, outdir)
  except IOError as ex:
    print "%s"%ex
    print "Aborting"
    exit(1)
  except shutil.Error as er:
    print "Warning: %s"%er

  del xp

if __name__ == "__main__":
  main()

