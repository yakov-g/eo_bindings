########################################################
##
## generated from from "/home/yakov/eobj/python/Mixin2.xml"
##
########################################################

from eobjdefault cimport *

cdef extern from "/home/yakov/eobj/examples/mixin/mixin2.h":

  ctypedef struct Mixin2_Public_Data:
    int count


  Eobj_Class* mixin2_class_get()

