cimport eobjdefault
import sys
import operator

##########################################################
##
## Wrapping for Elementary functions
##

PRIORITY_BEFORE = eobjdefault.EOBJ_CALLBACK_PRIORITY_BEFORE
PRIORITY_DEFAULT = eobjdefault.EOBJ_CALLBACK_PRIORITY_DEFAULT
PRIORITY_AFTER = eobjdefault.EOBJ_CALLBACK_PRIORITY_AFTER

def init():
    return bool(eobjdefault.eobj_init())

def elem_run():
   eobjdefault.elm_run()

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
    return <int>(eobjdefault.elm_init(len(argv), NULL))

#########################################################

cdef Eobj *_eobj_instance_get(EobjDefault pyobj):
    """ 
if x is a Python object, (x is None) and (x is not None) are very efficient because they translate directly to C pointer comparisons.
Whereas (x == None) and (x != None), or simply using x as a boolean value (as in if x: ...) will invoke Python operations and therefore be much slower.
"""
    if pyobj is not None:
        return pyobj.eobj
    else:
        NULL

def pytext_to_utf8(text):	
    utf8_data = ""

    if isinstance(text, unicode):
        utf8_data = text.encode('UTF-8')
    elif isinstance(text, str):
        utf8_data = text
    else:
        print "Error typecheck"

    return utf8_data

#FIXME: is there another way to cast range of Python int(uint, long) to the range of C int(uint ,long) ???
def cast_pytypesize_to_ctypesize(py_par, type_from_c):
    if type_from_c == 'int':
            return py_par
    elif type_from_c == 'unsigned int':
        return py_par
    elif type_from_c == 'char*':
        if isinstance(py_par, unicode):
            return py_par.encode('UTF-8')
        elif isinstance(py_par, str):
            return py_par

#===========

cdef class EobjDefault:

   def __cinit__(self):
      self._callbacks = {}

   def __dealloc__(self):
       cdef Eobj *eobj
       self.print_func_name("__dealloc__base__")

       eobj = self.eobj

       if eobj == NULL:
         return
       _object_unregister_callbacks(self)

       eobjdefault.eobj_do(eobjdefault._eobj_instance_get(self), eobjdefault.EOBJ_BASE_BASE_ID + eobjdefault.EOBJ_BASE_SUB_ID_DATA_DEL, <char*>"python-eobj")
       self.eobj = NULL
       eobjdefault.eobj_unref(eobj)
       
   # eobj_del()
   def delete(self):
      self.ref()
      eobjdefault.eobj_del(self.eobj)

   # eobj_ref()
   def ref(self):
      eobjdefault.eobj_ref(self.eobj)
      return self

   # eobj_ref_get()
   def ref_get(self):
      ref_count = <object>eobjdefault.eobj_ref_get(self.eobj)
      return ref_count

   # eobj_parent_get()
   def parent_get(self):
      cdef Eobj * parent
      cdef void * data
      parent = eobjdefault.eobj_parent_get(self.eobj)
      eobjdefault.eobj_do(parent, eobjdefault.EOBJ_BASE_BASE_ID+eobjdefault.EOBJ_BASE_SUB_ID_DATA_GET, <char*>"python-eobj", &data)
      obj = <object>data   
      return obj

   # eobj_class_name_get()
   def class_name_get(self):
      name = eobjdefault.eobj_class_name_get(eobjdefault.eobj_class_get(self.eobj))
      return name

   def name_get(self):
      return self.name

   cdef int _eobj_instance_set(self, Eobj *eobj):
       assert self.eobj == NULL, "Object must be clean"
       self.eobj = eobj
       self.name = self.__class__.__name__
       #eobjdefault.eobj_generic_data_set(eobj, "python-eobj", <void*>self)

   cpdef _eobj_instance_set2(self, _kl, EobjDefault p):
       kl = <long>_kl
       cdef Eobj_Class *kl2 = <Eobj_Class*>kl
       self._eobj_instance_set(eobjdefault.eobj_add(kl2, eobjdefault._eobj_instance_get(p)))


   cdef int print_func_name(self, f_name):
       print self.__class__, " :: ", f_name, " :: ", sys.getsizeof(self)

