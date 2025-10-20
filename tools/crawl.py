from typing import Type
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter
from crewai.tools import BaseTool
from pydantic import BaseModel, Field



class crawl4aiInput(BaseModel):
    url: str = Field(..., description="URL to crawl")



class crawl4aiTool(BaseTool):
    name: str = "crawl4ai"
    description: str = "Crawl a URL on a microbiome study and return the the study in Markdown format"
    args_schema: Type[BaseModel] = crawl4aiInput
    

    def _run(self, url: str) -> str:
        """Synchronous run method required by BaseTool."""
        return asyncio.run(self._async_run(url))
    
    async def _async_run(self, url: str) -> str:
        """Async implementation of the crawling logic."""
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                config = CrawlerRunConfig(
                    markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter)
                )
            )
            # # Save entire article content in Markdown
            # with open("./output/raw.md", "w") as f:
            #     f.write(result.markdown)


            return result.markdown


