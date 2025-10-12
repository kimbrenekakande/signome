from crewai_tools import BaseTool
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    url = "https://www.mdpi.com/2076-2607/13/9/2112"
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        # Save entire article content in Markdown
        with open("mdpi_article.md", "w") as f:
            f.write(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
