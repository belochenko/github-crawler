import itertools

class ProxyManager:
    """
    Manages a pool of proxies for use in web crawling.

    This class keeps track of how many times each proxy has been used and cycles through them,
    ensuring that no proxy is used more than a specified maximum number of times.

    Attributes:
        proxies (list): A list of proxy addresses.
        max_usage (int): The maximum number of times each proxy can be used.
        usage_count (dict): A dictionary mapping each proxy to its current usage count.
        proxy_pool (itertools.cycle): An iterator that cycles through the proxies.

    Methods:
        get_next_proxy(): Retrieves the next available proxy from the pool. Returns None if all proxies have reached their usage limit.
    """
    def __init__(self, proxies: list, max_usage=5):
        self.proxies = proxies
        self.max_usage = max_usage
        self.usage_count = {proxy: 0 for proxy in proxies}
        self.proxy_pool = itertools.cycle(proxies)

    def get_next_proxy(self):
        """
        Retrieves the next available proxy from the pool.

        (Considering) This method cycles through the proxies, pinging each one to check if it is active,
        and returns the first active proxy that has not reached its usage limit.
        If all proxies have reached their usage limit or are inactive, it raises an Exception.

        Returns:
            str: The next available active proxy address prefixed with 'http://', or None if all proxies have been exhausted or are inactive.

        Raises:
            Exception: If all proxies have reached their usage limit or are inactive.
        """
        active_proxies = [proxy for proxy in self.proxies if self.usage_count[proxy] < self.max_usage]
        if not active_proxies:
            return None

        proxy = next(self.proxy_pool)
        while self.usage_count[proxy] >= self.max_usage:
            proxy = next(self.proxy_pool)

        self.usage_count[proxy] += 1
        if not proxy.startswith("http://") and not proxy.startswith("https://"):
            proxy = 'http://' + proxy

        return proxy

    def ping_proxy(self, proxy):
        """
        Pings a proxy to check if it is active.

        Parameters:
            proxy (str): The proxy address to ping.

        Returns:
            bool: True if the proxy is active and reachable, False otherwise.
        """
        # In future, if no another solution than ping proxy before usage example procedures in DB,
        # it is better to ping proxy here

