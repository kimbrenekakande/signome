# from crewai.tools import BaseTool
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, LLMConfig, PruningContentFilter, LLMExtractionStrategy, extraction_strategy
import os

# async def prunned():
#     url = "https://www.mdpi.com/2076-2607/13/9/2112"
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url=url,
#             config = CrawlerRunConfig(
#                 markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter)
#             )
#         )
#         # Save entire article content in Markdown
#         with open("./mdpi_article_prune.md", "w") as f:
#             f.write(result.markdown)


# # async def main():
# #     url = "https://www.mdpi.com/2076-2607/13/9/2112"
# #     async with AsyncWebCrawler() as crawler:
# #         result = await crawler.arun(url=url)
# #         # Save entire article content in Markdown
# #         with open("../output/mdpi_article.md", "w") as f:
# #             f.write(result.markdown)


