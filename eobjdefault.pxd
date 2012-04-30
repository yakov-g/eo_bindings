
cdef extern from "Eina.h":
    ctypedef unsigned char Eina_Bool


cdef extern from "Eobj.h":

    ####################################################################
    # Basic Types
    #

    ctypedef int Evas_Coord
    ctypedef int Evas_Angle
    ctypedef int Evas_Font_Size
    ctypedef int Eobj_Op
    ctypedef short Eobj_Callback_Priority

    ctypedef struct Eobj
    ctypedef struct Eobj_Class

    ctypedef struct Eobj_Event_Description:
       char *name
       char *type
       char *doc

    Eobj_Op EOBJ_BASE_BASE_ID


    Eobj_Event_Description * EOBJ_EV_CALLBACK_ADD
    Eobj_Event_Description * EOBJ_EV_CALLBACK_DEL
    Eobj_Event_Description * EOBJ_EV_FREE
    Eobj_Event_Description * EOBJ_EV_DEL
 
    ctypedef enum:
      EOBJ_BASE_SUB_ID_DATA_GET
      EOBJ_BASE_SUB_ID_DATA_DEL

    ctypedef void (*Eobj_Event_Cb)(void *data, Eobj *obj,
                                   Eobj_Event_Description *desc, 
                                   void *event_info)
    ctypedef void (*eobj_base_data_free_func)(void *p)

    cdef short EOBJ_CALLBACK_PRIORITY_BEFORE
    cdef short EOBJ_CALLBACK_PRIORITY_DEFAULT
    cdef short EOBJ_CALLBACK_PRIORITY_AFTER

    Eina_Bool eobj_init()
    Eobj_Class *eobj_base_class_get()

    Eobj* eobj_add(Eobj_Class *klass, Eobj *parent)

    Eobj* eobj_ref(Eobj *obj)
    void eobj_unref(Eobj *obj)
    int eobj_ref_get(Eobj *obj)
    void eobj_del(Eobj *obj)

    Eobj *eobj_parent_get(Eobj *obj)

    Eobj_Class *eobj_class_get(Eobj *obj)
    char *eobj_class_name_get(Eobj_Class *klass)

    void *eobj_data_get(Eobj *obj, Eobj_Class *klass)


    Eina_Bool eobj_do(Eobj *obj, ...)

#    void *eobj_generic_data_set(Eobj *obj, char *key, void *data)
#    void *eobj_generic_data_get(Eobj *obj, char *key)
#    void *eobj_generic_data_del(Eobj *obj, char *key)

#    Eina_Bool eobj_event_callback_add(Eobj *obj,
#                                      Eobj_Event_Description *desc,
#                                      Eobj_Event_Cb func,
#                                      void *user_data)

    Eina_Bool eobj_event_callback_priority_add(Eobj *obj,
                                      Eobj_Event_Description *desc,
                                      Eobj_Callback_Priority priority,
                                      Eobj_Event_Cb func,
                                      void *user_data)

    Eina_Bool eobj_event_callback_del(Eobj *obj,
                                      Eobj_Event_Description *desc,
                                      Eobj_Event_Cb func,
                                      void * data)
    
#    Eina_Bool eobj_event_callback_del_lazy(Eobj *obj,
#                                      Eobj_Event_Description *desc,
#                                      Eobj_Event_Cb func)


    Eina_Bool eobj_event_callback_call(Eobj *obj,
                                       Eobj_Event_Description *desc,
                                       void *event_info)

cdef extern from "Elementary.h":
   int elm_init(int argc, char **argv) 
   void elm_run()


cdef class EobjDefault:
   cdef Eobj *eobj
   cdef object _callbacks
   cdef object name
   cdef int print_func_name(self, f_name)
   cdef int _eobj_instance_set(self, Eobj *eobj)
   cpdef _eobj_instance_set2(self, klass, EobjDefault parent)
   

cdef Eobj* _eobj_instance_get(EobjDefault pyobj)


