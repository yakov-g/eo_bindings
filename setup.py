from distutils.core import setup

setup(
    name='eoparser',
    version='0.1dev',
    packages=['eoparser',],
    package_data={'eoparser': ['data/types.xml']},
    scripts=['bin/eo_xml_gen.py', 'bin/eo_graph_gen.py'],
    license='GPL',
    long_description=open('README').read(),
)
