import argparse
import asyncio
import json
from crawler import GitHubCrawler
from misc.logging_config import setup_logger

async def main(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON in '{config_file}'.")
        return

    github_crawler = GitHubCrawler(config)
    await github_crawler.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GitHub Crawler')
    parser.add_argument('--config', default='config.json', help='Path to the configuration file')
    args = parser.parse_args()

    logger = setup_logger()
    asyncio.run(main(args.config))
