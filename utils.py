import time
import itertools

class RateLimitHandler:
    def handle(self):
        print("Rate limit exceeded. Waiting for 60 seconds...")
        time.sleep(60)

class ProxyManager:
    def __init__(self, proxies: list):
        self.proxy_pool = itertools.cycle(proxies)

    def get_next_proxy(self):
        return next(self.proxy_pool)
