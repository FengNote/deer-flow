import json
import os
from typing import Dict, List, Optional

import aiohttp
import requests


class SerperSearchAPIWrapper:
    def __init__(self, serper_api_key: Optional[str] = None):
        self.serper_api_key = serper_api_key or os.getenv("SERPER_API_KEY")
        if not self.serper_api_key:
            raise ValueError("SERPER_API_KEY environment variable is required")

    def raw_results(
        self,
        query: str,
        max_results: Optional[int] = 10,
    ) -> Dict:
        payload = json.dumps({"q": query, "num": max_results})
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            "https://google.serper.dev/search",
            data=payload,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    async def raw_results_async(
        self,
        query: str,
        max_results: Optional[int] = 10,
    ) -> Dict:
        async def fetch() -> str:
            payload = json.dumps({"q": query, "num": max_results})
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://google.serper.dev/search",
                    data=payload,
                    headers=headers
                ) as res:
                    if res.status == 200:
                        data = await res.text()
                        return data
                    else:
                        raise Exception(f"Error {res.status}: {res.reason}")

        results_json_str = await fetch()
        return json.loads(results_json_str)

    def clean_results(self, raw_results: Dict) -> List[Dict]:
        clean_results = []
        
        organic_results = raw_results.get("organic", [])
        for result in organic_results:
            clean_result = {
                "type": "page",
                "title": result.get("title", ""),
                "url": result.get("link", ""),
                "content": result.get("snippet", ""),
                "score": 1.0,
            }
            clean_results.append(clean_result)
        
        return clean_results


if __name__ == "__main__":
    wrapper = SerperSearchAPIWrapper()
    results = wrapper.raw_results("apple inc")
    print(json.dumps(results, indent=2, ensure_ascii=False))
