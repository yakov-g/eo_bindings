########################################################
##
## generated from from "/home/yakov/eobj/python/Mixin2.xml"
##
########################################################

cimport mixin2
cimport eobjdefault

from mixin import Mixin

class Mixin2(Mixin,):

  _count = 12345
  def __init__(self, EobjDefault parent):
    instantiateable = False
    if not instantiateable:
      print "Class '%s' is not instantiate-able. Aborting."%(self.__class__.__name__)
      exit()
  
  def _count_set(self, value):
    cdef Mixin2_Public_Data *_data, data
    _data = <Mixin2_Public_Data *>eobjdefault.eobj_data_get(eobjdefault._eobj_instance_get(self), mixin2.mixin2_class_get());
    _data[0].count = value


  def _count_get(self):
    cdef Mixin2_Public_Data *_data, data
    _data = <Mixin2_Public_Data *>eobjdefault.eobj_data_get(eobjdefault._eobj_instance_get(self), mixin2.mixin2_class_get());
    data = _data[0]
    return _data[0].count
    return self._count

  def _count_del(self):
    del self._count

  count = property(_count_get, _count_set, _count_del, "I'm the 'x' property.")
