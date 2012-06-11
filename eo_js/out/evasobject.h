########################################################
##
## generated from from "/tmp/evas_py/l/evasobject.xml"
##
########################################################

#ifndef _JS_EVASOBJECT_H_
#define _JS_EVASOBJECT_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "evas_obj.h" //eo-class include file

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class EvasObject : public virtual CElmObject {
private:
protected:
   EvasObject();
   virtual ~EvasObject();
public:

cdef extern from "evas_obj.h":

  Eo_Op EVAS_OBJ_BASE_ID


  ctypedef enum:
    EVAS_OBJ_SUB_ID_COLOR_SET,
    EVAS_OBJ_SUB_ID_LONGLONGS,
    EVAS_OBJ_SUB_ID_PAR_BY_REF,
    EVAS_OBJ_SUB_ID_COLOR_GET,
    EVAS_OBJ_SUB_ID_LONGS,
    EVAS_OBJ_SUB_ID_VISIBILITY_SET,
    EVAS_OBJ_SUB_ID_INTS,
    EVAS_OBJ_SUB_ID_CHILD_ADD,
    EVAS_OBJ_SUB_ID_SIZE_SET,
    EVAS_OBJ_SUB_ID_NO_PAR,
    EVAS_OBJ_SUB_ID_POSITION_SET,
    EVAS_OBJ_SUB_ID_GEOMETRY_GET,
    EVAS_OBJ_SUB_ID_FLOATS

  Eo_Class* evas_object_class_get()

}; //end class

} //end namespace elm

#endif

