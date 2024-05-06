import time
import requests as rq
from requests import Response, HTTPError, Timeout

NPOINT_API = "https://api.npoint.io/78eff6ee825163d0043a"

class BlogData:

    def __init__(self) -> None:
        self._refresh_time = time.time() + 60
        self.ok, self.data = self._get_blog_data()


    def check_for_refresh(self):
        print(f"Refresh time is: {self._refresh_time}")
        print(f"Current time is: {time.time()}")
        if not self.ok:
            print("Data refreshed.")
            self.ok, self.data = self._get_blog_data()
            self._refresh_time = time.time() + 60

        if time.time() >= self._refresh_time:
            print("Data refreshed.")
            self.ok, self.data = self._get_blog_data()
            self._refresh_time = time.time() + 60

    def _verify_connection(self, res: Response):
        try:
            res.raise_for_status()
            return True, None
        except (HTTPError, Timeout) as e:
            return False, e

    def _get_blog_data(self):
        res = rq.get(url=NPOINT_API, timeout=30)
        ok, error = self._verify_connection(res)
        if ok:
            return ok, res.json()
        return ok, error