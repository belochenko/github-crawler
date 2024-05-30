import unittest
from unittest.mock import patch
from misc.utils import ProxyManager

class TestProxyManager(unittest.TestCase):
    def setUp(self):
        self.proxies = ["proxy1:8080", "proxy2:8080", "proxy3:8080"]
        self.proxy_manager = ProxyManager(self.proxies, max_usage=2)

    def test_init(self):
        self.assertEqual(len(self.proxy_manager.proxies), 3)
        self.assertEqual(self.proxy_manager.max_usage, 2)
        self.assertEqual(len(self.proxy_manager.usage_count), 3)
        self.assertEqual(next(self.proxy_manager.proxy_pool), "proxy1:8080")

    @patch('misc.utils.itertools.cycle')
    def test_get_next_proxy(self, mock_cycle):
        mock_cycle.return_value = iter(self.proxies)
        # Test if proxies are cycled properly
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy1:8080")
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy2:8080")
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy3:8080")
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy1:8080")
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy2:8080")
        self.assertEqual(self.proxy_manager.get_next_proxy(), "http://proxy3:8080")
        # All proxies exhausted, should return None
        self.assertEqual(self.proxy_manager.get_next_proxy(), None)

    def test_ping_proxy(self):
        pass

    def test_get_next_proxy_prefix(self):
        # Test if returned proxies have correct prefix
        proxy = self.proxy_manager.get_next_proxy()
        self.assertTrue(proxy.startswith("http://") or proxy.startswith("https://"))

if __name__ == '__main__':
    unittest.main()
