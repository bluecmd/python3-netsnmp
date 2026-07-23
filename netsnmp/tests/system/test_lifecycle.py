import unittest

import netsnmp

from netsnmp.tests.system.common import (
    READ_ARGS,
    SYS_DESCR,
    SYSTEM,
    assert_value,
)


class SessionLifecycleTests(unittest.TestCase):
    def test_repeated_session_creation(self):
        for _ in range(25):
            session = netsnmp.Session(**READ_ARGS)
            varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))
            assert_value(self, session.get(varlist))
            del session

    def test_repeated_walks(self):
        session = netsnmp.Session(**READ_ARGS)

        for _ in range(10):
            varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
            assert_value(self, session.walk(varlist))
            self.assertGreater(len(varlist), 1)


if __name__ == '__main__':
    unittest.main()
