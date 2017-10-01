# coding: U8


import re

from distutils.core import setup


mod_name = 'pprofiler'


def find_version(filename):
    version_file = open(filename, 'r').read()
    version_match = re.search(r'''^__version__ = ['"]([^'"]*)['"]''', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name=mod_name,
    version=find_version(mod_name + '.py'),
    py_modules=[mod_name],
    author='Alexey Michurin',
    author_email='a.michurin@gmail.com',
    url='https://github.com/michurin/pprofiler',
    description='Python code level profiler',
    long_description='Python code level profiler with nested scopes',
    platforms=['any'],
    license='MIT License',
)
