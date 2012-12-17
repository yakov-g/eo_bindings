from distutils.core import setup
from distutils.extension import Extension

#True, False, 'auto'
USE_CYTHON = 'auto'

import sys, commands

def pkgconfig(_libs):
  cf = commands.getoutput("pkg-config --cflags %s"%_libs).split()
  ldf = commands.getoutput("pkg-config --libs %s"%_libs).split()
  return (cf, ldf)

(e_compile_args, e_link_args) = pkgconfig("eo")

e_include_dirs = ["."]
e_library_dirs = []
e_libraries = []

cmdclass = {}
ext_modules = []


if USE_CYTHON:
   try:
      from Cython.Distutils import build_ext
   except ImportError:
      if USE_CYTHON=='auto':
         USE_CYTHON=False
      else:
         raise

if USE_CYTHON:
   print "Using Cython"
   ext_modules += [
         Extension("eorepo.eodefault", ['eorepo/eodefault.pyx'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),
         ]
   ext_modules += [
         Extension("eorepo.eobase", ['eorepo/eobase.pyx'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),
         ]

   #cmdclass = {'build_ext' : build_ext}
   cmdclass.update({'build_ext' : build_ext})
else:
   print "Not using Cython"
   ext_modules += [
         Extension("eorepo.eodefault", ['eorepo/eodefault.c'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),
         ]
   ext_modules += [
         Extension("eorepo.eobase", ['eorepo/eobase.c'], include_dirs = e_include_dirs, library_dirs = e_library_dirs, libraries = e_libraries, extra_compile_args = e_compile_args, extra_link_args = e_link_args),
         ]


setup(
      cmdclass = cmdclass,
      name='eoparser_eorepo',
      version='0.1dev',
      author='Yakov Goldberg',
      author_email='yakov.goldberg@gmail.com',
      packages=['eoparser', 'eorepo'],
      package_data={'eoparser': ['data/types.xml'],
         'eorepo': ['EoBase.xml',
                    'eodefault.pxd', 'eobase.pxd',
                    'eodefault.c', 'eobase.c']
         },
      ext_modules = ext_modules,

      data_files=[('/usr/local/share/eoparser/examples', ['examples/evas_elem_test.py', 
                                                          'examples/elm_elm.js',
                                                          'examples/elw_button.js',
                                                          'examples/elw_button_new_names.js',
                                                          'examples/elw_button_old.js',
                                                          'examples/elw_eoisa.js',
                                                          'examples/elw_mixin.js',
                                                          'examples/elw_signal.js',
                                                          'examples/eoisa_test.py',
                                                          'examples/evas_lib_test.py',
                                                          'examples/evas_test.py',
                                                          'examples/evas_test2.py',
                                                          'examples/mixin_test.py',
                                                          'examples/signal_test.py',
                                                          'examples/simple_test.py'
                                                         ])],
      scripts=['bin/eo_xml_gen.py', 'bin/eo_graph_gen.py',
         'bin/eo_py_gen.py', 'bin/eo_js_gen.py'],
      license='GPL',
      long_description=open('README').read(),
      )



