########################################################
##
## generated from from "/home/yakov/xml/base/EoBase.xml"
##
########################################################

cimport eobase as eobase
from eodefault import EoDefault

from cpython cimport Py_INCREF, Py_DECREF

from eorepo.eodefault import pytext_to_utf8

cdef int eobase_sub_id(int sub_id):
  return eobase.EO_BASE_BASE_ID + sub_id

class EoBase(EoDefault):

  CALLBACK_DEL = <long>eobase.EO_EV_CALLBACK_DEL
  DEL = <long>eobase.EO_EV_DEL
  CALLBACK_ADD = <long>eobase.EO_EV_CALLBACK_ADD

  def event_thaw(self):
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_THAW))
  
  def event_freeze(self):
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_FREEZE))
  
  def __init__(self, EoDefault parent):
    instantiateable = False
    if not instantiateable:
      print "Class '%s' is not instantiate-able. Aborting."%(self.__class__.__name__)
      exit(1)
  
  
  @staticmethod
  def event_global_freeze_get():
    cdef int fcount
    eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE_GET), &fcount)
    fcount_ = <object>fcount
    return (fcount_)
  

  @staticmethod
  def event_global_freeze():
    eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_FREEZE))
  

  def data_get(self, object _key):
    _key = None if _key is None else pytext_to_utf8(_key)
    cdef char* key =  NULL if _key is None else <char*> _key
    cdef void* data
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_GET), key, &data)
    data_ = None if data == NULL else <object>data
    return (data_)
  
  def event_callback_del(self, long _desc, object _func):
    cdef Eo_Event_Cb func = <Eo_Event_Cb> eodefault._object_callback
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_DEL), _desc, func, <void*>_func)
    Py_DECREF(_func)
  

  

  def event_freeze_get(self):
    cdef int fcount
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_FREEZE_GET), &fcount)
    fcount_ = <object>fcount
    return (fcount_)
  
  @staticmethod
  def event_global_thaw():
    eodefault.eo_class_do(eobase.eo_base_class_get(), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_GLOBAL_THAW))
  

  def data_del(self, object _key):
    _key = None if _key is None else pytext_to_utf8(_key)
    cdef char* key =  NULL if _key is None else <char*> _key
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_DEL), key)
  
  def event_callback_call(self, long _desc, object _event_info):
    cdef long desc = <long> _desc
    cdef void* event_info = <void*> _event_info
    cdef unsigned char aborted
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_CALL), desc, event_info, &aborted)
    aborted_ = <object>aborted
    return (aborted_)
  
  def event_callback_priority_add(self, long _desc, int _priority, object _cb):
    if not callable(_cb[0]):
      raise TypeError("func must be callable")
    cdef Eo_Event_Cb cb = <Eo_Event_Cb> eodefault._object_callback
    Py_INCREF(_cb)
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_EVENT_CALLBACK_PRIORITY_ADD), _desc, _priority, cb, <void*>_cb)
  

  def data_set(self, object _key, object _data):
    _key = pytext_to_utf8(_key)
    cdef char* key = <char*> _key
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)
  
  def _data_set(self, object _key, object _data):
    _key = pytext_to_utf8(_key)
    cdef char* key = <char*> _key
    eodefault.eo_do(eodefault._eo_instance_get(self), eobase_sub_id(eobase.EO_BASE_SUB_ID_DATA_SET), key, <void*>_data, NULL)
  


