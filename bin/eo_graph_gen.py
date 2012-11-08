#!/usr/bin/env python

from eoparser.helper import isXML, dir_files_get, abs_path_get
from eoparser.xmlparser import XMLparser
from argparse import ArgumentParser
import os

def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass

def main():
  parser = ArgumentParser()
  parser.add_argument("-d", "--dir", dest="directory",
                  action="append", help="Source files directory")

  parser.add_argument("-o", "--outfile", dest="outfile",
                  action="store", help="Path for output files")

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Print status messages to stdout")

  parser.add_argument("--graphstyle", action="store", dest="graphstyle", default="digraph",
                  help="Set graph style. Default: \"digraph\"")

  parser.add_argument("--edge", action="store", dest="edge", default="solid",
                  help="Set line style for parent edge. Default: \"solid\"")

  parser.add_argument("--extedge", action="store", dest="extedge", default="dashed",
                  help="Set line style for extension edge. Default: \"dashed\"")

  parser.add_argument("--rankdir", action="store", dest="rankdir", default="BT",
                  help="Direction of directed graph[BT, TB, LR, RL]. Default: \"BT\"")

  parser.add_argument("--graphfontsize", action="store", dest="graphfontsize", default="15",
                  help="Graph font size. Default: \"15\"")

  parser.add_argument("--graphlabel", action="store", dest="graphlabel", default="",
                  help="Graph label")

  parser.add_argument("--nodefontsize", action="store", dest="nodefontsize", default="10",
                  help="Node font size. Default: \"10\"")

  parser.add_argument("--nodeshape", action="store", dest="nodeshape", default="polygon",
                  help="Node shape.[\"polygon\", \"circle\", \"ellipse\"] Default: \"polygon\"")


  styles = {}

  args = parser.parse_args()
  styles["edge"] = args.edge
  styles["extedge"] = args.extedge
  styles["graphstyle"] = args.graphstyle
  styles["rankdir"] = args.rankdir
  styles["graphfontsize"] = args.graphfontsize
  styles["graphlabel"] = args.graphlabel
  styles["nodefontsize"] = args.nodefontsize
  styles["nodeshape"] = args.nodeshape


  types = {
            "REGULAR":"EO_CLASS_TYPE_REGULAR",
            "MIXIN" : "EO_CLASS_TYPE_MIXIN",
            "INTERFACE":"EO_CLASS_TYPE_INTERFACE",
            "NO_INSTANT":"EO_CLASS_TYPE_REGULAR_NO_INSTANT"
          }

  n_color = {
              types["REGULAR"]:"green",
              types["MIXIN"] : "blue",
              types["INTERFACE"]:"red",
              types["NO_INSTANT"]:"darkviolet"
            }

  verbose_print = None
  if args.verbose is True:
    verbose_print = verbose_true
  else:
    verbose_print = verbose_false

  verbose_print("Options: %s"%args)
  verbose_print("Args: %s"%args)

  directories = []
  outfile = ""

  if args.directory == None:
    print "ERROR: no source directory was provided"
    exit(1)
  elif args.outfile == None:
    print "ERROR: no output file was provided"
    exit(1)

  else:
    directories = abs_path_get(args.directory)

    outfile = args.outfile
    outfile = os.path.expanduser(outfile)
    outfile = os.path.abspath(outfile)

    outdir = os.path.split(outfile)[0]
    if not os.path.exists(outdir):
      print "ERROR: output directory %s doesn't exists... Aborting..."%outdir
      exit(1)

  verbose_print("Dirs: %s"%directories)
  verbose_print("Outfile: %s"%outfile)

  xml_files = dir_files_get(directories)
  xml_files = filter(isXML, xml_files)

  graph = {}

  if len(xml_files) == 0:
    print "ERROR: no xml files were found"
    exit(1)

  xp = XMLparser()
  for f in xml_files:
    xp.parse(f)

  graph = dict(xp.objects)

  del xp

  if len(graph) == 0:
    print "ERROR: no data was found in source files"
    exit(1)

  lines = []

  lines.append("%s G{"%(styles["graphstyle"]))
  lines.append("      graph [rankdir = \"%s\", fontsize = %s, label = \"%s\"];"%(styles["rankdir"], styles["graphfontsize"], styles["graphlabel"]))
  lines.append("      node [shape = \"%s\" fontsize = %s];"%(styles["nodeshape"], styles["nodefontsize"]))

  #generating dot node description for node, for each class
  for n, o in graph.items():
    if o.eo_type == types["REGULAR"]:
      line = "      \"%s\" [label = \"%s \\n %s\", color = \"%s\"];"%(n, o.c_name, o.eo_type, n_color[types["REGULAR"]])
    elif o.eo_type == types["MIXIN"]:
      line = "      \"%s\" [label = \"%s \\n %s\", color = \"%s\"];"%(n, o.c_name, o.eo_type, n_color[types["MIXIN"]])
    elif o.eo_type == types["INTERFACE"]:
      line = "      \"%s\" [label = \"%s \\n %s\", color = \"%s\"];"%(n, o.c_name, o.eo_type, n_color[types["INTERFACE"]])
    elif o.eo_type == types["NO_INSTANT"]:
      line = "      \"%s\" [label = \"%s \\n %s\", color = \"%s\"];"%(n, o.c_name, o.eo_type, n_color[types["NO_INSTANT"]])
    else:
      line = "      \"%s\" [label = \"%s \\n %s\"];"%(n, o.c_name, o.eo_type)

    lines.append(line)

  #generating dot edge description for each parent of each class
  for n, o in graph.items():
    parent = o.parents[0]
    ext = o.parents[1:]
    ext = filter(len, ext)
    if len(parent) != 0:
      if parent in graph:
        p_type = graph[parent].eo_type
      else:
        p_type = types["REGULAR"]
      line = "      \"%s\" -> \"%s\" [style = \"%s\", color=\"%s\"];"%(n, parent, styles["edge"], n_color[p_type])
      lines.append(line)
    for l in ext:
      if graph[l].eo_type == types["REGULAR"]:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(n, l, "dashed", n_color[types["REGULAR"]])
      elif graph[l].eo_type == types["MIXIN"]:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(n, l, "dashed", n_color[types["MIXIN"]])
      elif graph[l].eo_type == types["INTERFACE"]:
#       line = "      \"%s\" -> \"%s\" [style=\"%s\"] ;"%(k, l, styles["extedge"])
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color = \"%s\"] ;"%(n, l, "dotted", n_color[types["INTERFACE"]])
      elif graph[l].eo_type == types["NO_INSTANT"]:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(n, l, "dashed", n_color[types["NO_INSTANT"]])
      else:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(k, l, "dashed", "black")

      lines.append(line)
  lines.append("}")

  f = open(outfile, 'w')
  for l in lines:
    f.write(l+'\n')

  f.close()

  verbose_print("dot file: %s was generated"%(outfile))

if __name__ == "__main__":
  main()

