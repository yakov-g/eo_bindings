########################################################
##
## generated from from "/home/yakov/eobj/python/Mixin3.xml"
##
########################################################

from eobjdefault cimport *

cdef extern from "/home/yakov/eobj/examples/mixin/mixin3.h":

  ctypedef struct Mixin3_Public_Data:
    int count

  Eobj_Class* mixin3_class_get()

