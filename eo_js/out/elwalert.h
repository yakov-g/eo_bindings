########################################################
##
## generated from from "/tmp/evas_py/l/elwalert.xml"
##
########################################################

#ifndef _JS_ELWALERT_H_
#define _JS_ELWALERT_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_alert.h" //eo-class include file

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwAlert : public virtual CElmObject {
private:
protected:
   ElwAlert();
   virtual ~ElwAlert();
public:

cdef extern from "elw_alert.h":

  Eo_Op ELW_ALERT_BASE_ID


  ctypedef enum:
    ELW_ALERT_SUB_ID_ALERT

  Eo_Class* elw_alert_interface_get()

}; //end class

} //end namespace elm

#endif

