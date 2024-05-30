import aiohttp
import json
import asyncio
import logging
from parsers.github import GitHubParser
from misc.utils import ProxyManager
from generic.basic_crawler import Crawler

logger = logging.getLogger(__name__)

class GitHubCrawler(Crawler):
    def __init__(self, data):
        self.keywords = data.get("keywords", [])
        self.proxies = data.get("proxies", [])
        self.search_type = data.get("type", "")
        self.proxy_manager = ProxyManager(self.proxies)
        self.parser = GitHubParser()
        self.current_proxy = None
        self.GITHUB_BASE_URL = "https://github.com"
        self.session = None  # Initialize session variable

    async def create_session(self, custom_headers=None):
        """
        Create a new aiohttp session if one does not exist or if the current session is closed.
        """
        if custom_headers is None:
            custom_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(base_url=self.GITHUB_BASE_URL, headers=custom_headers)

    async def close_session(self):
        """
        Close the aiohttp session if it exists and is open.
        """
        if self.session and not self.session.closed:
            await self.session.close()

    async def construct_github_search_params(self):
        """
        Construct the GitHub search URL and parameters.

        Returns:
        - params (dict): Parameters for the GitHub search.
        """
        await self.create_session()

        query = "+".join(self.keywords)
        params = {
            "q": query,
            "type": self.search_type
        }

        self.current_proxy = self.proxy_manager.get_next_proxy()  # This can return None if no proxies are left
        return params

    async def fetch_search_page(self, search_url, params):
        """
        Fetch a GitHub search page.

        Parameters:
        - search_url (str): The search URL.
        - params (dict): Parameters for the search.

        Returns:
        - HTML content of the search page.
        """
        proxy = self.current_proxy
        try:
            async with self.session.get(search_url, params=params, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 429:
                    logger.warning("Rate limit exceeded. Switching proxy...")
                    self.current_proxy = self.proxy_manager.get_next_proxy()
                    if self.current_proxy:
                        return await self.fetch_search_page(search_url, params)
                    else:
                        raise ValueError("There are no more available proxies.")
                else:
                    logger.warning(f"Failed to fetch search results from {response.url}. Status code: {response.status}")
                    return None
        except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError) as e:
            logger.warning(f"Failed to connect to proxy server {proxy}: {e}")
            self.current_proxy = self.proxy_manager.get_next_proxy()
            if self.current_proxy:
                return await self.fetch_search_page(search_url, params)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    async def get_search_result(self, search_url="/search"):
        """
        Get the search results from GitHub.

        Parameters:
        - search_url (str): The URL of the search page.

        Returns:
        - all_results (list): A list of search result URLs.
        """
        params = await self.construct_github_search_params()
        all_results = []

        logger.info("Getting search results and flipping through the pages...")
        try:
            while True:
                html = await self.fetch_search_page(search_url, params)
                if not html:
                    break

                short_repo_location = self.parser.parse_search_results(html, self.search_type)
                all_results.extend(short_repo_location)
                logger.info(f"Page {params.get('p', 1)}, parsed {len(short_repo_location)} entries")

                next_page_url = self.parser.parse_pagination(html)
                if next_page_url:
                    params['p'] = params.get('p', 1) + 1
                else:
                    logger.info(f"Last page was {params.get('p', 1)}")
                    break
        finally:
            await self.close_session()

        return all_results

    async def get_repo_info(self, repo_url):
        """
        Get information about a repository from GitHub.

        Parameters:
        - repo_url (str): The URL of the repository.

        Returns:
        - repo_info (dict): Information about the repository.
        """
        try:
            async with self.session.get(repo_url, proxy=self.current_proxy) as response:
                if response.status == 200:
                    html = await response.text()
                    return self.parser.parse_repo_info(html)
                else:
                    logger.warning(f"Failed to fetch repository info for URL: {repo_url}. Status code: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching repo info: {e}")
            return None

    async def run(self):
        """
        Run the GitHub crawler to fetch search results and repository information.

        Returns:
        - final_results (list): A list of dictionaries containing search results and repository information.
        """
        logger.info("Running GitHub Crawler...")

        search_results = await self.get_search_result()
        final_results = []

        await self.create_session()
        if self.search_type.lower() == "repositories":
            tasks = [self.get_repo_info(result["url"]) for result in search_results]
            repo_infos = await asyncio.gather(*tasks)

            for result, repo_info in zip(search_results, repo_infos):
                if repo_info:
                    result["url"] = self.GITHUB_BASE_URL + result["url"]
                    result["extra"] = repo_info
                    final_results.append(result)
        else:
            for result in search_results:
                result["url"] = self.GITHUB_BASE_URL + result["url"]
                final_results.append(result)

        logger.info(f'No more tasks. Finished with results {json.dumps(final_results, indent=4)}')
        await self.close_session()

        return final_results
