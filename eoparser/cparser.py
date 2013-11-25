import xml.parsers.expat
import sys, os, re, json

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from string import capwords
from helper import normalize_names
from helper import _const
from collections import OrderedDict

const = _const()

LOCAL_CPARSER = True

#filter func to throw out from comment everything
#but the @def, @param
def macro_filter_func(l):
  l = " ".join(l.split()) #removing more than one spaces
  if "@def" in l or "@param" in l:
    return True
  else:
    return False

print_flag = False
def verbose_print(mes):
  if print_flag:
    print mes

class Cparser(object):
  def __init__(self, _print_flag):
    global print_flag
    print_flag = _print_flag
    self.cl_data = {}
    self.cl_incl = {}
    self.eapi_func_ret_type_hash = {}
    self.all_eo_funcs_hash = {}

    self.outdir = ""
    self.typedefs = {"Evas_Coord" : "int",
                     "Evas_Angle":"int",
                     "Evas_Font_Size" : "int",
                     "Evas_Object" : "Eo",
                     "Evas_Smart" : "Eo",
                     "Evas_Map" : "Eo",
                     "Evas_Text_Style_Type" : "int",#enum
                     "Evas_Colorspace" : "int",#enum
                     "Evas_Render_Op" : "int",#enum
                     "Evas_Aspect_Control" : "int",#enum
                     "Evas_Object_Pointer_Mode" : "int", #enum
                     "Evas_Image_Scale_Hint" : "int", #enum
                     "Evas_Image_Content_Hint" : "int", #enum
                     "Evas_Image_Animated_Loop_Hint" : "int", #enum
                     "Evas_Border_Fill_Mode" : "int", #enum
                     "Evas_Object_Table_Homogeneous_Mode" : "int", #enum
                     "Evas_Textgrid_Font_Style" : "int",
                     "Evas_Textgrid_Palette" : "int",
                     "Evas_Modifier_Mask" : "unsigned long long",
                     "Evas_Button_Flags" : "int",
                     "Evas_Fill_Spread" : "int",
                     "Evas_Event_Flags" : "int",
                     "Evas_Font_Hinting_Flags" : "int",
                     "Evas_Load_Error" : "int",
                     "Elm_Photocam_Zoom_Mode" : "int",
                     "Eina_Bool" : "bool",
                     "Elm_Bg_Option" : "int",
                     "Elm_Fileselector_Mode" : "int",
                     "Elm_Object_Select_Mode" : "int",
                     "Elm_Actionslider_Pos" : "int",
                     "Elm_Web_Zoom_Mode" : "int",
                     "Elm_Icon_Type" : "int",
                     "Elm_Colorselextor_Mode" : "int",
                     "Elm_List_Mode" : "int",
                     "Elm_Image_Orient"  : "int",
                     "Elm_Map_Route_Type" : "int",
                     "Elm_Map_Zoom_Mode" : "int",
                     "Elm_Map_Source_Type" : "int",
                     "Elm_Clock_Edit_Mode" : "int",
                     "Elm_Dayselector_Day" : "int",
                     "Elm_Thumb_Animation_Setting" : "int",
                     "Elm_Win_Keyboard_Mode" : "int",
                     "Elm_Toolbar_Shrink_Mode" : "int",
                     "Elm_Icon_Lookup_Order" : "int",
                     "Elm_Datetime_Field_Type" : "int",
                     "Elm_Gesture_Type" : "int",
                     "Evas_BiDi_Direction" : "int",
                     "Elm_Bubble_Pos" : "int",
                     "Ecore_X_Window" : "unsigned int",

                     "Elm_Flip_Interaction" : "int",
                     "Elm_Flip_Direction" : "int",
                     "Elm_Flip_Interaction" : "int",
                     "Elm_Flip_Mode" : "int",
                     "Elm_Calendar_Weekday" : "int",
                     "Elm_Calendar_Selectable" : "int",
                     "Elm_Calendar_Weekday" : "int",
                     "Elm_Calendar_Select_Mode" : "int",
                     "Elm_Illume_Command" : "int",
                     "Elm_Win_Keyboard_Mode" : "int",
                     "Elm_Win_Indicator_Opacity_Mode" : "int",
                     "Elm_Win_Indicator_Mode" : "int",
                     "Ecore_Wl_Window" : "int",
                     "Elm_GLView_Render_Policy" : "int",
                     "Elm_GLView_Mode" : "int",
                     "Elm_Panel_Orient" : "int",
                     "Elm_Popup_Orient" : "int",
                     "Elm_Wrap_Type" : "int",
                     "Elm_Cnp_Mode" : "int",
                     "Elm_Input_Panel_Lang" : "int",
                     "Elm_Text_Format" : "int",
                     "Elm_Input_Panel_Return_Key_Type" : "int",
                     "Elm_Wrap_Type" : "int",
                     "Elm_Autocapital_Type" : "int",
                     "Elm_Text_Format" : "int",
                     "Elm_Object_Select_Mode" : "int",
                     "Elm_List_Mode" : "int",
                     "Eo_Callback_Priority": "short"}


  #parsing function, to parse typedef file
  def typedefs_xml_parser(self, name, attrs):
      attrs_ascii = {}
      for key, val in attrs.iteritems():
         attrs_ascii[key.encode("ascii")] = val.encode("ascii")

      attrs = attrs_ascii

      if name == "type":
         fr = attrs["from"]
         to = attrs["to"]
         fr = " ".join(fr.split())
         fr = fr.replace(" *", "*")
         to = " ".join(to.split())
         to = to.replace(" *", "*")
         if fr not in self.typedefs:
           self.typedefs[fr] = to
      else:
         pass

  def typedefs_add(self, fName):
     p = xml.parsers.expat.ParserCreate()
     p.StartElementHandler = self.typedefs_xml_parser
     p.ParseFile(open(fName, 'r'))

  #typedef resolving
  # _in - in type
  # Returns resolved type
  def typedef_resolve(self, _in):
    stars = ""

    l = _in.split('*', 1)
    t_tmp = l[0]
    stars += l[1]+'*' if len(l) == 2 else ""

    while t_tmp in self.typedefs:
      t_tmp = self.typedefs[t_tmp]

      l = t_tmp.split('*', 1)
      t_tmp = l[0]
      stars += l[1]+'*' if len(l) == 2 else ""

    return t_tmp + stars

  def _old_signals_get(self, _in_data):
    sig_desc = {}
    sig_names_map = {}

    # looking for constructions like
    # static const char SIG_CLICKED[] = "clicked";
    # and put it into map
    af = _in_data.replace("\n", "")
    reg = "(SIG[\w]*)\[ *\][ ]*= *\"([,\w]*)\";"
    sig_names_list = re.findall(reg, af)
    for k, n in sig_names_list:
       sig_names_map[k] = n

    # looking for constructions like
    # #define SIG_CLICKED "clicked"
    # and put it into map
    reg = "#define *(SIG[\w]*) *\"([^\"]*)\""
    sig_names_list = re.findall(reg, af)
    for k, n in sig_names_list:
       sig_names_map[k] = n

    #looking for Cb_Descriptions array, parse it
    # and change SIG_ variables with it's defines...
    reg = "Evas_Smart_Cb_Description *([\w]*)[][ =]*{([^;]*);"
    sig_desc_list = re.findall(reg, af)
    #if len(sig_list) > 1:
    sig_desc = {}
    for it in sig_desc_list:
       key = it[0]
       data = it[1]
       #print data
       reg = "{([^}]*)}"
       sigs = re.findall(reg, data)
       #print "---------------------"
       arr = []
       for i in sigs:
          (v, c) = smart_split2(i, "\"", "\"")
          v = v.strip();
          c = c.strip();

          if v.find("\"") == -1 and v != "NULL":
             v = sig_names_map[v]
          v = v.strip("\"")
          c = c.strip("\"")
          if v != "NULL":
             arr.append((v, c))
       sig_desc[key] = arr

    return sig_desc

  def c_file_data_get2(self, filename):

    f = open(filename, 'r')
    _in_data = f.read()
    f.close()

    def_list = []
    reg = "EO_DEFINE_CLASS\((.*)\).*"
    def_list += re.findall(reg, _in_data)

  #event_desc structure
  #  EO_DEFINE_CLASS(elm_scrollable_interface_get, &_elm_scrollable_interface_desc, NULL, EVAS_SMART_SCROLLABLE_INTERFACE, NULL);
  #
    cl_name_to_desc_var_name_map = {}
    ev_desc = {"NULL" : []}
    #print "def list: ", def_list
    for s in def_list:
       s = s.replace(" ", "")
       s = s.replace("\n", "")
       l_tmp = s.split(",")

       key = l_tmp[0].strip(" ")
       desc_var = l_tmp[1].strip(" &")
       parent = l_tmp[2]
       l_tmp = l_tmp[3:-1]
       l_tmp = filter(lambda l: False if l == "NULL" else True, l_tmp)

       # map class get func to description variable
       cl_name_to_desc_var_name_map[key] = desc_var

       lst = []
       lst.append(parent) 
       lst += l_tmp
       lst = filter(lambda l: False if l == "NULL" else True, lst)

       self.cl_data[key] = {const.PARENTS:lst,
                            const.FUNCS:{}}
    
  #looking for old styled signals, which begin with
  # SIG_
    sig_list = self._old_signals_get(_in_data)

  #FIXME: this regex must hande case when \" in inside quotes
  #looking for declarations of all events, This can fail, if bracket is used inside
    event_descriptions = {}
    reg = "Eo_Event_Description[ ]*([\w]*)[ =]*EO_(HOT_)*EVENT_DESCRIPTION\(([^\)]*)\);"
    af = _in_data.replace("\n", "")
    ev_list = re.findall(reg, af)
    for key, hot, desc in ev_list:
       event, comment = smart_split2(desc, "\"", "\"")
       event = event.strip().strip("\"")
       comment = comment.strip().strip("\"")
       event_descriptions[key] = (event, comment)

  #event_desc structure
  # { EV_CLICKED, EV_BUTTON_DOWN, EV_BUTTON_UP, NULL  }
  #
    reg = "Eo_Event_Description[ *]*([\w]*)[][ =]*{([^}]*)};"
    af = _in_data.replace("\n", "")
    ev_list = re.findall(reg, af)

    for tup in ev_list:
       key = tup[0]
       lst = tup[1].replace(" ", "").split(",")
       if lst[-1] != "NULL":
         print "ERROR: last event descriptor should be NULL in class %s"%(cl_id)
         exit(1)
       lst = filter(lambda l: False if l == "NULL" else True, lst)
       ev_desc[key] = lst

   #  fetching
   #  op description
   #
    reg = "Eo_Op_Description[ ]*([\w]*)\[\][ =]*{([^}]*)};"
    all_op_descs = re.findall(reg, af)
    op_desc = {"NULL" : []}
    for tup in all_op_descs:
      s_tmp = tup[1]
      # fetching op_ids and descriptions
      # this awful RegEx is for catching comment like this:
      #  "This is comment \" with escaped quotes \" in the middle "
      #  " and next line which should be combined with C preprocessor "
      reg =  "EO_OP_DESCRIPTION[^\)]*\([ ]*([A-Z0-9_]*)[ ]*,([ ]*\"([^\"]*((?<=\\\)\")*)*\"[ ]*[\n]*)+\),"
      # reg =  "EO_OP_DESCRIPTION[^\)]*\([ ]*([A-Z0-9_]*)[ ]*,([ ]*\"([^\"]*)\"[ ]*[\n]*)+\),"
      # reg =  "EO_OP_DESCRIPTION[^\)]*\([ ]*([A-Z0-9_]*)[ ]*,[ ]*\"([^\"]*)\"[ ]*\),"
      ids_and_descs = re.findall(reg, s_tmp)

      op_list = []
      for t in ids_and_descs:
         op_id = t[0] #op_id
         func_name = re.findall("SUB_ID_(.*)", op_id)
         func_name = func_name[0].lower()
         op_list.append((op_id, func_name))

      op_desc[tup[0]] = op_list

