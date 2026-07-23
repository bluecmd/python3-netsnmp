import unittest

import netsnmp

from netsnmp.tests.system.common import READ_ARGS, SYS_DESCR, SYS_LOCATION


class ErrorPathTests(unittest.TestCase):
    def test_unknown_oid_returns_no_value(self):
        varbind = netsnmp.Varbind('.1.3.6.1.2.1.1.999', '0')
        values = netsnmp.snmpget(varbind, **READ_ARGS)

        self.assertEqual(values, (None,))
        self.assertIn(varbind.type, ('NOSUCHOBJECT', 'NOSUCHINSTANCE'))

    def test_unknown_instance_returns_no_value(self):
        varbind = netsnmp.Varbind(SYS_DESCR, '123')

        self.assertEqual(netsnmp.snmpget(varbind, **READ_ARGS), (None,))
        self.assertEqual(varbind.type, 'NOSUCHINSTANCE')

    def test_read_only_set_is_rejected(self):
        session = netsnmp.Session(**READ_ARGS)
        varlist = netsnmp.VarList(
            netsnmp.Varbind(
                SYS_LOCATION, '0', b'not-written', 'OCTETSTR'))

        self.assertEqual(session.set(varlist), 0)
        self.assertTrue(session.ErrorStr)
        self.assertNotEqual(session.ErrorNum, 0)

    def test_timeout_updates_session_error(self):
        timeout_args = READ_ARGS.copy()
        timeout_args['DestHost'] = '127.0.0.1:1162'
        timeout_args['Timeout'] = 100000
        session = netsnmp.Session(**timeout_args)
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR, '0'))

        self.assertEqual(session.get(varlist), (None,))
        self.assertTrue(session.ErrorStr)
        self.assertNotEqual(session.ErrorInd, 0)


if __name__ == '__main__':
    unittest.main()
