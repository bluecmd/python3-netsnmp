import unittest

import netsnmp

from netsnmp.tests.system.common import SYS_DESCR


class VarbindTests(unittest.TestCase):
    def test_complete_numeric_oid_is_preserved(self):
        varbind = netsnmp.Varbind(SYS_DESCR + '.0')

        self.assertEqual(varbind.tag, SYS_DESCR + '.0')
        self.assertEqual(varbind.iid, '')

    def test_explicit_iid_is_converted_to_string(self):
        varbind = netsnmp.Varbind(SYS_DESCR, 0)

        self.assertEqual(varbind.tag, SYS_DESCR)
        self.assertEqual(varbind.iid, '0')

    def test_value_preserves_its_type(self):
        byte_value = netsnmp.Varbind(SYS_DESCR, '0', b'value')
        integer_value = netsnmp.Varbind(SYS_DESCR, '0', 42)

        self.assertEqual(byte_value.val, b'value')
        self.assertEqual(integer_value.val, 42)

    def test_print_str_returns_all_fields(self):
        varbind = netsnmp.Varbind(SYS_DESCR, '0', b'value', 'OCTETSTR')

        self.assertEqual(
            varbind.print_str(),
            (SYS_DESCR, '0', b'value', 'OCTETSTR'))


if __name__ == '__main__':
    unittest.main()
