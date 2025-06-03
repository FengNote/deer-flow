import json
from typing import Dict, List, Optional, Tuple, Union

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field

from src.tools.serper_search.serper_search_api_wrapper import SerperSearchAPIWrapper


class SerperSearchResults(BaseTool):
    name: str = "serper_search"
    description: str = (
        "A wrapper around Serper Search API. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    max_results: int = Field(default=10)
    api_wrapper: SerperSearchAPIWrapper = Field(default_factory=SerperSearchAPIWrapper)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[Union[List[Dict[str, str]], str], Dict]:
        try:
            raw_results = self.api_wrapper.raw_results(query, self.max_results)
        except Exception as e:
            return repr(e), {}
        cleaned_results = self.api_wrapper.clean_results(raw_results)
        print("sync", json.dumps(cleaned_results, indent=2, ensure_ascii=False))
        return cleaned_results, raw_results

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Tuple[Union[List[Dict[str, str]], str], Dict]:
        try:
            raw_results = await self.api_wrapper.raw_results_async(query, self.max_results)
        except Exception as e:
            return repr(e), {}
        cleaned_results = self.api_wrapper.clean_results(raw_results)
        print("async", json.dumps(cleaned_results, indent=2, ensure_ascii=False))
        return cleaned_results, raw_results
