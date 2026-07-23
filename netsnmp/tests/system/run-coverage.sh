#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd)
cd "$ROOT"

rm -rf build
rm -f netsnmp/client_intf*.so

CFLAGS='--coverage -O0' \
LDFLAGS='--coverage' \
RUN_VALGRIND=0 \
    sh netsnmp/tests/system/run.sh

OBJECT_DIR=$(dirname "$(find build -name client_intf.o -print -quit)")
gcov -b -f -o "$OBJECT_DIR" netsnmp/client_intf.c \
    | tee client_intf-coverage.txt

awk -F: '
    /memcpy\(oid_arr_broken_check\[varlist_ind\]/ ||
    /snmp_free_pdu\(newpdu\)/ {
        count++
        executed = $1
        gsub(/[[:space:]]/, "", executed)
        if (executed !~ /^[1-9][0-9]*$/)
            exit 1
    }
    END { if (count != 3) exit 1 }
' client_intf.c.gcov