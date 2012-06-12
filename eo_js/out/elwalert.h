/**
 * generated from "/tmp/evas_py/l/elwalert.xml"
 */
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


   Handle<Value> alert(const Arguments&);

}; //end class

/* properties callbacks */

/* properties(events) callbacks */

/* methods callbacks */
   Handle<Value> Callback_alert(const Arguments&);

} //end namespace elm

#endif
