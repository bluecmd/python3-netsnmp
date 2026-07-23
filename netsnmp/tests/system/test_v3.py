import unittest

import netsnmp

from netsnmp.tests.system.common import (
    SYS_DESCR,
    SYS_LOCATION,
    SYSTEM,
    V3_ARGS,
    assert_value,
)


class SnmpV3Tests(unittest.TestCase):
    """SNMPv3 authPriv coverage (USM authentication and privacy)."""

    def test_get(self):
        values = netsnmp.snmpget(netsnmp.Varbind(SYS_DESCR, '0'), **V3_ARGS)
        assert_value(self, values)

    def test_getnext(self):
        values = netsnmp.snmpgetnext(netsnmp.Varbind(SYSTEM), **V3_ARGS)
        assert_value(self, values)

    def test_getbulk(self):
        session = netsnmp.Session(**V3_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, session.getbulk(0, 4, varlist))
        self.assertGreater(len(varlist), 1)

    def test_set(self):
        value = b'snmp-v3'
        result = netsnmp.snmpset(
            netsnmp.Varbind(SYS_LOCATION, '0', value, 'OCTETSTR'), **V3_ARGS)
        self.assertEqual(result, 1)
        self.assertEqual(netsnmp.snmpget(
            netsnmp.Varbind(SYS_LOCATION, '0'), **V3_ARGS)[0], value)

    def test_walk(self):
        varlist = netsnmp.VarList(netsnmp.Varbind(SYSTEM))
        assert_value(self, netsnmp.snmpwalk(varlist, **V3_ARGS))
        self.assertGreater(len(varlist), 1)

    def test_session_get(self):
        session = netsnmp.Session(**V3_ARGS)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))
        assert_value(self, session.get(varlist))

    def test_unknown_user_is_rejected(self):
        session = netsnmp.Session(**dict(V3_ARGS, SecName='nosuchuser'))
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))
        values = session.get(varlist)
        self.assertFalse(values and values[0])

    def test_wrong_auth_password_is_rejected(self):
        """Proves the agent really enforces authPriv, so the tests above are
        not silently passing over an unauthenticated session.

        Uses a dedicated user rather than the one above: net-snmp caches
        localized USM keys per (engineID, username) process-wide, so reusing
        a name that already authenticated successfully would reuse the good
        key and the wrong passphrase would never reach the agent.
        """
        session = netsnmp.Session(
            **dict(V3_ARGS, SecName='baduser', AuthPass='wrong_auth_pass',
                   PrivPass='wrong_priv_pass'))
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))
        values = session.get(varlist)
        self.assertFalse(values and values[0])


if __name__ == '__main__':
    unittest.main()
