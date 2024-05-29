# parser.py
from bs4 import BeautifulSoup

class GitHubParser:
    @staticmethod
    def parse_search_results(html, search_type):
        soup = BeautifulSoup(html, 'html.parser')
        result_list_div = soup.find('div', {'data-testid': 'results-list'})
        result_urls = []

        if result_list_div:
            if search_type == "Repositories":
                repositories = result_list_div.find_all('a', href=True)
                for repo in repositories:
                    result_urls.append({"url": "https://github.com" + repo['href']})

        return result_urls

    @staticmethod
    def parse_pagination(html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find('nav', {'aria-label': 'Pagination'})
        if pagination:
            next_page = pagination.find('a', {'rel': 'next'})
            if next_page:
                return next_page['href']
        return None

    @staticmethod
    def parse_repo_info(html):
        soup = BeautifulSoup(html, 'html.parser')
        owner = soup.find('span', class_='author').text.strip()
        language_stats = {}
        languages = soup.find_all('span', class_='lang')
        for lang in languages:
            language = lang.text.strip()
            percentage = float(lang.find_next_sibling('span').text.replace('%', ''))
            language_stats[language] = percentage
        return {"owner": owner, "language_stats": language_stats}