###################################################3
    reg = "Eo_Op_Func_Description"
    #reg = "Eo_Op_Func_Description[ ]*([\w]*)\[\][ =]*{([^}]*)};"
    #all_func_descs = re.findall(reg, af)
    #if len(all_func_descs) > 1:
    #   print all_func_descs
    
    buf = _in_data
    func_desc_block = buf.find(reg);

    func_descs = {"NULL" : {}}

    while func_desc_block > 0:
       count = 0
       p = func_desc_block

       desc = ""
       desc_start = desc_end = 0
       desc_start = buf.find("{", func_desc_block)
       desc_end = buf.find("};", desc_start)
       desc = buf[desc_start + 1: desc_end]

       #this is already flag for next iteration
       func_desc_block = buf.find(reg, desc_end)
 
      #ugly but simple way to fetch constructor name
       while p > 0:
          if buf[p] == '}':
            count += 1
          if buf[p] == '{':
            count -= 1
          if count == -1:
             break
          p -= 1

       count = 0
       stop = False
       while p > 0:
          if buf[p] == ')':
            count += 1
          if buf[p] == '(':
            count -= 1
            stop = True
          if ((count == 0) and stop):
             break   
          p -= 1
     
       end_of_constructor_name = p
     
       stop = False
       begin_of_constructor_name = -1
       while p > 0:
          c = buf[p]
          if ((c >= '0' and c <= '9') or (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c == '_')):
             stop = True
          else:
             if stop:
                begin_of_constructor_name = p
                break;
          p -= 1

       if begin_of_constructor_name != -1:     
         res = buf[begin_of_constructor_name : end_of_constructor_name]
         res = res.strip()

         desc = " ".join(desc.split())
         desc = desc.replace("\n", "").strip()
         desc = smart_split(desc)
         desc2 = {}
         for d in desc:
            d = d.replace('(', " ").replace(")", " ").replace(",", " ")
            d = " ".join(d.split())
            d = d.split()
            if (len(d) == 4):
              desc2[d[2]] = d[1]

         func_descs[res] = desc2

    ###
    # Class desc structure:
    # {
    #[0]    EO_VERSION
    #[1]    "Evas_Object_Line",
    #[2]    EO_CLASS_TYPE_REGULAR,
    #[3]    EO_CLASS_DESCRIPTION_OPS(&EVAS_OBJ_LINE_BASE_ID, op_desc, EVAS_OBJ_LINE_SUB_ID_LAST),
    #[4]    NULL,
    #[5]    sizeof(Evas_Object_Line),
    #[6]    _class_constructor,
    #[7]    NULL
    # }
    #
    reg = "Eo_Class_Description[ ]*([\w]*)[ =]*{([^}]*)};"
    desc_list = re.findall(reg, af)
    class_desc = {}

    for tup in desc_list:
       key = tup[0]
       l_tmp = smart_split(tup[1])
       ver = l_tmp[0].strip(" ")
       name = l_tmp[1].strip(" ")
       cl_type = l_tmp[2].strip(" ")
       constr_name = l_tmp[6].strip(" ")
       
       #splitting string into list
       desc_ops = l_tmp[3].replace(" ", "").replace("&", "")
       desc_ops = re.findall("\(([^)]*)\)" , desc_ops)[0].split(",")

       #mapping op_desc var name into ops list
       #if op_desc == NULL; t.e. no op_id for current class; NULL will be changed to empty list
       desc_ops[1] = op_desc[desc_ops[1]]

       ev_desc_var = l_tmp[4].strip(" ")

       if -1 == name.find("\""):
          name = name.strip(" ")
          reg = "#define[ ]*%s[ ]*(\"[^\"]*\")"%name
          ll = re.findall(reg, af)
          if len(ll):
            name = ll[0]

       name = name.strip("\"")

       #check which of OP_IDs present in FUNC_IDs and remove them
       # t.e. only IMPLEMENTED functions will remain
       desc_ops_arr = desc_ops[1]
       for a, b in desc_ops_arr:
          if a in func_descs[constr_name]:
             del func_descs[constr_name][a]
       impl_funcs = func_descs[constr_name]
       del desc_ops_arr

       # here key is name of class_desc variable
       class_desc[key] = {}
       class_desc[key]["name"] = name
       class_desc[key]["cl_type"] = cl_type
       class_desc[key]["op_desc"] = desc_ops
       class_desc[key]["implements"] = impl_funcs
       class_desc[key]["ev_desc"] = ev_desc[ev_desc_var]
    del desc_list, reg

    # matching data form class_desc to class defined with its get_func
    # here key is name of class_get func
    for key, var_name in cl_name_to_desc_var_name_map.iteritems():
       cl_desc = class_desc[var_name]

       #assigning the same sig list to all classes in current file
       self.cl_data[key][const.SIG_DESC] = []
       if len (sig_list) == 2:
         print "There is hack here in parsing of SIG_, if we are here, there are two classes with different descriptiptions in this file."
       if len(sig_list) == 1:
          for k, d in sig_list.items():
            self.cl_data[key][const.SIG_DESC] = d

       #assigning all event's descriptions to class
       # descriptions are: _CLICKED_EVENT = {"clicked", "Clicked comment"}
       self.cl_data[key][const.EVENT_DICT] = event_descriptions

       self.cl_data[key][const.TYPE] = cl_desc["cl_type"]
       self.cl_data[key][const.IMPL_DESC] = cl_desc["implements"]
       self.cl_data[key][const.EV_DESC] = cl_desc["ev_desc"]
       self.cl_data[key][const.BASE_ID] = cl_desc["op_desc"][0].strip()
       self.cl_data[key][const.OP_DESC] = cl_desc["op_desc"][1]

       for tup in cl_desc["op_desc"][1]:
          self.cl_data[key][const.FUNCS][tup[1]] = {const.OP_ID : tup[0], const.MACRO: ""}

       name = cl_desc["name"]
       self.cl_data[key][const.C_NAME] = name
       self.cl_data[key][const.MODULE] = normalize_names([name])[0].lower()
       self.cl_data[key][const.C_FILE] = filename;

  # at this point we have following:
  # list of events for each class, like:
  # [EVAS_OBJECT_CLICKED_EVENT, EVAS_OBJECT_MOVED_EVENT]
  #
  # Eo_Event_Descriptions, like:
  # _CLICKED_EVENT = {"clicked", "Clicked event"}
  # _MOVED_EVENT = {"moved", "Moved event"}
  #
  # List of defines, like
  # #define EVAS_OBJECT_CLICKED_EVENT (&(_CLICKED_EVENT))
  # #define EVAS_OBJECT_MOVED_EVENT (&(_MOVED_EVENT))
  #
  # We want to have list like this:
  # (_CLICKED_EVENT, EVAS_OBJECT_CLICKED_EVENT, "clicked", "Clicked event")
  # (_MOVED_EVENT, EVAS_OBJECT_MOVED_EVENT, "moved", "Moved Event")
  #
  def parse_events(self, cl_id):
    kl = self.cl_data[cl_id]
    defines = kl[const.DEFINES]
    event_descriptions = kl[const.EVENT_DICT]
    kl_events_list = kl[const.EV_DESC]
    for idx, ev in enumerate(kl_events_list):
       printed = False
       for d in defines:
          s = "#define %s"%ev
          if d.find(s) != -1:
             token = d[len(s):]
             token = token.replace(" ", "").replace("(", "").replace(")", "").replace("&", "")
             kl_events_list[idx] = ((token, ev, event_descriptions[token][0], event_descriptions[token][1]))

  #understand which property is going to be implemented
  # set, get, or both
  def implemented_type_get(self, key, lst):
     s = key[:-4]
     suffix = key[-4:]
     SET = GET = ""
     if suffix == "_set" or suffix == "_get":
        SET = "_set"
        GET = "_get"
     elif suffix == "_SET" or suffix == "_GET":
        SET = "_SET"
        GET = "_GET"
     else:
        return const.METHOD

     ret = ""
     if (s + SET) in lst:
        ret = const.SET_ONLY
     if (s + GET in lst):
        if ret == const.SET_ONLY:
          ret = const.SET_GET
        else:
          ret = const.GET_ONLY
     return ret


  def parse_implement_funcs(self, cl_id):
    kl = self.cl_data[cl_id]
    impl_funcs = kl[const.IMPL_DESC]
    kl[const.IMPL_FINAL] = {}
    defines = kl[const.DEFINES]
    base_id = kl[const.BASE_ID]

    #print impl_funcs
    # for each inherited function from list
    # look for a class this function overloads, iterate over each operation of this class an get needed op with name
    for impl_op_id, impl_class_base_id_macro in impl_funcs.iteritems():
       for class_id, class_data in self.cl_data.iteritems():
          #looking for needed class
          if (const.BASE_ID_MACRO in class_data) and (class_data[const.BASE_ID_MACRO] == impl_class_base_id_macro):
             #looking for needed func
             for op, func_name in class_data[const.OP_DESC]:
                if op == impl_op_id:
                   orig_func_type = self.func_type(class_data[const.C_NAME], func_name)
                   if orig_func_type != const.METHOD:
                      func_name = func_name[:-4]

                   impl_func_type = ""
                   # if func which going to be implemented is method, everything is ok
                   # if it is property, we need to understand which property is going to be implemented,
                   # set/get or boty
                   if orig_func_type != const.METHOD:
                     impl_func_type = self.implemented_type_get(impl_op_id, impl_funcs)

                   # if it is set or get, add it to parameters
                   if (impl_func_type == const.SET_ONLY) or (impl_func_type == const.GET_ONLY):
                      kl[const.IMPL_FINAL][func_name] = (class_data[const.C_NAME], func_name, impl_func_type)
                   # if both - keep blank
                   else:
                      kl[const.IMPL_FINAL][func_name] = (class_data[const.C_NAME], func_name)
                   break;
             break;

  # As OP_IDs were generated from EAPI,
  # we try to find new func in hash of legacy.
  # But sometimes we need to do tricks because
  # prefix(class name) is a little bit different

  def find_func_in_hash(self,funcs_list):
     for func in funcs_list:
      # try to find right by the key
       if func in self.eapi_func_ret_type_hash:
         # if func totally maches put None
         self.all_eo_funcs_hash[func] = ((self.eapi_func_ret_type_hash[func], None))
         del(self.eapi_func_ret_type_hash[func])
         continue
      #second try to find for "evas", as in some cases
      # "object" was deleted from class name, so func prefux was changed in eo op
       tokens = func.split("_")
       if ((tokens[0] == "evas") and (tokens[1] != "object")):
         tokens.insert(1, "object")
         new_func = "_".join(tokens)
         if new_func in self.eapi_func_ret_type_hash:
           #here func and new_func are not mistake
           self.all_eo_funcs_hash[func] = ((self.eapi_func_ret_type_hash[new_func], new_func))
           del(self.eapi_func_ret_type_hash[new_func])
           continue

       i = 0
       ll = []
       tokens = func.split("_")
       for key in self.eapi_func_ret_type_hash:
          ret = True
          key_tokens = key.split("_")
          for t in tokens:
             if t not in key_tokens:
                ret = False
          if ret:
             i += 1
             ll.append(key)
       if i > 1:
          print "SUCKS: find %d for %s"%(i, tokens)
          print ll
          # we found several functions which match pattern,
          # there are only 4 cases now, and they are not needed to be fixed
          # (or can be easily fixed manually)
          self.all_eo_funcs_hash[func] = (("void", None))
       elif i == 1:
          self.all_eo_funcs_hash[func] = ((self.eapi_func_ret_type_hash[ll[0]], ll[0]))
          del(self.eapi_func_ret_type_hash[ll[0]])
       elif i == 0:
          print "NOT FOUND: for %s"%(tokens)
          #legacy for func was not found, so return type is "void"
          self.all_eo_funcs_hash[func] = (("void", None))


  def parse_all_return_types(self):
    #iterate over all classes.
    # concatinate class name with func name,
    # save it all in one list and sort by desc length

    all_new_funcs = []
    for cl_id in self.cl_data:
      if const.OP_DESC not in self.cl_data[cl_id]:
         print "Not found: %s"%const.OP_DESC
         exit()
      op_desc = self.cl_data[cl_id][const.OP_DESC]
      func_prefix = self.cl_data[cl_id][const.C_NAME].lower()
      for op, f in op_desc:
         all_new_funcs.append(func_prefix +"_" + f)

    all_new_funcs.sort(key = len)
    all_new_funcs.reverse()
    self.find_func_in_hash(all_new_funcs)


