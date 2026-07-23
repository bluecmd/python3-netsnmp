import unittest

import netsnmp

from netsnmp.tests.system.common import SYS_DESCR, SYS_LOCATION


class VarListTests(unittest.TestCase):
    def test_constructor_wraps_oid(self):
        varlist = netsnmp.VarList(SYS_DESCR)

        self.assertEqual(len(varlist), 1)
        self.assertIsInstance(varlist[0], netsnmp.Varbind)
        self.assertEqual(varlist[0].tag, SYS_DESCR)

    def test_append_iterate_and_delete(self):
        first = netsnmp.Varbind(SYS_DESCR, '0')
        second = netsnmp.Varbind(SYS_LOCATION, '0')
        varlist = netsnmp.VarList(first)

        varlist.append(second)
        self.assertEqual(list(varlist), [first, second])

        del varlist[0]
        self.assertEqual(list(varlist), [second])

    def test_append_rejects_non_varbind(self):
        varlist = netsnmp.VarList()

        with self.assertRaises(TypeError):
            varlist.append(SYS_DESCR)

    def test_assignment_rejects_non_varbind(self):
        varlist = netsnmp.VarList(netsnmp.Varbind(SYS_DESCR))

        with self.assertRaises(TypeError):
            varlist[0] = SYS_LOCATION


if __name__ == '__main__':
    unittest.main()
