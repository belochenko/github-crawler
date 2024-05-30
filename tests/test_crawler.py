import unittest
import asyncio
from unittest.mock import MagicMock, patch
from crawler import GitHubCrawler

class TestGitHubCrawler(unittest.TestCase):
    def setUp(self):
        self.data = {
            "keywords": ["openstack", "nova", "css"],
            "proxies": ["http://194.126.37.94:8080", "http://13.78.125.167:8080"],
            "type": "repositories"
        }
        self.crawler = GitHubCrawler(self.data)

    @patch('crawler.ProxyManager.get_next_proxy')
    async def test_construct_github_search(self, mock_get_next_proxy):
        mock_get_next_proxy.return_value = "http://mock_proxy:8080"
        params = await self.crawler.construct_github_search_params()
        self.assertIsNotNone(params)
        self.assertEqual(params['q'], 'openstack+nova+css')
        self.assertEqual(params['type'], 'repositories')

    @patch('crawler.GitHubCrawler.fetch_search_page')
    async def test_get_search_result(self, mock_fetch_search_page):
        mock_fetch_search_page.return_value = '<html>Mock Search Page</html>'
        results = await self.crawler.get_search_result()
        self.assertIsNotNone(results)

    @patch('crawler.GitHubCrawler.fetch_search_page')
    async def test_get_repo_info(self, mock_fetch_search_page):
        mock_fetch_search_page.return_value = '<html>Mock Repo Info Page</html>'
        repo_url = 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'
        repo_info = await self.crawler.get_repo_info(repo_url)
        self.assertIsNotNone(repo_info)

    @patch('crawler.ProxyManager.get_next_proxy')
    async def test_fetch_search_page(self, mock_get_next_proxy):
        mock_get_next_proxy.return_value = "http://mock_proxy:8080"
        session_mock = MagicMock()
        response_mock = MagicMock()
        response_mock.status = 200
        response_mock.text.return_value = '<html>Mock Search Page</html>'
        session_mock.get.return_value.__aenter__.return_value = response_mock
        html = await self.crawler.fetch_search_page('http://mock_url', {})
        self.assertIsNotNone(html)

    @patch('crawler.ProxyManager.get_next_proxy')
    async def test_fetch_search_page_connection_error(self, mock_get_next_proxy):
        mock_get_next_proxy.return_value = "http://mock_proxy:8080"
        session_mock = MagicMock()
        session_mock.get.side_effect = asyncio.TimeoutError
        html = await self.crawler.fetch_search_page('http://mock_url', {})
        self.assertIsNone(html)

    @patch('crawler.ProxyManager.get_next_proxy')
    async def test_fetch_search_page_proxy_error(self, mock_get_next_proxy):
        mock_get_next_proxy.return_value = "http://mock_proxy:8080"
        session_mock = MagicMock()
        session_mock.get.side_effect = aiohttp.ClientProxyConnectionError
        html = await self.crawler.fetch_search_page('http://mock_url', {})
        self.assertIsNone(html)

    async def test_run(self):
        results = await self.crawler.run()
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()
