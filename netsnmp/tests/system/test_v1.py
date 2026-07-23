import unittest

import netsnmp

from netsnmp.tests.system.common import (
    READ_ARGS,
    SYS_DESCR,
    SYS_LOCATION,
    SYSTEM,
    WRITE_ARGS,
    assert_value,
)


V1_READ_ARGS = READ_ARGS.copy()
V1_READ_ARGS['Version'] = 1
V1_WRITE_ARGS = WRITE_ARGS.copy()
V1_WRITE_ARGS['Version'] = 1


class SnmpV1Tests(unittest.TestCase):
    def test_get(self):
        values = netsnmp.snmpget(
            netsnmp.Varbind(SYS_DESCR, '0'), **V1_READ_ARGS)
        assert_value(self, values)

    def test_getnext(self):
        values = netsnmp.snmpgetnext(
            netsnmp.Varbind(SYSTEM), **V1_READ_ARGS)
        assert_value(self, values)

    def test_getbulk_is_not_supported(self):
        session = netsnmp.Session(**V1_READ_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        self.assertIsNone(session.getbulk(0, 4, varlist))

    def test_set(self):
        value = b'snmp-v1'
        result = netsnmp.snmpset(
            netsnmp.Varbind(SYS_LOCATION, '0', value, 'OCTETSTR'),
            **V1_WRITE_ARGS)
        self.assertEqual(result, 1)
        self.assertEqual(netsnmp.snmpget(
            netsnmp.Varbind(SYS_LOCATION, '0'), **V1_READ_ARGS)[0], value)

    def test_walk(self):
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, netsnmp.snmpwalk(varlist, **V1_READ_ARGS))
        self.assertGreater(len(varlist), 1)


if __name__ == '__main__':
    unittest.main()
