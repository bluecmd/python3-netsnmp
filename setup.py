from distutils.core import setup, Extension
from setuptools import setup, Extension, find_packages
import os
import re
import string
import sys

args = sys.argv[:]
for arg in args:
    if '--basedir' in arg:
        basedir = string.split(arg,'=')[1]
        sys.argv.remove(arg)

netsnmp_libs = os.popen('net-snmp-config --libs').read()
libdirs = re.findall(r" -L(\S+)", netsnmp_libs)
incdirs = []
libs = re.findall(r" -l(\S+)", netsnmp_libs)

setup(
    name="python3-netsnmp", version="1.1a1",
    description = 'The Net-SNMP Python Interface',
    long_description = '''
Python3 port of the official Net-SNMP Python bindings.

Maintainer: Christian Svensson <blue@cmd.nu>

Source: https://github.com/bluecmd/python3-netsnmp
''',
    author = 'G. S. Marzot',
    author_email = 'giovanni.marzot@sparta.com',
    url = 'http://www.net-snmp.org',
    license="BSD",
    packages=find_packages(),
    test_suite = "netsnmp.tests.test",

    ext_modules = [
       Extension("netsnmp.client_intf", ["netsnmp/client_intf.c"],
                 library_dirs=libdirs,
                 include_dirs=incdirs,
                 libraries=libs )
       ]
    )
