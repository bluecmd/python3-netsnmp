import unittest

import netsnmp

from netsnmp.tests.system.common import READ_ARGS, SYSTEM, assert_value


class GetNextTests(unittest.TestCase):
    def test_convenience_function(self):
        varbind = netsnmp.Varbind(SYSTEM)
        assert_value(self, netsnmp.snmpgetnext(varbind, **READ_ARGS))
        self.assertTrue(varbind.tag)

    def test_session_method(self):
        session = netsnmp.Session(**READ_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, session.getnext(varlist))


if __name__ == '__main__':
    unittest.main()
