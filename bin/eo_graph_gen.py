#!/usr/bin/env python

from eoparser.helper import isXML, dir_files_get, abs_path_get
from eoparser.xmlparser import XMLparser
from argparse import ArgumentParser
import os, sys

def verbose_true(mes):
  print mes

def verbose_false(mes):
  pass

def main():
  parser = ArgumentParser()
  parser.add_argument("-d", "--dir", dest="directory",
                  action="append", help="Path to XML descriptions", required=True)

  parser.add_argument("-o", "--outfile", dest="outfile",
        action="store", help="Out file in png format. Default: \"out.png\"", default="out.png")

  parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Verbose output")
  """
  parser.add_argument("--graphstyle", action="store", dest="graphstyle", default="digraph",
                  help="Set graph style. Default: \"digraph\"")
  """

  parser.add_argument("--extedge", action="store", dest="extedge", default="dashed, dashed, dotted, dashed",
                  help="Set line style for extension edges depending on extension type(REGULAR, MIXIN, INTERFACE, NO_INSTANT).[\"solid, dotted, dashed, bold\"].  Default: \"dashed, dashed, dotted, dashed\"")

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

  parser.add_argument("--long-names", action="store", dest="short_long", default="short",
                  help="Node shape.[\"short\", \"long\"] Default: \"short\"")

  styles = {}

  args = parser.parse_args()
  styles["extedge"] = args.extedge.replace(" ", "").split(",")
  if len (styles["extedge"]) < 4:
     print "--extedge option is not correct"
     exit(1)
  styles["graphstyle"] = "digraph"# args.graphstyle
  styles["rankdir"] = args.rankdir
  styles["graphfontsize"] = args.graphfontsize
  styles["graphlabel"] = args.graphlabel
  styles["nodefontsize"] = args.nodefontsize
  styles["nodeshape"] = args.nodeshape
  SHORT_LONG = 0 if args.short_long == "short" else 1

  TYPE_REGULAR = "EO_CLASS_TYPE_REGULAR"
  TYPE_MIXIN = "EO_CLASS_TYPE_MIXIN"
  TYPE_INTERFACE = "EO_CLASS_TYPE_INTERFACE"
  TYPE_NO_INSTANT = "EO_CLASS_TYPE_REGULAR_NO_INSTANT"

  types_list = (TYPE_REGULAR, TYPE_MIXIN, TYPE_INTERFACE, TYPE_NO_INSTANT)

  type_names = {
            TYPE_REGULAR : ("REGULAR", "EO_CLASS_TYPE_REGULAR"),
            TYPE_MIXIN : ("MIXIN", "EO_CLASS_TYPE_MIXIN"),
            TYPE_INTERFACE : ("INTERFACE", "EO_CLASS" ),
            TYPE_NO_INSTANT : ("NO INSTANT", "EO_CLASS_TYPE_REGULAR_NO_INSTANT")
          }

  #node colors
  n_color = {
              TYPE_REGULAR :"green",
              TYPE_MIXIN : "blue",
              TYPE_INTERFACE :"red",
              TYPE_NO_INSTANT :"darkviolet"
            }

  #ext edge line style
  p_edge = {}
  p_edge[TYPE_REGULAR] = styles["extedge"][0]
  p_edge[TYPE_MIXIN] = styles["extedge"][1]
  p_edge[TYPE_INTERFACE] = styles["extedge"][2]
  p_edge[TYPE_NO_INSTANT] = styles["extedge"][3]

  verbose_print = None
  if args.verbose is True:
    verbose_print = verbose_true
  else:
    verbose_print = verbose_false

  directories = args.directory + sys.path
  directories = abs_path_get(directories, False)

  outfile = args.outfile
  outfile = os.path.expanduser(outfile)
  outfile = os.path.abspath(outfile)

  outdir = os.path.split(outfile)[0]
  if not os.path.exists(outdir):
    print "ERROR: output directory %s doesn't exists... Aborting..."%outdir
    exit(1)

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
    if o.eo_type in types_list:
      line = "      \"%s\" [label = \"%s \\n %s\", color = \"%s\"];"%(n, o.c_name, type_names[o.eo_type][SHORT_LONG], n_color[o.eo_type])
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
        p_type = TYPE_REGULAR
      line = "      \"%s\" -> \"%s\" [style = \"%s\", color=\"%s\"];"%(n, parent, "solid", n_color[p_type])
      lines.append(line)
    for l in ext:
      eo_type_tmp = graph[l].eo_type
      if eo_type_tmp in types_list:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(n, l, p_edge[eo_type_tmp], n_color[eo_type_tmp])
      else:
        line = "      \"%s\" -> \"%s\" [style=\"%s\", color=\"%s\"] ;"%(k, l, "dashed", "black")

      lines.append(line)
  lines.append("}")

  tmp_dot_file = "tmp.dot"
  f = open(tmp_dot_file, 'w')
  for l in lines:
    f.write(l+'\n')

  f.close()

  verbose_print("Dot file: '%s' was generated"%(tmp_dot_file))
  verbose_print("Graph file: '%s was generated"%(outfile))
  os.system("dot -Tpng %s -o %s"%(tmp_dot_file, outfile))
  #os.system("neato -Tpng %s -o %s_neato"%(tmp_dot_file, outfile))
  #os.system("twopi -Tpng %s -o %s_twopi"%(tmp_dot_file, outfile))
  #os.system("circo -Tpng %s -o %s_circo"%(tmp_dot_file, outfile))
  #os.system("fdp -Tpng %s -o %s_fdp"%(tmp_dot_file, outfile))
  #os.system("sfdp -Tpng %s -o %s_sfdp"%(tmp_dot_file, outfile))

if __name__ == "__main__":
  main()

