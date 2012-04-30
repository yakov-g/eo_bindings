#python setup_c_eobj.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import commands

def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    for token in commands.getoutput("pkg-config --libs --cflags %s" % ' '.join(packages)).split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw

res = pkgconfig('elementary', 'eobj')

my_include_dirs = res["include_dirs"]
my_library_dirs = res["library_dirs"]
my_libraries = res["libraries"]

#my_include_dirs.append("./../lib")
#my_include_dirs.append("./../examples/evas")
my_libraries.append("myelm")

setup(
      cmdclass = {'build_ext': build_ext},
      ext_modules = [
        Extension("eobjdefault", ['eobjdefault.pyx'], include_dirs = my_include_dirs, library_dirs = my_library_dirs, libraries = my_libraries),
        Extension("eobjbase", ['eobjbase.pyx'], include_dirs = my_include_dirs,	library_dirs = my_library_dirs, 	libraries = my_libraries),
	  	Extension("evasobject", ['evasobject.pyx'],	include_dirs = my_include_dirs,	library_dirs = my_library_dirs, libraries = my_libraries),
        Extension("elwwin", ['elwwin.pyx'],	include_dirs = my_include_dirs, library_dirs = my_library_dirs, libraries = my_libraries),
	  	Extension("elwbutton", ['elwbutton.pyx'], include_dirs = my_include_dirs, library_dirs = my_library_dirs, libraries = my_libraries),
	  	Extension("elwbox", ['elwbox.pyx'], include_dirs = my_include_dirs, library_dirs = my_library_dirs, libraries = my_libraries),
	  	Extension("elwboxedbutton", ['elwboxedbutton.pyx'], include_dirs = my_include_dirs,	library_dirs = my_library_dirs, libraries = my_libraries)
	  ]
)
