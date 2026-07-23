import unittest

import netsnmp

from netsnmp.tests.system.common import READ_ARGS, SYSTEM, assert_value


class GetBulkTests(unittest.TestCase):
    def test_convenience_function(self):
        values = netsnmp.snmpgetbulk(
            0, 4, netsnmp.Varbind(SYSTEM), **READ_ARGS)
        assert_value(self, values)

    def test_session_method(self):
        session = netsnmp.Session(**READ_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, session.getbulk(0, 4, varlist))


if __name__ == '__main__':
    unittest.main()
