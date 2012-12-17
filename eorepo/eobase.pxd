########################################################
##
## generated from ""
##
########################################################
from eorepo.eodefault cimport *

cimport eorepo.eodefault as eodefault

cdef extern from "Eo.h":

  Eo_Op EO_BASE_BASE_ID

  ctypedef enum:
    EO_BASE_SUB_ID_WREF_DEL,
    EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE,
    EO_BASE_SUB_ID_EVENT_CALLBACK_FORWARDER_DEL,
    EO_BASE_SUB_ID_EVENT_GLOBAL_THAW,
    EO_BASE_SUB_ID_EVENT_CALLBACK_DEL,
    EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET,
    EO_BASE_SUB_ID_DATA_SET,
    EO_BASE_SUB_ID_EVENT_THAW,
    EO_BASE_SUB_ID_WREF_ADD,
    EO_BASE_SUB_ID_DESTRUCTOR,
    EO_BASE_SUB_ID_DATA_GET,
    EO_BASE_SUB_ID_DATA_DEL,
    EO_BASE_SUB_ID_CONSTRUCTOR,
    EO_BASE_SUB_ID_EVENT_CALLBACK_CALL,
    EO_BASE_SUB_ID_EVENT_FREEZE_GET,
    EO_BASE_SUB_ID_EVENT_FREEZE,
    EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD,
    EO_BASE_SUB_ID_EVENT_CALLBACK_FORWARDER_ADD


  Eo_Class* eo_base_class_get()

  Eo_Event_Description * EO_EV_CALLBACK_DEL
  Eo_Event_Description * EO_EV_DEL
  Eo_Event_Description * EO_EV_CALLBACK_ADD