#######################

  #  resolving parameters's types and names according to
  #  #define, @def and op_ids
  def parse_op_func_params(self, cl_id):
    if const.OP_DESC not in self.cl_data[cl_id]:
       print "Not found: %s"%const.OP_DESC
       exit()

    op_desc = self.cl_data[cl_id][const.OP_DESC]
    defines = self.cl_data[cl_id][const.DEFINES]
    macros = self.cl_data[cl_id][const.OP_MACROS]
    b_id = self.cl_data[cl_id][const.BASE_ID]
    b_id_macro = ""
    for d in defines:
      o = re.match("#define ([\w]*)\(([^\)]*)\) \(%s[\W]*\\2[\W]*\)"%(b_id), d)
      if o != None:
         b_id_macro = o.group(1)

    #save macro which is used to calculate BASE_ID + OP_ID
    self.cl_data[cl_id][const.BASE_ID_MACRO] = b_id_macro

    #looking for op_id in define; if found, cutting op_macro from define
    #and checking if it is in macros list. If not - we forgot to add comment
    #if yes - cutting types from define
    func_prefix = self.cl_data[cl_id][const.C_NAME].lower()
    for op, f in op_desc:
       found = False
       for d in defines:
         # looking for #define elm_obj_flip_get ELM_OBJ_FLIP_ID(ELM_OBJ_FLIP_SUB_ID_GET)
         o = re.match("#define ([\w]*)\([^\)]*\) %s\(%s\).*"%(b_id_macro, op), d)
         if o != None:
           found = True
           s_tmp = o.group(1)

           if s_tmp not in macros:
              print "Warning: no comments for \"%s\"; file: \"%s\" "%(s_tmp, self.cl_data[cl_id][const.H_FILE])
              found = False
           else:

             params = []
             params_direction = macros[s_tmp][const.PARAMETERS]
             reg = "%s\(([^,]*),([^,]*)\)"%const.EO_TYPECHECK
             ss = re.findall(reg, d)

             if len(ss) != len(params_direction):
                print "Warning: for function: %s, there are %d params in comment and %d in define"%(s_tmp, len(params_direction), len(ss))
             i = 0
             for tup in ss:
                lst = list(tup)
                modifier = "const" if lst[0].find("const") != -1 else ""
                lst[0] = lst[0].replace("const", "")
                lst[0] = " ".join(lst[0].split())
                lst[0] = lst[0].replace(" *", "*")
                lst[1] = lst[1].replace(" ", "")
                if len(lst) == 2:
                   try:
                     tok = params_direction[i][0]
                     comment = params_direction[i][1]
                     params.append((lst[1], modifier, lst[0], tok, comment))
                   except IndexError:
                     print "Warning: error in description %s in  %s"%(s_tmp,self.cl_data[cl_id][const.H_FILE])

                else:
                   print "ERROR: check parameters in EO_TYPECHECK"
                   exit(1)
                i += 1
             self.cl_data[cl_id][const.FUNCS][f][const.PARAMETERS] = params
             self.cl_data[cl_id][const.FUNCS][f][const.COMMENT] = macros[s_tmp][const.COMMENT]
             self.cl_data[cl_id][const.FUNCS][f][const.MACRO] = s_tmp
             ret_t, legacy_name = self.all_eo_funcs_hash[func_prefix + "_" + f]
             self.cl_data[cl_id][const.FUNCS][f][const.RETURN_TYPE] = ret_t
             self.cl_data[cl_id][const.FUNCS][f][const.LEGACY_NAME] = legacy_name
         
       if not found:
         print "Warning: no API for %s in  %s"%(op, self.cl_data[cl_id][const.H_FILE])
         print "Function won't be added"
         self.cl_data[cl_id][const.FUNCS].pop(f)



  #generating XML
  def build_xml(self, cl_id):
    self.cl_data[cl_id][const.XML_FILE] = os.path.join(self.outdir, normalize_names([self.cl_data[cl_id][const.C_NAME]])[0] + ".xml")

    cl_data = self.cl_data[cl_id]

    module = Element(const.MODULE)
    module.set(const.NAME, cl_data[const.C_NAME])

    SubElement(module, const.PARSE_VERSION, {const.NUM : const.VER_NUM} )
    SubElement(module, const.INCLUDE, {const.NAME: os.path.split(cl_data[const.H_FILE])[1]})

    cl_parent = ""
    cl_brothers = []
    for i, l in enumerate(cl_data[const.PARENTS]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit(1)
      if i == 0:
        cl_parent = tmp[l][const.C_NAME]
      else:
        cl_brothers.append(tmp[l][const.C_NAME])

    SubElement(module, const.EXTERN_FUNCTION, {const.NAME:cl_data[const.GET_FUNCTION]+"()",
                                           const.TYPENAME:"Eo_Class*"})

    cl_brothers = ",".join(cl_brothers)

    instantiateable = "False"
    if cl_data[const.TYPE] == const.CLASS_TYPE_REGULAR:
      instantiateable = "True"
    cl = SubElement(module, const.CLASS, {
                                      const.C_NAME : cl_data[const.C_NAME],
                                      const.PARENT:cl_parent,
                                      const.EXTENSIONS:cl_brothers,
                                      const.MACRO:cl_id,
                                      const.GET_FUNCTION: cl_data[const.GET_FUNCTION],
                                      const.TYPE : cl_data[const.TYPE],
                                      const.INSTANTIATEABLE : instantiateable})

    op_tag = SubElement(cl, const.OP_ID)
    ev_tag = SubElement(cl, const.EVENTS)
    m_tag = SubElement(cl, const.METHODS)

    if cl_data[const.BASE_ID] != "NULL":
      SubElement(op_tag, const.BASE_ID, {const.NAME:cl_data[const.BASE_ID]})

    for k in cl_data[const.FUNCS]:
        SubElement(op_tag, const.XML_SUB_ID, {const.NAME:cl_data[const.FUNCS][k][const.OP_ID]})

        c_macro = cl_data[const.FUNCS][k][const.MACRO]
        #if generating XML not for base class, change func name to avoid name clash
        func_name = k if cl_id == "EO_BASE_CLASS" else c_macro

        # add <method> tag
        m = SubElement(m_tag, const.METHOD, {const.NAME : func_name,
                                      const.OP_ID:cl_data[const.FUNCS][k][const.OP_ID],
                                      const.MACRO:c_macro, const.COMMENT:cl_data[const.FUNCS][k][const.COMMENT]})

        #add <parameter> tags
        if const.PARAMETERS in cl_data[const.FUNCS][k]:
          params = cl_data[const.FUNCS][k][const.PARAMETERS]
          for v_name, modifier, t, d, c in params:
             p = SubElement(m, const.PARAMETER, {const.NAME:v_name, const.MODIFIER:modifier, const.C_TYPENAME:t, const.PRIMARY_TYPE : self.typedef_resolve(t),const.DIRECTION:d, const.COMMENT:c})


    if const.EV_DESC in cl_data:
      lst = cl_data[const.EV_DESC]
      for api_id, event_id, event_name, comment in lst:
         SubElement(ev_tag, const.EVENT,{const.NAME:api_id, const.EVENT_ID:event_id,
                                         const.EVENT_NAME:event_name, const.COMMENT:comment})

    res = tostring(module, "utf-8")
    res = minidom.parseString(res)
    res = res.toprettyxml(indent="  ")

    (h, t) = os.path.split(self.cl_data[cl_id][const.XML_FILE])
    if not os.path.isdir(h):
      os.makedirs(h)
    f = open (self.cl_data[cl_id][const.XML_FILE], 'w')
    f.write(res)
    f.close()

  # helper function
  # takes doxygen comment, removes * in the beginning of comment
  # concatenates @param lines
  def _comment_preparse(self, _com):
     com_lines =  _com.split("\n")
     com_lines2 = []
     for idx, l in enumerate(com_lines):
        s = l.lstrip(" ").lstrip("\"").lstrip("*").lstrip(" ")
        if s[ : 6] == "@param":
           ss = com_lines[idx + 1].lstrip(" ").lstrip("\"").lstrip("*").lstrip(" ")
           if ((len(ss) != 0) and (ss[0] != "@")):
             s = s + " " + ss
             com_lines.pop(idx + 1)

        com_lines2.append(s)

     com = "\n".join(com_lines2)
     return com

  # get perams direction and description from comment
  def get_param_dir_from_comment(self, com):
     res = re.findall("@param.*", com)
     l_tmp = []
     for s in res:
       ret = re.match("@param[ ]*\[([inout,]*)\][ ]+[\w]+([ \(\),#@\w]*)", s)
       direct = ""
       comment = ""
       if ret:
          direct = ret.group(1)
          comment = ret.group(2)
          comment = comment.strip()
       direct = direct if direct in ["in", "out", "in,out"] else "in,out"
       l_tmp.append((direct, comment))
     return l_tmp

  def get_brief_desc_from_comment(self, com):
     res = re.findall("@brief(.*)", com)
     desc = res[0] if res else ""
     desc = " ".join(desc.split())
     return desc

  def get_desc_from_comment(self, com):
     desc = re.sub("@.*\n", "", com)
     desc = desc.replace("*", "").strip()
     desc = " ".join(desc.split())
     return desc

  #parsing header file
  def h_file_data_get(self, filename):
    f = open (filename, 'r')
    allfile = f.read()
    f.close()

    # fetch all EAPI functions to match with funcs from classes
    reg = "EAPI[^;]*;"
    af = allfile.replace("\n", "");
    eapi_list = re.findall(reg, allfile)
    for l in eapi_list:
      tmp = " ".join(l.split())
      # suppose this is usual func, so we can look for (
      # and cut everything off
      pos = tmp.find("(")
      if pos == -1:
         continue
      tmp = tmp[ : pos].strip()

      #look for EAPI and cut it off
      pos = tmp.find("EAPI")
      tmp = tmp[pos + 4 :].strip()

      # look for * from right, if not found look for space
      pos = tmp.rfind("*")
      if pos == -1:
         pos = tmp.rfind(" ")
      type_name = tmp[ : pos + 1].replace(" *", "*").strip()
      func_name = tmp[pos + 1 : ].replace(" ", "")
      # if func starts with "_" dont add it. This is internal API
      if func_name[0] == "_":
         continue
      if ((type_name.find("void") != -1) and (type_name.find("*") == -1)):
        type_name = "void"
      self.eapi_func_ret_type_hash[func_name] = type_name

   #fetch all "#define" from file
    matcher = re.compile(r"^[ \t]*(#define(.*\\\n)*.*$)",re.MULTILINE)
    ss = matcher.findall(allfile)
    def_list = []
    for tup in ss:
      s_tmp = tup[0].replace("\n", "").replace("\\", "")
      s_tmp = " ".join(s_tmp.split())
      def_list.append(s_tmp)

    #fetch all "@def" from file
    matcher = re.compile("(^/\*\*\n(((.(?!\*/))*\n)*).*\*/$)",re.MULTILINE)
    all_comments_list = matcher.findall(allfile)
    macro = {}
    for comment in all_comments_list:
         comment_tmp = comment[1]

         #looking for @def token in comment
         res = re.search("@def[ ]+([\w]*)", comment_tmp)
         if res == None:
            continue

         macro_name = res.group(1)
         #looking for parameters direction and desc in comment
         macro[macro_name] = {}
         comment_tmp = self._comment_preparse(comment_tmp)
         macro[macro_name][const.PARAMETERS] = self.get_param_dir_from_comment(comment_tmp)
         #save comment for method
         desc = self.get_brief_desc_from_comment(comment_tmp)
         if desc == "":
            desc = self.get_desc_from_comment(comment_tmp)
         else:
            desc += "\n"
            desc += self.get_desc_from_comment(comment_tmp)
 
         macro[macro_name][const.COMMENT] = desc


    #looking for class_get function to get class macro
    current_class = ""
    cl_macro = []
    cl_id_copy = []

    for k in self.cl_data:
      pos = 0
      get_func = ""
      
      for d in def_list: 
        # looking for #define SOME_CLASS some_class_get()
        reg = '#define[ ]*[\w]*[ ]*%s\(\)'%k
        res = re.findall(reg, d)
        if re.match(reg, d):
          lst = d.split()
          current_class = lst[1]
          get_func = k
          cl_macro.append((get_func, current_class))

          if current_class in self.cl_data:
            verbose_print("Class %s from file %s won't be added in the tree"%(current_class, filename))
            verbose_print("Class %s from file %s will be used as parent in inheritance"%(current_class, self.cl_data[current_class][const.H_FILE]))
            return

    if current_class == "":
      return

    for gf, cl_id in cl_macro:
      self.cl_data[cl_id] = self.cl_data[gf]
      self.cl_data.pop(gf)
      self.cl_data[cl_id][const.GET_FUNCTION] = gf
      self.cl_data[cl_id][const.H_FILE] = filename
      self.cl_data[cl_id][const.DEFINES] = def_list
      self.cl_data[cl_id][const.OP_MACROS] = macro

  #print out data from each class in parser object
  def print_data(self):
    for klass in self.cl_data:
      print ""
      print klass
      for kk in self.cl_data[klass]:
        print "  ", kk, " : ", type(self.cl_data[klass][kk])# " : ", cp.cl_data[klass][kk]
        d = self.cl_data[klass][kk]
        spaces = " " * 15
        if type(d) == str:
          print spaces, d
        elif type(d) == dict:
          for key in d:
            print spaces, key, " : ", d[key]
        elif type(d) == list:
          for l in d:
            print spaces, l

  #set internal variable for outdir
  def outdir_set(self, _d):
    self.outdir = _d

  #generating Eo file in C-style
  def build_eo(self, cl_id):
    self.cl_data[cl_id][const.XML_FILE] = os.path.join(self.outdir, normalize_names([self.cl_data[cl_id][const.C_NAME]])[0] + ".eo")

    new_buf = ""

    cl_data = self.cl_data[cl_id]

    cl_parent = ""
    cl_brothers = []
    cl_brothers_str = ""
    for i, l in enumerate(cl_data[const.PARENTS]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit(1)
      if i == 0:
        cl_parent = tmp[l][const.C_NAME]
      else:
        cl_brothers.append(tmp[l][const.C_NAME])

    cl_brothers_str = ",".join(cl_brothers)

    instantiateable = "False"
    if cl_data[const.TYPE] == const.CLASS_TYPE_REGULAR:
      instantiateable = "True"

    #resolve funcs/set/get/properties
    func_name_list_not_visited = []
    for name in cl_data[const.FUNCS]:
      func_name_list_not_visited.append(name) 

    cl_data[const.METHOD] = []
    cl_data[const.SET_GET] = []
    cl_data[const.SET_ONLY] = []
    cl_data[const.GET_ONLY] = []
    for i, v in cl_data[const.FUNCS].iteritems():
       T = ""
       if cl_data[const.C_NAME] == "Eo Base":
         T = const.METHOD
         cl_data[T].append(i)
         continue

       #check if both properties are in tree; and if they are in,
       # if their parameters are all in or out
       prefix = i[:-4] 
       postfix = i[-4:]
       if postfix in ["_set", "_get"]:
          if prefix + "_set" in func_name_list_not_visited and prefix + "_get" in func_name_list_not_visited:
             T = const.SET_GET
             for (n, m ,t1, d, c) in cl_data[const.FUNCS][prefix+"_set"][const.PARAMETERS]:
               if d != "in":
                 T = const.METHOD

             for (n, m ,t1, d, c) in cl_data[const.FUNCS][prefix+"_get"][const.PARAMETERS]:
               if d != "out":
                 T = const.METHOD

             if (T == const.SET_GET):
                cl_data[T].append(prefix)
             else:
                cl_data[T].append(prefix + "_set")
                cl_data[T].append(prefix + "_get")

             func_name_list_not_visited.remove(prefix + "_set")
             func_name_list_not_visited.remove(prefix + "_get")

          elif prefix + "_set" in func_name_list_not_visited:
             T = const.SET_ONLY
             for (n, m ,t1, d, c) in cl_data[const.FUNCS][prefix+"_set"][const.PARAMETERS]:
               if d != "in":
                 T = const.METHOD
             cl_data[T].append(i)
             func_name_list_not_visited.remove(i)

          elif prefix + "_get" in func_name_list_not_visited:
             T = const.GET_ONLY
             for (n, m ,t1, d, c) in cl_data[const.FUNCS][prefix+"_get"][const.PARAMETERS]:
               if d != "out":
                 T = const.METHOD
             cl_data[T].append(i)
             func_name_list_not_visited.remove(i)

       else:
         T = const.METHOD
         cl_data[T].append(i)
         func_name_list_not_visited.remove(i)

    lines = []
    parents = []
    tab = "     "
    tab_level = 0

    parents.append(cl_parent)
    parents += cl_brothers
    lines.append("inherit")
    lines.append("%s%s"%(tab_level * tab, "{"))
    tab_level += 1
    param_num = len(parents)
    for l in parents:
      line = "%s%s"%(tab_level * tab, l)
      line += "," if param_num > 1 else ";"
      lines.append(line)
      param_num -= 1
    tab_level -= 1
    lines.append("%s%s"%(tab_level * tab, "}"))

    prop_dir = "rw"
    #properties
    if len(cl_data[const.SET_GET]) or len(cl_data[const.SET_ONLY]) or len(cl_data[const.GET_ONLY]):
      lines.append("properties")

      lines.append("%s%s"%(tab_level * tab, "{"))
      tab_level += 1
      for name in cl_data[const.SET_GET]:
        f = cl_data[const.FUNCS][name + "_set"]
        lines.append("%s /* %s */"%(tab_level * tab, f[const.COMMENT]))
        lines.append("%s %s %s("%(tab_level * tab, prop_dir, name))
        tab_level += 1
        param_num = len(f[const.PARAMETERS])
        for (n, m ,t1, d, c) in f[const.PARAMETERS]:
           line = "%s%s %s /* %s */"%(tab_level * tab, t1, n, c)
           if param_num > 1:
              line += ","
           lines.append(line)
           param_num -=1
        tab_level -= 1
        lines.append("%s);"%(tab_level * tab))

      prop_dir = "wo"
    #properties_set
      for name in cl_data[const.SET_ONLY]:
        f = cl_data[const.FUNCS][name]
        lines.append("%s /* %s */"%(tab_level * tab, f[const.COMMENT]))
        lines.append("%s %s %s("%(tab_level * tab, prop_dir, name))
        tab_level += 1
        param_num = len(f[const.PARAMETERS])
        for (n, m ,t1, d, c) in f[const.PARAMETERS]:
           line = "%s%s %s /* %s */"%(tab_level * tab, t1, n, c)
           if param_num > 1:
              line += ","
           lines.append(line)
           param_num -=1
        tab_level -= 1
        lines.append("%s);"%(tab_level * tab))

      prop_dir = "ro"
    #properties_get
      for name in cl_data[const.GET_ONLY]:
        f = cl_data[const.FUNCS][name]
        lines.append("%s /* %s */"%(tab_level * tab, f[const.COMMENT]))
        lines.append("%s %s %s("%(tab_level * tab, prop_dir, name))
        tab_level += 1
        param_num = len(f[const.PARAMETERS])
        for (n, m ,t1, d, c) in f[const.PARAMETERS]:
           line = "%s%s %s /* %s */"%(tab_level * tab, t1, n, c)
           if param_num > 1:
              line += ","
           lines.append(line)
           param_num -=1
        tab_level -= 1
        lines.append("%s);"%(tab_level * tab))
      tab_level -= 1
      lines.append("%s%s"%(tab_level * tab, "}"))

    #methods
    if len(cl_data[const.METHOD]):
      lines.append("methods")
      lines.append("%s%s"%(tab_level * tab, "{"))
      tab_level += 1
      for name in cl_data[const.METHOD]:
        f = cl_data[const.FUNCS][name]
        lines.append("%s /* %s */"%(tab_level * tab, f[const.COMMENT]))
        lines.append("%s%s("%(tab_level * tab, name))
        tab_level += 1
        param_num = len(f[const.PARAMETERS])
        for (n, m ,t1, d, c) in f[const.PARAMETERS]:
           line = "%s%s %s %s /* %s */"%(tab_level * tab, "inout" if d == "in,out" else d, t1, n, c)
           if param_num > 1:
              line += ","
           lines.append(line)
           param_num -=1
        tab_level -= 1
        lines.append("%s);"%(tab_level * tab))
      tab_level -= 1
      lines.append("%s%s"%(tab_level * tab, "}"))

    #main brackets
    tab_level = 1
    new_buf = "%s =\n{\n"%(cl_data[const.C_NAME])
    for l in lines:
       new_buf += "%s%s\n"%(tab_level * tab, l)

    new_buf += "\n}"
    res = new_buf

    (h, t) = os.path.split(cl_data[const.XML_FILE])
    if not os.path.isdir(h):
      os.makedirs(h)

    f = open (cl_data[const.XML_FILE], 'w')
    f.write(res)
    f.close()


  def func_type(self, cl_name, func_name):
    kl = None
    for cl_id, data in self.cl_data.iteritems():
       if data[const.C_NAME] == cl_name:
          kl = data
          break;

    if "constructor" in func_name:
       return const.METHOD

    prefix = func_name[:-4]
    postfix = func_name[-4:]

    T = None
    if postfix in ["_set", "_get"]:
      if prefix + "_set" in kl[const.FUNCS] and prefix + "_get" in kl[const.FUNCS]:
         T = const.SET_GET
         for (n, m ,t1, d, c) in kl[const.FUNCS][prefix+"_set"][const.PARAMETERS]:
           if d != "in":
             T = const.METHOD

         for (n, m ,t1, d, c) in kl[const.FUNCS][prefix+"_get"][const.PARAMETERS]:
           if d != "out":
             T = const.METHOD
      elif prefix + "_set" in kl[const.FUNCS]:
         T = const.SET_ONLY
         for (n, m ,t1, d, c) in kl[const.FUNCS][prefix+"_set"][const.PARAMETERS]:
           if d != "in":
             T = const.METHOD

      elif prefix + "_get" in kl[const.FUNCS]:
         T = const.GET_ONLY
         for (n, m ,t1, d, c) in kl[const.FUNCS][prefix+"_get"][const.PARAMETERS]:
           if d != "out":
             T = const.METHOD

    elif func_name in kl[const.FUNCS]:
       T = const.METHOD
    
    return T


  #generating Eo file in JSON
  def build_eo2(self, cl_id):
    ret = OrderedDict()
    CLASS_NAME = "name"
    INHERITS = "inherits"
    METHODS = "methods"
    PROPERTIES = "properties"
    CONSTRUCTORS = "constructors"
    IMPLEMENTS = "implements"
    SIGNALS = "signals"
    ret[CLASS_NAME] = ""
    ret[const.LEGACY_NAME] = ""
    ret[INHERITS] = []
    ret[CONSTRUCTORS] = OrderedDict()
    ret[PROPERTIES] = OrderedDict()
    ret[METHODS] = OrderedDict()
    ret[IMPLEMENTS] = []
    ret[SIGNALS] = []

    self.cl_data[cl_id][const.XML_FILE] = os.path.join(self.outdir, normalize_names([self.cl_data[cl_id][const.C_NAME]])[0] + ".eo")

    new_buf = ""

    cl_data = self.cl_data[cl_id]
    ret[CLASS_NAME] = cl_data[const.C_NAME]
    ret[const.LEGACY_NAME] = ret[CLASS_NAME].lower()
    #ret[MACRO] = cl_id

    cl_parent = ""
    cl_brothers = []
    cl_brothers_str = ""
    for i, l in enumerate(cl_data[const.PARENTS]):
      tmp = {}
      if l in self.cl_data:
        tmp = self.cl_data
      elif l in self.cl_incl:
        tmp = self.cl_incl
      else:
        print "ERROR: no parent class \"%s\" was found"%l
        exit(1)
      if i == 0:
        cl_parent = tmp[l][const.C_NAME]
      else:
        cl_brothers.append(tmp[l][const.C_NAME])

    parents = []
    parents.append(cl_parent)
    parents += cl_brothers
    ret[INHERITS] = parents

    instantiateable = "False"
    if cl_data[const.TYPE] == const.CLASS_TYPE_REGULAR:
      instantiateable = "True"

    #resolve funcs/set/get/properties
    func_name_list_not_visited = []
    for name in cl_data[const.FUNCS]:
      func_name_list_not_visited.append(name)

    cl_data[const.METHOD] = []
    cl_data[CONSTRUCTORS] = []
    cl_data[const.SET_GET] = []
    cl_data[const.SET_ONLY] = []
    cl_data[const.GET_ONLY] = []

    for itr_name, v in cl_data[const.FUNCS].iteritems():
       if itr_name not in func_name_list_not_visited:
          continue
       T = ""
       if cl_data[const.C_NAME] == "Eo Base":
         T = const.METHOD
         cl_data[T].append(itr_name)
         continue

       #check if both properties are in tree; and if they are in,
       # if their parameters are all in or out

       T = self.func_type(cl_data[const.C_NAME], itr_name)
       prefix = itr_name[:-4]
       """
       if (prefix in cl_data[const.FUNCS]):
          print "Clash"
          print ("%s :: %s :: %s :: %s")%(ret[CLASS_NAME], itr_name, prefix, T)
       """
       if (T == const.SET_GET):
          cl_data[T].append(prefix)
          func_name_list_not_visited.remove(prefix + "_set")
          func_name_list_not_visited.remove(prefix + "_get")
       elif (T == const.SET_ONLY or T == const.GET_ONLY):
          cl_data[T].append(prefix)
          func_name_list_not_visited.remove(itr_name)
       elif (T == const.METHOD):
          suffix = itr_name[-4:]
          if suffix in ["_set", "_get"]:
             if prefix + "_set" in func_name_list_not_visited and prefix + "_get" in func_name_list_not_visited:
                cl_data[T].append(prefix + "_set")
                cl_data[T].append(prefix + "_get")
                func_name_list_not_visited.remove(prefix + "_set")
                func_name_list_not_visited.remove(prefix + "_get")
             else:
                cl_data[T].append(itr_name)
                func_name_list_not_visited.remove(itr_name)
          else:
             cl_data[T].append(itr_name)
             func_name_list_not_visited.remove(itr_name)

    #properties
    for name in cl_data[const.SET_GET]:
      f_ret = ret[PROPERTIES][name] = OrderedDict()
      f = cl_data[const.FUNCS][name + "_set"]
     
      f_ret["set"] = OrderedDict()
      f_ret["get"] = OrderedDict()

      f_ret["set"]["comment"] = f[const.COMMENT]
      f_ret["get"]["comment"] = cl_data[const.FUNCS][name + '_get'][const.COMMENT]

      if f[const.LEGACY_NAME]:
        f_ret["set"][const.LEGACY_NAME] = f[const.LEGACY_NAME]

      legacy_name = cl_data[const.FUNCS][name + '_get'][const.LEGACY_NAME]
      if legacy_name:
        f_ret["get"][const.LEGACY_NAME] = legacy_name

      par_arr = f_ret["parameters"] = []
      for (n, m ,t1, d, c) in f[const.PARAMETERS]:
         t1 = ("%s %s"%(m, t1)).strip()
         p = {}
         p[n] = (t1, c)
         par_arr.append(p)

  #properties_set
    for name in cl_data[const.SET_ONLY]:
      f_ret = ret[PROPERTIES][name] = OrderedDict()
      f = cl_data[const.FUNCS][name + "_set"]
      f_ret["set"] = OrderedDict()
      f_ret["set"]["comment"] = f[const.COMMENT]
      if f[const.LEGACY_NAME]:
        ret[PROPERTIES][name]["set"][const.LEGACY_NAME] = f[const.LEGACY_NAME]
      par_arr = f_ret["parameters"] = []
      for (n, m ,t1, d, c) in f[const.PARAMETERS]:
         t1 = ("%s %s"%(m, t1)).strip()
         p = {}
         p[n] = (t1, c)
         par_arr.append(p)

  #properties_get
    for name in cl_data[const.GET_ONLY]:
      f_ret = ret[PROPERTIES][name] = OrderedDict()
      f = cl_data[const.FUNCS][name + "_get"]
      f_ret["get"] = OrderedDict()
      f_ret["get"]["comment"] = f[const.COMMENT]
      if f[const.LEGACY_NAME]:
        ret[PROPERTIES][name]["get"][const.LEGACY_NAME] = f[const.LEGACY_NAME]
      par_arr = f_ret["parameters"] = []
      for (n, m ,t1, d, c) in f[const.PARAMETERS]:
         #remove * from out parameter
         p = t1.find("*")
         t1 = t1[:p] + t1[p + 1:]
         t1 = ("%s %s"%(m, t1)).strip()
         p = {}
         p[n] = (t1, c)
         par_arr.append(p)

    #constructors
    for name in cl_data[CONSTRUCTORS]:
      f_ret = ret[CONSTRUCTORS][name] = OrderedDict()
      par_arr = f_ret["parameters"] = []
      f = cl_data[const.FUNCS][name ]
      f_ret["comment"] = f[const.COMMENT]
      for (n, m ,t1, d, c) in f[const.PARAMETERS]:
         par_arr.append((d, "%s %s"%(m, t1), n, c))

    #methods
    for name in cl_data[const.METHOD]:
      ret_tmp = ret[METHODS]
      if "constructor" in name:
         ret_tmp = ret[CONSTRUCTORS]
      ret_tmp[name] = OrderedDict()
      f = cl_data[const.FUNCS][name]

      ret_tmp[name]["comment"] = f[const.COMMENT]

      #add "return_type" field only if type is no void
      ret_type = f[const.RETURN_TYPE]
      if ret_type != "void":
        ret_tmp[name][const.RETURN_TYPE] = ret_type
      if f[const.LEGACY_NAME]:
        ret_tmp[name][const.LEGACY_NAME] = f[const.LEGACY_NAME]
      par_map = ret_tmp[name]["parameters"] = OrderedDict()
      #par_map["in"] = []
      #par_map["in,out"] = []
      #par_map["out"] = []

      in_params_array = []
      out_params_array = []
      PAR_IN = 1
      PAR_IN_OUT = 2
      PAR_OUT = 3
      par_dir_state = PAR_IN
      for idx, (n, m ,t1, d, c) in enumerate(f[const.PARAMETERS]):
         # if return type is not "void", don't add last parameter - generator will add it by himself
         if ((ret_type != "void") and (idx == len(f[const.PARAMETERS]) - 1)):
           break
         if d == "in" and (par_dir_state > PAR_IN):
            print "IN parameter after OUT parameter detected in %s %s"%(ret[CLASS_NAME], name)
            #exit()
         # if parameter is out cut off * in type
         if d == "in,out":
            if par_dir_state == PAR_OUT:
              print "IN,OUT parameter after OUT parameter detected in %s %s"%(ret[CLASS_NAME], name)
            else:
              par_dir_state = PAR_IN_OUT
         if d == "out":
           p = t1.find("*")
           t1 = t1[:p] + t1[p + 1:]
           in_after_out = True
           par_dir_state = PAR_OUT


         t1 = ("%s %s"%(m, t1)).strip()
         p = {}
         p[n] = (t1, c)
         if d not in par_map:
            par_map[d] = []
         par_map[d].append(p)

    # add pairs Class name - func which is overriden
    for op_id, data in cl_data[const.IMPL_FINAL].iteritems():
       ret[IMPLEMENTS].append(data)

    # add old styled signals
    ret[SIGNALS] = cl_data[const.SIG_DESC]
    # add eo events
    eo_events = cl_data[const.EV_DESC]
    for l in eo_events:
       ret[SIGNALS].append((l[2], l[3]))

    (h, t) = os.path.split(cl_data[const.XML_FILE])
    if not os.path.isdir(h):
      os.makedirs(h)

    f = open(cl_data[const.XML_FILE], 'w')
    f.write(json.dumps(ret, indent=2))
    #f.write(json.dumps(cl_data, indent=2))
    f.close()

# smart_split(tmp)
#
# tmp - string to split
# Splits string with delimeter ',', but doesn't split data in brackets
#
# Returns list of tokens
#
##########

def smart_split(tmp):
  bracket = 0
  pos_start = 0
  l = []
  for i in range(len(tmp)):
    if tmp[i] == ',' and bracket == 0:
      l.append(tmp[pos_start:i])
      pos_start = i + 1
    elif tmp[i] == '(':
      bracket += 1
    elif tmp[i] == ')':
      bracket -= 1
  l.append(tmp[pos_start : ])

  return l

def smart_split2(tmp, open_delimeter, close_delimeter):
  bracket = 0
  pos_start = 0
  l = []
  for i in range(len(tmp)):
    if tmp[i] == ',' and bracket == 0:
      l.append(tmp[pos_start:i])
      pos_start = i + 1
    elif tmp[i] == open_delimeter:
      if open_delimeter == close_delimeter and bracket == 1:
         bracket -=1
      else:
         bracket += 1
    elif tmp[i] == close_delimeter:
      bracket -= 1
  l.append(tmp[pos_start : ])

  return tuple(l)
