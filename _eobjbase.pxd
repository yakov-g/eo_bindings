########################################################
##
## generated from from "/home/yakov/eobj_test/python/Simple.xml"
##
########################################################

from eobjdefault cimport *

cdef extern from "/home/yakov/eobj/lib/Eobj.h":

  Eobj_Op EOBJ_BASE_BASE_ID

  Eobj_Event_Description * EOBJ_EV_CALLBACK_ADD
  Eobj_Event_Description * EOBJ_EV_CALLBACK_DEL
  Eobj_Event_Description * EOBJ_EV_FREE
  Eobj_Event_Description * EOBJ_EV_DEL

  ctypedef enum:
    EOBJ_BASE_SUB_ID_DATA_SET,
    EOBJ_BASE_SUB_ID_DATA_GET,
    EOBJ_BASE_SUB_ID_DATA_DEL

  Eobj_Class* eobj_base_class_get()
