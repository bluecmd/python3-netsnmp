import unittest

import netsnmp

from netsnmp.tests.system.common import READ_ARGS, SYS_DESCR, assert_value


class GetTests(unittest.TestCase):
    def test_convenience_function(self):
        values = netsnmp.snmpget(
            netsnmp.Varbind(SYS_DESCR, '0'), **READ_ARGS)
        assert_value(self, values)

    def test_session_method(self):
        session = netsnmp.Session(**READ_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))
        assert_value(self, session.get(varlist))


if __name__ == '__main__':
    unittest.main()
