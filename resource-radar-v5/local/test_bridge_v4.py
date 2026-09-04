import importlib.util
import ipaddress
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).with_name("siiaos_bridge_v4.py")
SPEC = importlib.util.spec_from_file_location("siiaos_bridge_v4", MODULE_PATH)
bridge = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(bridge)


class BridgeSecurityTests(unittest.TestCase):
    def test_safe_target_stays_under_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = bridge.safe_target(root, "../../outside", "../payload.bin")
            self.assertTrue(target.is_relative_to(root.resolve()))
            self.assertEqual(target.name, "_payload.bin")

    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ValueError):
            bridge.validate_http_url("file:///etc/passwd", set())

    def test_rejects_userinfo(self):
        with self.assertRaises(ValueError):
            bridge.validate_http_url("https://user:pass@example.org/file", set())

    def test_rejects_private_resolution(self):
        fake = [(2, 1, 6, "", ("127.0.0.1", 0))]
        with mock.patch.object(bridge.socket, "getaddrinfo", return_value=fake):
            with self.assertRaises(ValueError):
                bridge.validate_http_url("https://example.invalid/file", set())

    def test_allows_explicit_private_host_override(self):
        with mock.patch.object(bridge.socket, "getaddrinfo") as resolver:
            parsed = bridge.validate_http_url("http://mirror.local/file", {"mirror.local"})
            self.assertEqual(parsed.hostname, "mirror.local")
            resolver.assert_not_called()

    def test_global_ip_classification_assumption(self):
        self.assertTrue(ipaddress.ip_address("8.8.8.8").is_global)
        self.assertFalse(ipaddress.ip_address("10.0.0.1").is_global)


if __name__ == "__main__":
    unittest.main()
