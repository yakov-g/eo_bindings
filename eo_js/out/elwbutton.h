/**
 * generated from "/tmp/evas_py/l/elwbutton.xml"
 */
#ifndef _JS_ELWBUTTON_H_
#define _JS_ELWBUTTON_H_

#include "elm.h" //kinda supporting functions
#include "CElmObject.h" //base object
#include "elw_button.h" //eo-class include file
#include "evasobject.h" //include generated js-wrapping classes
#include "elwalert.h" //include generated js-wrapping classes

namespace elm { //namespace should have the same meaning as module for python

using namespace v8;

class ElwButton : public virtual CElmObject, public virtual EvasObject, public virtual ElwAlert {
private:
   static Persistent<FunctionTemplate> tmpl;

protected:
   ElwButton();
   ElwButton(Local<Object> _jsObject, CElmObject *parent);
   static Handle<FunctionTemplate> GetTemplate();

   struct {
      Persistent<Value> _event_ev_clicked;
   } cb;

   virtual ~ElwButton();

public:
   static void Initialize(Handle<Object> target);
   virtual void DidRealiseElement(Local<Value> obj);
   friend Handle<Value> CElmObject::New<ElwButton>(const Arguments& args);


   Handle<Value> ev_clicked_get() const;
   void ev_clicked_set(Handle<Value> val);
   void ev_clicked(void *event_info);
   staic Eina_Bool ev_clicked_wrapper(void *data, Eo *obj, const Eo_Event_Description *desc, void *event_info);

   Handle<Value> text_set(const Arguments&);

}; //end class

/* properties callbacks */

/* properties(events) callbacks */
   Handle<Value> Callback_ev_clicked_get(Local<String>, const AccessorInfo &info);
   void Callback_ev_clicked_set(Local<String>, Local<Value> val, const AccessorInfo &info);

/* methods callbacks */
   Handle<Value> Callback_text_set(const Arguments&);

} //end namespace elm

#endif
