import unittest

import netsnmp

from netsnmp.tests.system.common import (
    READ_ARGS,
    SYS_DESCR,
    SYS_LOCATION,
    SYS_UPTIME,
    SYSTEM,
    assert_value,
)


class MultiVarbindTests(unittest.TestCase):
    def test_get_multiple_varbinds(self):
        varlist = netsnmp.VarList(
            netsnmp.Varbind(SYS_DESCR, '0'),
            netsnmp.Varbind(SYS_UPTIME, '0'),
            netsnmp.Varbind(SYS_LOCATION, '0'),
        )
        values = netsnmp.Session(**READ_ARGS).get(varlist)

        self.assertEqual(len(values), 3)
        self.assertTrue(all(value is not None for value in values))
        self.assertTrue(all(varbind.val is not None for varbind in varlist))

    def test_getnext_multiple_varbinds(self):
        varlist = netsnmp.VarList(
            netsnmp.Varbind(SYS_DESCR),
            netsnmp.Varbind(SYS_UPTIME),
            netsnmp.Varbind(SYS_LOCATION),
        )
        values = netsnmp.Session(**READ_ARGS).getnext(varlist)

        self.assertEqual(len(values), 3)
        self.assertTrue(all(varbind.tag for varbind in varlist))

    def test_getbulk_multiple_varbinds(self):
        varlist = netsnmp.VarList(
            netsnmp.Varbind(SYSTEM),
            netsnmp.Varbind(SYS_UPTIME),
        )
        values = netsnmp.Session(**READ_ARGS).getbulk(1, 3, varlist)

        assert_value(self, values)
        self.assertGreater(len(values), 2)
        self.assertEqual(len(varlist), len(values))


if __name__ == '__main__':
    unittest.main()
