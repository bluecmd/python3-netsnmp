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

def netsnmp_config(flag):
    cmd = 'net-snmp-config ' + flag
    if sys.platform == 'win32':
        # net-snmp-config is a POSIX shell script; on Windows os.popen goes
        # through cmd.exe which can't execute it, so run it via sh (available
        # in the MSYS2/mingw environment used to build the extension).
        cmd = 'sh -c "net-snmp-config %s"' % flag
    return os.popen(cmd).read()

netsnmp_libs = netsnmp_config('--libs')
libdirs = re.findall(r" -L(\S+)", netsnmp_libs)
incdirs = []
libs = re.findall(r" -l(\S+)", netsnmp_libs)
if sys.platform == 'win32':
    # inet_addr() and the winsock symbols net-snmp relies on come from ws2_32.
    libs.append('ws2_32')

setup(
    name="python3-netsnmp", version="1.1a2",
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
