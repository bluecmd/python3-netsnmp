import unittest

import netsnmp

from netsnmp.tests.system.common import (
    READ_ARGS,
    SYS_LOCATION,
    WRITE_ARGS,
)


class SetTests(unittest.TestCase):
    def test_convenience_function(self):
        value = b'convenience-api'
        result = netsnmp.snmpset(
            netsnmp.Varbind(SYS_LOCATION, '0', value, 'OCTETSTR'),
            **WRITE_ARGS)
        self.assertEqual(result, 1)
        self.assertEqual(netsnmp.snmpget(
            netsnmp.Varbind(SYS_LOCATION, '0'), **READ_ARGS)[0], value)

    def test_session_method(self):
        read_session = netsnmp.Session(**READ_ARGS)
        write_session = netsnmp.Session(**WRITE_ARGS)
        value = b'session-api'
        set_vars = netsnmp.VarList(
            netsnmp.Varbind(SYS_LOCATION, '0', value, 'OCTETSTR'))
        self.assertEqual(write_session.set(set_vars), 1)

        verify_vars = netsnmp.VarList(netsnmp.Varbind(SYS_LOCATION, '0'))
        self.assertEqual(read_session.get(verify_vars)[0], value)


if __name__ == '__main__':
    unittest.main()
