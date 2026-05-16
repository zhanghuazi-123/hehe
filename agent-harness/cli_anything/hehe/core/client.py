"""HTTP client for Hehe API."""

import json
import urllib.request
import urllib.error
from typing import Optional, Any


class HeheClient:
    """Low-level HTTP client for Hehe API."""

    def __init__(self, base_url: str = "http://127.0.0.1:3721", token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, method: str, path: str, body: Any = None, raw: bool = False) -> Any:
        url = f"{self.base_url}{path}"
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = resp.read().decode("utf-8")
                if raw:
                    return result
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return result
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {msg[:200]}") from None
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection failed: {e.reason}") from None

    def get(self, path: str, raw: bool = False) -> Any:
        return self._request("GET", path, raw=raw)

    def post(self, path: str, body: Any = None) -> Any:
        return self._request("POST", path, body)

    def patch(self, path: str, body: Any = None) -> Any:
        return self._request("PATCH", path, body)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)
