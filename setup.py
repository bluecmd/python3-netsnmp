"""Build the netsnmp C extension.

Static project metadata lives in pyproject.toml. This file only remains for
the parts that can't be expressed declaratively: the net-snmp client library
is discovered at build time via net-snmp-config.
"""
import os
import re
import sys

from setuptools import Extension, setup


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
    ext_modules=[
        Extension(
            "netsnmp.client_intf",
            ["netsnmp/client_intf.c"],
            library_dirs=libdirs,
            include_dirs=incdirs,
            libraries=libs,
        )
    ],
)
