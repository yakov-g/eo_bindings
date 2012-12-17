
cdef extern from *:
    ctypedef char* const_char_ptr "const char*"

cdef extern from "Eina.h":
    ctypedef unsigned char Eina_Bool
    Eina_Bool EINA_FALSE
    Eina_Bool EINA_TRUE

cdef extern from "Eo.h":

    ####################################################################
    # Basic Types
    #

    ctypedef int Evas_Coord
    ctypedef int Evas_Angle
    ctypedef int Evas_Font_Size
    ctypedef int Eo_Op
    ctypedef short Eo_Callback_Priority

    ctypedef struct Eo
    ctypedef struct Eo_Class

    ctypedef struct Eo_Event_Description:
       char *name
       char *type
       char *doc

    Eo_Op EO_BASE_BASE_ID

    Eo_Event_Description * EO_EV_CALLBACK_ADD
    Eo_Event_Description * EO_EV_CALLBACK_DEL
    Eo_Event_Description * EO_EV_FREE
    Eo_Event_Description * EO_EV_DEL

    ctypedef enum:
      EO_BASE_SUB_ID_DATA_GET
      EO_BASE_SUB_ID_DATA_DEL

    ctypedef void (*Eo_Event_Cb)(void *data, Eo *obj,
                                   Eo_Event_Description *desc, 
                                   void *event_info)
    ctypedef void (*eo_base_data_free_func)(void *p)

    cdef short EO_CALLBACK_PRIORITY_BEFORE
    cdef short EO_CALLBACK_PRIORITY_DEFAULT
    cdef short EO_CALLBACK_PRIORITY_AFTER

    Eina_Bool eo_init()
    Eo_Class *eo_base_class_get()

    Eo* eo_add(Eo_Class *klass, Eo *parent)
    Eo* eo_add_custom(Eo_Class *klass, Eo *parent, ...)

    Eo* eo_ref(Eo *obj)
    void eo_unref(Eo *obj)
    int eo_ref_get(Eo *obj)
    void eo_del(Eo *obj)

    Eo *eo_parent_get(Eo *obj)

    Eo_Class *eo_class_get(Eo *obj)
    char *eo_class_name_get(Eo_Class *klass)

    void *eo_data_get(Eo *obj, Eo_Class *klass)


    Eina_Bool eo_do(Eo *obj, ...)
    Eina_Bool eo_class_do(Eo_Class *klass, ...)


cdef class EoDefault:
   cdef Eo *eo
   cdef object name
   cdef int print_func_name(self, f_name)
   cdef int _eo_instance_set(self, Eo *eo)
   cpdef _eo_instance_set2(self, unsigned long long klass, EoDefault parent)

cdef Eo* _eo_instance_get(EoDefault pyobj)
cdef Eina_Bool _object_callback(void *data, Eo *o, Eo_Event_Description *desc, void *event_info)