#================================================================

   def _object_callback_add(self, desc_id, priority, event_conv, func, *args, **kwargs):
      if priority == "default":
         priority = eobjdefault.EOBJ_CALLBACK_PRIORITY_DEFAULT
      
      _object_callback_add_internal(self, desc_id,
                                       priority, event_conv,
                                       func, args, kwargs)


   def _object_callback_del(self, desc_id, func):
      _object_callback_del_internal(self, desc_id, func)


cdef _object_callback_add_internal(EobjDefault obj, long d, short p,
                                            event_conv, func, args, kwargs):

   cdef Eobj_Event_Description *desc
   desc = <Eobj_Event_Description *>d

   if not callable(func):
     raise TypeError("func must be callable")
   if event_conv is not None and not callable(event_conv):
     raise TypeError("event_conv must be None or callable")
   
   ev = intern(desc[0].name)
   lst = obj._callbacks.setdefault(ev, [])
   if not lst:
     eobjdefault.eobj_event_callback_priority_add(obj.eobj, desc, p, <Eobj_Event_Cb>_object_callback, <void*>ev)
   else:
     #explicit call of event EOBJ_EV_CALLBACK_ADD
     eobjdefault.eobj_event_callback_call(obj.eobj, eobjdefault.EOBJ_EV_CALLBACK_ADD, desc) 


   lst.append((<long> d, p, func, event_conv, args, kwargs))
   #sorting by priority
   obj._callbacks[ev] = sorted(lst, key = operator.itemgetter(0))



cdef _object_callback_del_internal(EobjDefault obj, long _d, func):
   cdef Eobj_Event_Description *desc
   desc = <Eobj_Event_Description *>_d

   ev = intern(desc[0].name)
   try:
      lst = obj._callbacks[ev]
   except KeyError, event:
     raise ValueError("Unknown event %r" %ev)

   i = -1
   f = None
   for i, (d, p, f, ec, a, k) in enumerate (lst):
      if func == f:
         break

   if f != func:
      raise ValueError("Callback %s was not registered with event: %r"
                        %(func, ev))

   lst.pop(i)
   
   if lst:
     eobjdefault.eobj_event_callback_call(obj.eobj, eobjdefault.EOBJ_EV_CALLBACK_DEL, desc) 
     return

   obj._callbacks.pop(ev)
   eobjdefault.eobj_event_callback_del(obj.eobj, desc, <Eobj_Event_Cb>_object_callback, <void*>ev)
   #eobjdefault.eobj_event_callback_del_lazy(obj.eobj, desc, _object_callback)  


"""
In case when callback is added:
   1. Python function, added for callback, is saved in instance of
      Py object it's added to.
   2. For each event _object_callback() function is added to C object.
      Event name is transfered as data.
   3. In case of event on C side, _object_callback() function with event name as      data is called. Which, in it's turn, looks for and calls appropriate 
      python function, saved in Py object
"""
cdef void _object_callback(void *data, Eobj *o,
                           Eobj_Event_Description *desc, void *event_info):
   cdef EobjDefault obj
   cdef object event
   cdef void *p

   eobjdefault.eobj_do(o, eobjdefault.EOBJ_BASE_BASE_ID+eobjdefault.EOBJ_BASE_SUB_ID_DATA_GET, <char*>"python-eobj",&p)
   obj = <EobjDefault>p   

   event = <object>data
   lst = tuple(obj._callbacks[event])

   for  d, priority, func, event_conv, args, kwargs in lst:
     if event_conv is None:
       func(obj, *args, **kwargs)
     else:
       ei = None if event_info == NULL else event_conv(<long>event_info)
       func(obj, ei, *args, **kwargs)
     if "__stop__" in kwargs:
       break


cdef int _object_unregister_callbacks(EobjDefault o):
  cbs = dict(o._callbacks)
  for key in cbs:
    ev = intern(key)
    lst = o._callbacks[ev][:]
    for i, (d, p, f, ec, a, k) in enumerate(lst):
     _object_callback_del_internal(o, <long>d, f)
  return 1



