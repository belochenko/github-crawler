from aiohttp.client import ClientTimeout
import requests
import aiohttp
import logging
from parser import GitHubParser
from utils import RateLimitHandler, ProxyManager

logger = logging.getLogger(__name__)

class GitHubCrawler:
    def __init__(self, data):
        self.keywords = data.get("keywords", [])
        self.proxies = data.get("proxies", [])
        self.search_type = data.get("type", "")

        self.session = requests.Session()
        self.rate_limit_handler = RateLimitHandler()
        self.proxy_manager = ProxyManager(self.proxies)
        self.parser = GitHubParser()
        self.current_proxy = None

        self.GITHUB_BASE_URL = "https://github.com"

    def construct_github_search(self, custom_header=None):
        if custom_header is None:
            custom_header = {
                "Accept": "text/html"
            }

        query = "+".join(self.keywords)

        params = {
            "q": query,
            "type": self.search_type
        }

        if not self.current_proxy:
            self.current_proxy = 'http://' + self.proxy_manager.get_next_proxy()

        session = aiohttp.ClientSession(base_url=self.GITHUB_BASE_URL,
            headers=custom_header)
        return session, params


    async def fetch_search_page(self, session, search_url, params, proxy):
        try:
            async with session.get(search_url, params=params, proxy=proxy,) as response:
                if response.status == 200:
                    html = await response.text()
                    return html
                elif response.status == 429:
                    self.current_proxy = 'http://' + self.proxy_manager.get_next_proxy()
                    return self.fetch_search_page(search_url, session, params, proxy)
                else:
                    logger.warning(f"Failed to fetch search results from {response.url}. Status code: {response.status}")
                    return None
        except aiohttp.ClientProxyConnectionError and aiohttp.ClientHttpProxyError as e:
                logger.warning(f"Failed to connect to proxy server {proxy}: {e}")
                self.current_proxy = 'http://' + self.proxy_manager.get_next_proxy()  # Switch to the next proxy
                return await self.fetch_search_page(session, search_url, params, self.current_proxy)  # Retry with the next proxy

    async def get_search_result(self, url="/search"):
        session, params = self.construct_github_search()
        proxy = self.current_proxy
        all_results = []
        page = 1
        logger.info(f"Getting search result and and flipping through the pages...")
        while True:
            async with session:
                html = await self.fetch_search_page(session, url, params, proxy)
                if not html:
                    break

                result_urls = self.parser.parse_search_results(html, self.search_type)
                logger.info(f"Now {page} page, parsed {len(result_urls)} entries")
                all_results.extend(result_urls)
                logger.info(f"{all_results}")

                next_page_url = self.parser.parse_pagination(html)
                if next_page_url:
                    page += 1
                    params['p'] = page
                else:
                    logger.info(f"Last page was {page}")
                    break

        return all_results

    async def get_repo_info(self, repo_url):
        session, _ = self.construct_github_search()
        proxy = self.current_proxy
        async with session:
            async with session.get(repo_url, proxy=proxy) as response:
                if response.status == 200:
                    html = await response.text()
                    return self.parser.parse_repo_info(html)
                else:
                    logger.warning(f"Failed to fetch repository info for URL: {repo_url}. Status code: {response.status}")
                    return None

    async def run(self):
        search_results = await self.get_search_result()
        final_results = []
        for result in search_results:
            repo_info = await self.get_repo_info(result["url"])
            if repo_info:
                result["extra"] = repo_info
                final_results.append(result)
        return final_results
