#!/usr/bin/env python

from eo_parser.helper import isXML, abs_path_get, filter_files, normalize_names
from eo_parser.XMLparser import XMLparser
from argparse import ArgumentParser
import os, sys, shutil

def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass


def build_setup_file(module_name, pkg, outdir):
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

  parser.add_argument("-t", "--typedefs", dest="typedefs",
                  action="store", help="Additional typedefs for parser")

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
  typedefs = ""
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
    directories = abs_path_get(args.directory)
    if args.xmldir is not None:
      xmldir = abs_path_get(args.xmldir, False)

    outdir = abs_path_get([args.outdir])[0]


  if args.typedefs != None:
    typedefs = abs_path_get([args.typedefs])[0]

  verbose_print("Dirs: %s"%directories)
  verbose_print("Outdir: %s"%outdir)
  verbose_print("Xmldir: %s"%xmldir)

  xml_files = filter_files(directories, isXML, False)
  verbose_print("In Files: %s"%xml_files)


  xp = XMLparser()
  #adding typedefs to type definitions
  if typedefs:
    xp.typedefs_add(typedefs)

  for f in xml_files:
    xp.parse(f)

  #excluding everything, but the "eobase", if building eobse
  #excluding "eobase" module, if building non-eobase module
  if args.module == "eobase":
     if "Eo Base" in xp.objects:
       cl_data_tmp = dict(xp.objects)
       xp.objects = {}
       xp.objects["Eo Base"] = cl_data_tmp["Eo Base"]
       del cl_data_tmp
     else:
       print "ERROR: source files for module \"EoBase\" not found"
       exit(1)
  else:
     if "Eo Base" in xp.objects:
       xp.objects.pop("Eo Base")
       print("Warning: EoBase module was removed from building tree")


  parents_to_find =  xp.check_parents2()
  print parents_to_find

  verbose_print("Warning: need to find parent classes %s"%parents_to_find)

  if len(parents_to_find) != 0:

    if len(xmldir) == 0:
      print "No XML directory was provided"

    xml_files = filter_files(xmldir, isXML)

    if len(xml_files) == 0:
      print "ERROR: no include files found for %s classes... Aborting...(Use: --include=INCLUDE_DIR)"% ",".join(parents_to_find)
      exit(1)
    verbose_print("xml_files: %s"%xml_files)

    #Creating temp parser to look for in include files.
    xp_incl = XMLparser()
    for f in xml_files:
      xp_incl.parse(f)

    #Looking for parents. And saving proper object in include dictionary
    for n, o in xp_incl.objects.items():
      if n in parents_to_find:
        i = parents_to_find.index(n)
        parents_to_find.pop(i)
        n = normalize_names([n])[0]
        xp.objects_incl[n] = o
        print n

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


  objects_tmp = {}
  for n, o in xp.objects.items():
    o.c_name = normalize_names([o.c_name])[0]
    o.kl_id = normalize_names([o.kl_id])[0]
    o.parents = normalize_names(o.parents)
    objects_tmp[o.kl_id] = o

  xp.objects = objects_tmp

  #reodering parents and generating source code
  for n, o in xp.objects.items():
    o.parents = xp.reorder_parents2(o.parents)
    o.resolve()

  #saving source code
  for n, o in xp.objects.items():
    o.V.pxi_file_to_dir_save(outdir)
    o.V.pxd_file_to_dir_save(outdir)

  #xp.build_python_modules(args.module, args.pkg, sourcedir)
  build_setup_file(args.module, args.pkg, outdir)


#building right order of including files
  cl_parents = {}
  lst = []
  for n, o in xp.objects.items():
    cl_parents[n] = o.parents

  tmp = dict(cl_parents)

  cont = True
  while cont:
    cont = False
    for k in cl_parents:
      can_add = True
      for p in cl_parents[k]:
        if p in tmp:
          can_add = False
      if can_add is True:
        lst.append(k)
        tmp.pop(k)
        cont = True
    cl_parents = dict(tmp)
  if len(tmp) > 0:
    print "ERROR: can't resolve classes include order"
    exit(1)

  lines = []
  lines.append("from eodefault cimport *\n")
  for k in lst:
    lines.append("include \"%s\""%xp.objects[k].V.pxi["f_name"])

  f = open (os.path.join(outdir, args.module + ".pyx"), 'w')
  for l in lines:
    f.write(l + "\n")
  f.close()


#copying eodefault module into source dir to compile
  f_pyx = os.path.join(sourcedir, "eodefault.pyx")
  f_pxd = os.path.join(sourcedir, "eodefault.pxd")
  f_init = os.path.join(sourcedir, "__init__.py")
  try:
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

