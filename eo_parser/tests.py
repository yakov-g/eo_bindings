import unittest
from XMLparser import XMLparser
from eo_parser.Cparser import Cparser

class testP(unittest.TestCase):
    
    def setUp(self):
        self.c_parser = Cparser(False)

    def test_strip(self):
        s = """
            #define MY_TEST_CLASS_NAME "test_class_name"

static const Eo_Op_Description _elm_pan_op_desc[] = {
     EO_OP_DESCRIPTION(ELM_OBJ_PAN_SUB_ID_POS_SET, "description here"),
     EO_OP_DESCRIPTION(ELM_OBJ_PAN_SUB_ID_POS_GET, "description here"),
     EO_OP_DESCRIPTION_SENTINEL
};

static const Eo_Event_Description *event_desc[] = {
     EO_EV_CALLBACK_ADD,
     EO_EV_CALLBACK_DEL,
     EO_EV_DEL,
     NULL
};

static const Eo_Class_Description test_class_desc = {
     EO_VERSION,
     MY_TEST_CLASS_NAME,
     EO_CLASS_TYPE_REGULAR,
     EO_CLASS_DESCRIPTION_OPS(&ELM_OBJ_PAN_BASE_ID, _elm_pan_op_desc, ELM_OBJ_PAN_SUB_ID_LAST),
     event_desc,
     sizeof(Elm_Pan_Smart_Data),
     _elm_pan_class_constructor,
     NULL
};

            EO_DEFINE_CLASS(class_get, &test_class_desc, parent, brother, NULL)

            """
        class_def_answer = {"class_get" : ["parent", 
                                           ["brother"], 
                                           "test_class_name", 
                                           "EO_CLASS_TYPE_REGULAR", 
                                               ["ELM_OBJ_PAN_BASE_ID", 
                                               [("ELM_OBJ_PAN_SUB_ID_POS_SET", "pos_set"), ("ELM_OBJ_PAN_SUB_ID_POS_GET", "pos_get")],
                                                "ELM_OBJ_PAN_SUB_ID_LAST"], 
                                           ["EO_EV_CALLBACK_ADD", "EO_EV_CALLBACK_DEL", "EO_EV_DEL"]
                                           ]}
        answer = class_def_answer

        ret = self.c_parser.fetch_data(s)
        self.assertEqual(ret, answer)
#        self.assertEqual(self.prs.strip_replace("{test str}", "{} "), "teststr" )
    """    
    def test_strip2(self):
        s = "(teststr)"
        self.assertEqual(self.prs.strip_replace("  [te stst r]  ", "[] "), "teststr")

    def test_parse(self):
        s = "EO_DEFINE_CLASS(elm_button_class_get, &desc)"
        self.assertEqual(self.prs.parse_class_desc(s), ["elm_button_class_get", "desc"])
        self.assertEqual(self.prs.defs, ["elm_button_class_get", "desc"])
        self.assertEqual(self.prs.dic, {"a" : "b" , 1 :34} )
"""

def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testP))
    return suite



if __name__ == '__main__':

    unittest.main()
