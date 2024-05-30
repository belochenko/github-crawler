import unittest
from parsers.github import GitHubParser

class TestGitHubParser(unittest.TestCase):
    def test_parse_search_results(self):
        html = """
        <div data-testid="results-list">
            <div class="search-title">
                <a href="/repo1">Repository 1</a>
            </div>
            <div class="search-title">
                <a href="/repo2">Repository 2</a>
            </div>
        </div>
        """
        search_results = GitHubParser.parse_search_results(html, 'repositories')
        expected_results = [{"url": "/repo1"}, {"url": "/repo2"}]
        self.assertEqual(search_results, expected_results)

    def test_parse_pagination(self):
        html = """
        <nav aria-label="Pagination">
            <a rel="prev" href="/prev">Previous</a>
            <a rel="next" href="/next">Next</a>
        </nav>
        """
        next_page_url = GitHubParser.parse_pagination(html)
        self.assertEqual(next_page_url, "/next")

    def test_parse_pagination_no_next(self):
        html = """
        <nav aria-label="Pagination">
            <a rel="prev" href="/prev">Previous</a>
        </nav>
        """
        next_page_url = GitHubParser.parse_pagination(html)
        self.assertIsNone(next_page_url)

    def test_parse_repo_info(self):
        html = """
        <span class="author">Owner</span>
        <span class="Progress-item" aria-label="Python 50%">Python 50%</span>
        <span class="Progress-item" aria-label="JavaScript 30%">JavaScript 30%</span>
        """
        repo_info = GitHubParser.parse_repo_info(html)
        expected_info = {"owner": "Owner", "language_stats": {"Python": 50.0, "JavaScript": 30.0}}
        self.assertEqual(repo_info, expected_info)

if __name__ == '__main__':
    unittest.main()
