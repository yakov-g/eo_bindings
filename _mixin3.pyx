########################################################
##
## generated from from "/home/yakov/eobj/python/Mixin3.xml"
##
########################################################

cimport mixin3
cimport eobjdefault

from mixin import Mixin

class Mixin3(Mixin,):

  def __init__(self, EobjDefault parent):
    instantiateable = False
    if not instantiateable:
      print "Class '%s' is not instantiate-able. Aborting."%(self.__class__.__name__)
      exit()
  
  def _count_set(self, value):
    cdef Mixin3_Public_Data *_data
    _data = <Mixin3_Public_Data *>eobjdefault.eobj_data_get(eobjdefault._eobj_instance_get(self), mixin3.mixin3_class_get());
    _data[0].count = value

  def _count_get(self):
    cdef Mixin3_Public_Data *_data
    _data = <Mixin3_Public_Data *>eobjdefault.eobj_data_get(eobjdefault._eobj_instance_get(self), mixin3.mixin3_class_get());
    return _data[0].count

  def _count_del(self):
    del self.count

  count2 = property(_count_get, _count_set, _count_del)
