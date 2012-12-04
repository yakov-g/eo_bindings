cimport eodefault
import sys, operator


##########################################################
##
## Wrapping for Elementary functions
##

PRIORITY_BEFORE = eodefault.EO_CALLBACK_PRIORITY_BEFORE
PRIORITY_DEFAULT = eodefault.EO_CALLBACK_PRIORITY_DEFAULT
PRIORITY_AFTER = eodefault.EO_CALLBACK_PRIORITY_AFTER
CALLBACK_STOP = 12345

#cdef const_char_ptr py_eo = <const_char_ptr>"python-ej"


def init():
    return bool(eodefault.eo_init())

def elem_run():
   eodefault.elm_run()

def py_elm_init(argv):
    cdef void *p
#    s = " ".join(argv)
#    cdef char *cstr
#    cdef char **p_cstr
#    cstr = <char*>s
#    print "cstr = ", cstr
#    c_csrt = <char**>cstr
#    print "p_cstr[0] = ", p_cstr[0]
    p = NULL
    return <int>(eodefault.elm_init(len(argv), NULL))

#########################################################

cdef Eo *_eo_instance_get(EoDefault pyobj):
    """
if x is a Python object, (x is None) and (x is not None) are very efficient because they translate directly to C pointer comparisons.
Whereas (x == None) and (x != None), or simply using x as a boolean value (as in if x: ...) will invoke Python operations and therefore be much slower.
"""
    if pyobj is not None:
        return pyobj.eo
    else:
        NULL

def pytext_to_utf8(text):

    if not isinstance(text, basestring):
      raise TypeError("Argument '%s' has incorrect type (expected %s, got %s)"%("text",  "basestring", type(text).__name__))
    utf8_data = ""

    if isinstance(text, unicode):
        utf8_data = text.encode('UTF-8')
    elif isinstance(text, str):
        utf8_data = text

    return utf8_data

#===========

cdef class EoDefault:

   PY_EO_NAME = "python-eo"
   def __cinit__(self):
      self.eo = NULL

   def __dealloc__(self):
       cdef Eo *eo
       #self.print_func_name("__dealloc__base__")

       eo = self.eo
       if eo == NULL:
         return
       #eodefault._eo_instance_get(self)
       eodefault.eo_do(eo, eodefault.EO_BASE_BASE_ID + eodefault.EO_BASE_SUB_ID_DATA_DEL, <const_char_ptr>EoDefault.PY_EO_NAME)
       eodefault.eo_unref(eo)
       self.eo = NULL

   # eo_del()
   def delete(self):
      self.ref()
      eodefault.eo_del(self.eo)

   # eo_ref()
   def ref(self):
      eodefault.eo_ref(self.eo)
      return self

   def unref(self):
      eodefault.eo_unref(self.eo)

   # eo_ref_get()
   def ref_get(self):
      ref_count = <object>eodefault.eo_ref_get(self.eo)
      return ref_count

   # eo_parent_get()
   def parent_get(self):
      cdef Eo * parent
      cdef void * data
      parent = eodefault.eo_parent_get(self.eo)
      eodefault.eo_do(parent, eodefault.EO_BASE_BASE_ID+eodefault.EO_BASE_SUB_ID_DATA_GET, <const_char_ptr>EoDefault.PY_EO_NAME, &data)
      obj = <object>data
      return obj

   # eo_class_name_get()
   def class_name_get(self):
      name = eodefault.eo_class_name_get(eodefault.eo_class_get(self.eo))
      return name

   def name_get(self):
      return self.name
   #this func can be called only from this (c-styled)module
   cdef int _eo_instance_set(self, Eo *eo):
       assert self.eo == NULL, "Object must be clean"
       self.eo = eo
       self.name = self.__class__.__name__

   # this func is main routine to add new object
   # using default constructor
   # and connect C and Py objects
   cpdef _eo_instance_set2(self, unsigned long long _kl, EoDefault p):
       cdef Eo_Class *kl = <Eo_Class*>_kl
       cdef Eo *o = eodefault.eo_add(kl, eodefault._eo_instance_get(p))
       self._eo_instance_set(o)
       self._data_set(EoDefault.PY_EO_NAME, self)

   # this func can be called outside(this c-styled module), because receives Eo* as long.
   # it was added to be able to call eo_add_custom with different params
   # and connect C and Py objects after it
   def _eo_instance_set3(self, unsigned long long _eo):
       cdef Eo *o = <Eo*>_eo
       self._eo_instance_set(o)
       self._data_set(EoDefault.PY_EO_NAME, self)

   cdef int print_func_name(self, f_name):
       print self.__class__, " :: ", f_name, " :: ", sys.getsizeof(self)

#================================================================

cdef Eina_Bool _object_callback(void *data, Eo *o,
                           Eo_Event_Description *desc, void *event_info):
   cdef EoDefault obj
   cdef void *p

#passing "this" object to callback function
   cdef void * c_py_obj
   eodefault.eo_do(o, eodefault.EO_BASE_BASE_ID+eodefault.EO_BASE_SUB_ID_DATA_GET, <const_char_ptr>EoDefault.PY_EO_NAME, &c_py_obj)
   py_obj = <object>c_py_obj

   #cb_struct is tuple: (func, data)
   cb_struct = <object>data
   f = cb_struct[0]
   cb_data = cb_struct[1]
   res = f(py_obj, cb_data)

   if res == CALLBACK_STOP:
     return EINA_FALSE
   else:
     return EINA_TRUE


