########################################################
##
## generated from from "/home/yakov/eobj/python/EobjBase.xml"
##
########################################################

cimport eobjbase
cimport eobjdefault

from cpython cimport PyObject, Py_INCREF, Py_DECREF

from eobjdefault import EobjDefault

cdef int eobjbase_sub_id(int sub_id):
  return eobjbase.EOBJ_BASE_BASE_ID + sub_id

class EobjBase(EobjDefault,):

  generic_data = {} 

  def wref_del(self):
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjbase_sub_id(eobjbase.EOBJ_BASE_SUB_ID_WREF_DEL))
  
  def callback_eobj_ev_callback_del_del(self, func):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_CALLBACK_DEL
    self._object_callback_del(id_desc, func)
  
  def data_set(self, _key, _data, _free_func = None):

    #if type(_data) is list:
    #  self.generic_data[_key] = _data[:]
    #else:
    #  self.generic_data[_key] = _data
    #_data = self.generic_data[_key]

    #print "arr addr: %x"%<long>(<void*>self.generic_data[_key])
    #print "data addr: %x"%<long>(<void*>_data)

   # Py_INCREF(_data)
    #cdef PyObject *obj = <PyObject *>_data
    #print obj.ob_refcnt

    cdef char* key = <char*> _key
    cdef void* data = <void*> _data

    assert _free_func == None, "_free_func should be None"
    cdef void *tmp = NULL if _free_func is None else <void*>_free_func
    assert tmp == NULL, "_free_func should be null"
    cdef eobj_base_data_free_func free_func = <eobj_base_data_free_func> tmp
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjbase_sub_id(eobjbase.EOBJ_BASE_SUB_ID_DATA_SET), key, data, free_func)
  
  def callback_eobj_ev_del_add(self, priority, func, *args, **kwargs):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_DEL
    self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)
  
  def wref_add(self):
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjbase_sub_id(eobjbase.EOBJ_BASE_SUB_ID_WREF_ADD))
  
  def callback_eobj_ev_callback_del_add(self, priority, func, *args, **kwargs):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_CALLBACK_DEL
    self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)
  
  def callback_eobj_ev_callback_add_del(self, func):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_CALLBACK_ADD
    self._object_callback_del(id_desc, func)
  
  def __init__(self, EobjDefault parent):
    instantiateable = False
    if not instantiateable:
      print "Class '%s' is not instantiate-able. Aborting."%(self.__class__.__name__)
      exit()
  
  
  def data_get(self, _key):
    cdef char* key = <char*> _key
    cdef void* data
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjbase_sub_id(eobjbase.EOBJ_BASE_SUB_ID_DATA_GET), key, &data)
    #print "data get: %x"%(<long>data)
    data_ = None if data == NULL else <object>data
    #return self.generic_data[_key]
    return (data_)
  
  def data_del(self, _key):
    cdef char* key = <char*> _key
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjbase_sub_id(eobjbase.EOBJ_BASE_SUB_ID_DATA_DEL), key)
  
  def callback_eobj_ev_callback_add_add(self, priority, func, *args, **kwargs):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_CALLBACK_ADD
    self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)
  
  def callback_eobj_ev_free_add(self, priority, func, *args, **kwargs):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_FREE
    self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)
  
  def callback_eobj_ev_free_del(self, func):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_FREE
    self._object_callback_del(id_desc, func)
  
  def callback_eobj_ev_del_del(self, func):
    cdef long id_desc = <long>eobjbase.EOBJ_EV_DEL
    self._object_callback_del(id_desc, func)
  
