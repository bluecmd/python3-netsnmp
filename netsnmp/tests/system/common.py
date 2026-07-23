HOST = '127.0.0.1:1161'
READ_ARGS = {
    'Version': 2,
    'DestHost': HOST,
    'Community': 'public',
    'Timeout': 1000000,
    'Retries': 0,
}
WRITE_ARGS = READ_ARGS.copy()
WRITE_ARGS['Community'] = 'private'

# SNMPv3 authPriv credentials. Keep in sync with the createUser/rwuser
# directives in netsnmp/tests/system/snmpd.conf.
V3_ARGS = {
    'Version': 3,
    'DestHost': HOST,
    'SecLevel': 'authPriv',
    'SecName': 'testuser',
    'AuthProto': 'SHA',
    'AuthPass': 'auth_pass',
    'PrivProto': 'AES',
    'PrivPass': 'priv_pass',
    'Timeout': 1000000,
    'Retries': 0,
}

SYS_DESCR = '.1.3.6.1.2.1.1.1'
SYS_UPTIME = '.1.3.6.1.2.1.1.3'
SYS_LOCATION = '.1.3.6.1.2.1.1.6'
SYSTEM = '.1.3.6.1.2.1.1'


def assert_value(test_case, values):
    test_case.assertIsInstance(values, tuple)
    test_case.assertTrue(values)
    test_case.assertIsNotNone(values[0])
