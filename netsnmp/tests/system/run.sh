#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd)
RUNTIME_DIR=$(mktemp -d)
SNMPD_PID=

cleanup() {
    if [ -n "$SNMPD_PID" ]; then
        kill "$SNMPD_PID" 2>/dev/null || true
        wait "$SNMPD_PID" 2>/dev/null || true
    fi
    rm -rf "$RUNTIME_DIR"
}
trap cleanup EXIT INT TERM

cd "$ROOT"
python3 setup.py build_ext --inplace

SNMPD_CONFIG="$RUNTIME_DIR/snmpd.conf"
cat "$ROOT/netsnmp/tests/system/snmpd.conf" >"$SNMPD_CONFIG"
printf '\npersistentDir %s\n' "$RUNTIME_DIR" >>"$SNMPD_CONFIG"

snmpd -f -Lo -C \
    -c "$SNMPD_CONFIG" \
    -p "$RUNTIME_DIR/snmpd.pid" \
    >"$RUNTIME_DIR/snmpd.log" 2>&1 &
SNMPD_PID=$!

attempt=0
until snmpget -v2c -c public -t 1 -r 0 \
        127.0.0.1:1161 .1.3.6.1.2.1.1.1.0 >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 20 ] || ! kill -0 "$SNMPD_PID" 2>/dev/null; then
        cat "$RUNTIME_DIR/snmpd.log"
        exit 1
    fi
done

python3 -m unittest discover -v -s netsnmp/tests/system -p 'test_*.py'

valgrind \
    --error-exitcode=99 \
    --leak-check=full \
    --show-leak-kinds=definite \
    --errors-for-leak-kinds=definite \
    --track-origins=yes \
    --log-file="$RUNTIME_DIR/valgrind.log" \
    python3 -m unittest discover -v -s netsnmp/tests/system \
        -p 'test_*.py' || {
        status=$?
        cat "$RUNTIME_DIR/valgrind.log"
        exit "$status"
    }

cat "$RUNTIME_DIR/valgrind.log"
