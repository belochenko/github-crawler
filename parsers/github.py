from bs4 import BeautifulSoup

class GitHubParser:
    """
    A utility class for parsing HTML responses from GitHub.

    Methods:
        parse_search_results(html, search_type):
            Parses the search results HTML to extract repository, issue, or wiki URLs.
        
        parse_pagination(html):
            Parses the HTML to extract the URL of the next page, if available.
        
        parse_repo_info(html):
            Parses the HTML of a repository page to extract owner information and language statistics.
    """
    @staticmethod
    def parse_search_results(html, search_type):
        """
        Parses the HTML of search results to extract URLs of repositories, issues, or wikis.

        Args:
            html (str): The HTML content of the search results page.
            search_type (str): The type of search results to parse ('repositories', 'issues', or 'wikis').

        Returns:
            list: A list of dictionaries containing the URLs of the search results.
        """
        available_types = ["repositories", "issues", "wikis"]
        soup = BeautifulSoup(html, 'html.parser')
        result_list_div = soup.find('div', {'data-testid': 'results-list'})
        result_urls = []

        if search_type.lower() in available_types:
            if result_list_div:
                repositories = result_list_div.find_all('div', {'class': 'search-title'})
                for repo in repositories:
                    link = repo.find('a', href=lambda href: href and not href.startswith('/login?return_to='))
                    if link:
                        result_urls.append({"url": link['href']})

        return result_urls

    @staticmethod
    def parse_pagination(html):
        """
        Parses the HTML to extract the URL of the next page, if available.

        Args:
            html (str): The HTML content of the page containing pagination.

        Returns:
            str or None: The URL of the next page, or None if no next page is found.
        """
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find('nav', {'aria-label': 'Pagination'})
        if pagination:
            next_page = pagination.find('a', {'rel': 'next'})
            if next_page:
                return next_page['href']
        return None

    @staticmethod
    def parse_repo_info(html):
        """
        Parses the HTML of a repository page to extract owner information and language statistics.

        Args:
            html (str): The HTML content of the repository page.

        Returns:
            dict: A dictionary containing owner information and language statistics.
        """
        soup = BeautifulSoup(html, 'html.parser')
        owner = soup.find('span', class_='author').text.strip()
        language_stats = {}

        # Find the 'Progress' span that contains the language statistics
        progress_items = soup.find_all('span', class_='Progress-item')
        for item in progress_items:
            aria_label = item.get('aria-label')
            if aria_label:
                language, percentage = aria_label.split()
                percentage = float(percentage.replace('%', ''))
                language_stats[language] = percentage

        return {"owner": owner, "language_stats": language_stats}
