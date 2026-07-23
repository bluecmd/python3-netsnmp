#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd)
cd "$ROOT"

rm -rf build
rm -f netsnmp/client_intf*.so

SANITIZERS=address,undefined
CFLAGS="-O1 -g -fno-omit-frame-pointer -fsanitize=$SANITIZERS" \
LDFLAGS="-fsanitize=$SANITIZERS" \
LD_PRELOAD=$(gcc -print-file-name=libasan.so) \
ASAN_OPTIONS=detect_leaks=0:abort_on_error=1 \
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
RUN_VALGRIND=0 \
    sh netsnmp/tests/system/run.sh