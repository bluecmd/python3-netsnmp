# System tests

The system tests start a private SNMPv2c agent on `127.0.0.1:1161`, exercise
all convenience functions and `Session` methods, and repeat the test suite
under Valgrind. Each SNMP operation has a separate `test_*.py` file, and the
runner discovers new test files automatically.

The normal and Valgrind suites each run all discovered tests in one process.

Coverage also includes SNMPv1, multiple varbinds, protocol error paths,
repeated session and walk lifecycles, and the Python `Varbind` and `VarList`
containers.

Run the same Ubuntu environment locally with Podman:

```sh
podman build -f Containerfile.system-tests -t python3-netsnmp-system-tests .
podman run --rm python3-netsnmp-system-tests
```

Valgrind returns a non-zero status for memory errors and definite leaks.
GitHub Actions runs the same test script for every pull request.
