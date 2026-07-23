import unittest

import netsnmp

from netsnmp.tests.system.common import READ_ARGS, SYSTEM, assert_value


class WalkTests(unittest.TestCase):
    def test_convenience_function(self):
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, netsnmp.snmpwalk(varlist, **READ_ARGS))
        self.assertGreater(len(varlist), 1)

    def test_session_method(self):
        session = netsnmp.Session(**READ_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, session.walk(varlist))
        self.assertGreater(len(varlist), 1)


if __name__ == '__main__':
    unittest.main()
