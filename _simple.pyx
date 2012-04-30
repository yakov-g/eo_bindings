########################################################
##
## generated from from "/home/yakov/eobj/python/Simple.xml"
##
########################################################

cimport simple
cimport eobjdefault

from eobjbase import EobjBase

cdef int simple_sub_id(int sub_id):
  return simple.SIMPLE_BASE_ID + sub_id

def ev_conv(_addr):
   if _addr is None:
     return None

   addr = <long>_addr
   cdef void * data = <void*>addr
   res = (<int*>data)[0]
   return res
  

class Simple(EobjBase,):

  def callback_sig_a_changed_add(self, priority, func, *args, **kwargs):
    cdef unsigned int id_desc = <unsigned int>simple.SIG_A_CHANGED
    self._object_callback_add(id_desc, priority, ev_conv, func, *args, **kwargs)
 #   self._object_callback_add(id_desc, priority, None, func, *args, **kwargs)
  
  def a_set(self, _a):
    cdef int a = <int> _a
    eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), simple_sub_id(simple.SIMPLE_SUB_ID_A_SET), a)
  
  def __init__(self, EobjDefault parent):
    instantiateable = True
    if not instantiateable:
      print "Class '%s' is not instantiate-able. Aborting."%(self.__class__.__name__)
      exit()
    klass = <long>simple.simple_class_get()
    self._eobj_instance_set2(klass, parent)
    self.data_set("python-eobj", self, None)
  
  
  def callback_sig_a_changed_del(self, func):
    cdef unsigned int id_desc = <unsigned int>simple.SIG_A_CHANGED
    self._object_callback_del(id_desc, func)
  
