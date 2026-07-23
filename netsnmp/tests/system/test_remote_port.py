import socket
import unittest

import netsnmp


class RemotePortTests(unittest.TestCase):
    def assert_request_received(
            self, version, dest_host, use_remote_port=False):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listener:
            listener.bind(('127.0.0.1', 0))
            listener.settimeout(1)
            port = listener.getsockname()[1]
            session_args = {
                'Version': version,
                'DestHost': dest_host.format(port=port),
                'Community': 'public',
                'Timeout': 1000,
                'Retries': 0,
            }
            if use_remote_port:
                session_args['RemotePort'] = port
            session = netsnmp.Session(**session_args)
            varlist = netsnmp.VarList(
                netsnmp.Varbind('.1.3.6.1.2.1.1.1', '0'))

            session.get(varlist)
            request, _ = listener.recvfrom(65535)
            self.assertTrue(request)

    def test_remote_port_selects_destination_port(self):
        for version in (1, 2, 3):
            with self.subTest(version=version):
                self.assert_request_received(
                    version, '127.0.0.1', use_remote_port=True)

    def test_dest_host_port_remains_supported(self):
        for version in (1, 2, 3):
            with self.subTest(version=version):
                self.assert_request_received(
                    version, '127.0.0.1:{port}')


if __name__ == '__main__':
    unittest.main()
