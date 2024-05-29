import asyncio
from crawler import GitHubCrawler
from logging_config import setup_logger

logger = setup_logger()

async def main():
    logger.info("Starting the main function...")

    crawler_target_settings = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            "195.114.209.50:80"
            # "79.174.12.190:80",
            # "117.54.114.102:80",
            # "50.168.72.117:80",
            # "50.144.161.167:80",
            # "50.221.74.130:80",
            # "50.175.212.77:80",
            # "50.168.72.118:80",
            # "50.169.135.10:80",
            # "50.207.199.83:80",
            # "50.172.75.126:80",
            # "50.207.199.81:80",
            # "50.231.104.58:80",
            # "50.217.226.42:80",
            # "50.222.245.50:80",
            # "50.174.145.13:80",
            # "50.174.7.152:80",
            # "50.168.163.180:80",
            # "50.222.245.46:80",
            # "50.174.7.155:80",
            # "50.223.239.177:80",
            # "50.174.7.153:80",
            # "50.173.182.90:80",
            # "50.207.199.86:80"
        ],
        "type": "repositories"
    }

    logger.info("Running GitHub Crawler...")
    github_crawler = GitHubCrawler(crawler_target_settings)
    results = await github_crawler.run()

if __name__ == "__main__":
    asyncio.run(main())
