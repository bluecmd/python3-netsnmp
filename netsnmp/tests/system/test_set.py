import socket
import unittest

import netsnmp

from netsnmp.tests.system.common import (
    READ_ARGS,
    SYS_LOCATION,
    WRITE_ARGS,
)


TEST_INTEGER = '.1.3.6.1.4.1.8072.9999.9999.1'


class SetTests(unittest.TestCase):
    def test_accepts_canonical_scalar_values(self):
        read_session = netsnmp.Session(**READ_ARGS)
        write_session = netsnmp.Session(**WRITE_ARGS)
        values = (
            (73, b'73'),
            ('74', b'74'),
            (b'75', b'75'),
        )

        for value, expected in values:
            with self.subTest(value=value):
                varbind = netsnmp.Varbind(
                    TEST_INTEGER, '0', value, 'INTEGER')
                self.assertEqual(
                    write_session.set(netsnmp.VarList(varbind)), 1)
                self.assertEqual(
                    read_session.get(netsnmp.VarList(
                        netsnmp.Varbind(TEST_INTEGER, '0'))),
                    (expected,))

    def test_accepts_text_octet_string_values(self):
        read_session = netsnmp.Session(**READ_ARGS)
        write_session = netsnmp.Session(**WRITE_ARGS)

        for value, expected in (
                ('text-value', b'text-value'),
                (b'bytes-value', b'bytes-value')):
            with self.subTest(value=value):
                varbind = netsnmp.Varbind(
                    SYS_LOCATION, '0', value, 'OCTETSTR')
                self.assertEqual(
                    write_session.set(netsnmp.VarList(varbind)), 1)
                self.assertEqual(
                    read_session.get(netsnmp.VarList(
                        netsnmp.Varbind(SYS_LOCATION, '0'))),
                    (expected,))

    def test_accepts_binary_octet_string(self):
        value = b'\x00\xff'

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listener:
            listener.bind(('127.0.0.1', 0))
            listener.settimeout(1)
            port = listener.getsockname()[1]
            session = netsnmp.Session(
                Version=2,
                DestHost='127.0.0.1:{}'.format(port),
                Community='public',
                Timeout=1000,
                Retries=0,
            )
            varbind = netsnmp.Varbind(
                SYS_LOCATION, '0', value, 'OCTETSTR')

            self.assertEqual(session.set(netsnmp.VarList(varbind)), 0)
            request, _ = listener.recvfrom(65535)
            self.assertIn(value, request)

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
