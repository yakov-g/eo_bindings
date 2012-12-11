import unittest
import os
from eoparser.xmlparser import XMLparser
from eoparser.cparser import Cparser
from eoparser.helper import dir_files_get, abs_path_get, isC, isH, isXML, normalize_names

class testP(unittest.TestCase):
    
    def setUp(self):
        self.c_parser = Cparser(False)

    def test_fetch_data(self):
        f = open('test_data.in', 'r')
        s = f.read()
        f.close()

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

    def test_isC(self):
        self.assertTrue(isC("abc.c"))
        self.assertTrue(isC("abc.cc"))
        self.assertTrue(isC("abc.cpp"))
        self.assertFalse(isC("abc.cp"))
        self.assertFalse(isC("abc.def.c"))

    def test_isH(self):
        self.assertTrue(isH("abc.h"))
        self.assertFalse(isH("abc.c"))
        self.assertFalse(isH("abc.def.h"))

    def test_isXML(self):
        self.assertTrue(isXML("abc.xml"))
        self.assertTrue(isXML("/abc/def/abc.xml"))
        self.assertTrue(isXML("/abc/py2.7/abc.xml"))
        self.assertFalse(isXML("abc.h"))
        self.assertFalse(isXML("abc.qwe.xml"))

    def test_abs_path_get(self):
       _in = "test_data.in"
       _in_list = [_in]
       _out = _in
       _out = os.path.expanduser(_out)
       _out = os.path.abspath(_out)

       self.assertEqual(abs_path_get(_in_list), [_out])

    def test_normalize_names(self):
       _in = ["hello world", "elm_Box", "evas Object-SmaRt", "EvAs-common InTeRface"]
       _out = ["HelloWorld", "ElmBox", "EvasObjectSmart", "EvasCommonInterface"]

       self.assertEqual(normalize_names(_in), _out)


    def test_get_param_dir_from_comment(self):
       s = """
             @param[in,out] a
             @param[in] a
             @param[out] a
             parem[in]
             @param [in] a
             @param    [out] a
             @param[in, out] a
             @param in
             @param [  in  ]
             @param [  out, in  ]
             @param sdf [ out  ]
           """
       _out = ["in,out", "in", "out", "in", "out", "in,out", "in,out", "in", "in,out", "in,out"]
       ret = self.c_parser.get_param_dir_from_comment(s)
       self.assertEqual(ret, _out)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testP))
    return suite

if __name__ == '__main__':

    unittest.main()
