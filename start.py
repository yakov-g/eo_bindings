from XMLparser import XMLparser
from Cparser import Cparser
from optparse import OptionParser
import getopt, sys

def test(a, b):
    if a == b:
        print "ok"
    else:
        print "test failed"


parser = OptionParser()
parser.add_option("-f", "--filename", dest="filename",
                  action="append", help="source file to parse")
parser.add_option("-i", "--include", dest="include",
                  action="append", help="other modules to include")
parser.add_option("-s", "--source", dest="filename",
                 action="append", help="source file to parse")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")


(options, args) = parser.parse_args()

print "start.py :", options


verbose = False
filename = ""

if options.filename == None:
    print "No source file was provided"
else:
   filename = options.filename

for f in filename:

  if f.find(".c") != -1 or f.find(".h") != -1:
    cp = Cparser() 
    if options.include == None:
      print "At least one object should be included"
      exit()
    cp.parse(f, options)
    del cp

  elif f.find(".xml") != -1:
    xp = XMLparser()
    xp.parse(f)
    xp.testall()
    xp.build_module()
    del xp

