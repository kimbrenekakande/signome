# from crewai_tools import BaseTool
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, LLMConfig, PruningContentFilter, LLMExtractionStrategy, extraction_strategy


async def prunned():
    url = "https://www.mdpi.com/2076-2607/13/9/2112"
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config = CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter)
            )
        )
        # Save entire article content in Markdown
        with open("../output/mdpi_article_prune.md", "w") as f:
            f.write(result.markdown)



asyncio.run(prunned())








# async def main():
#     url = "https://www.mdpi.com/2076-2607/13/9/2112"
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(url=url)
#         # Save entire article content in Markdown
#         with open("../output/mdpi_article.md", "w") as f:
#             f.write(result.markdown)




# async def ai():
#     strategy = LLMExtractionStrategy(
#         llm_config=LLMConfig( provider="deepseek/deepseek-chat", api_token="env:DEEPSEEK_API_KEY"),
#         instruction='This is a microbiome study. extract the entirety of it without including other areas of the page like page navigation, interaction links, footer , action buttons etc. just the complete study',
#         schema="{title:string, body : string}",
#         extra_args={'temperature' : 0.7},
#         verbose=True
        
#     )
#     url = "https://www.mdpi.com/2076-2607/13/9/2112"
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url=url,
#             config = CrawlerRunConfig(extraction_strategy=strategy)
#         )
#         # Save entire article content in Markdown
#         with open("../output/mdpi_article_ai.json", "w") as f:
#             f.write(result.json())

# async def aimd():
#     strategy = LLMExtractionStrategy(
#         llm_config=LLMConfig( provider="gemini/gemini-2.5-flash", api_token="env:GEMINI_API_KEY"),
#         instruction='Please extract the entire microbiome study text content only. Exclude all other parts of the page such as page navigation, interaction links, footer, action buttons, etc.',
#         extra_args={'temperature' : 0.7},
#         verbose=True
        
#     )
#     url = "https://www.mdpi.com/2076-2607/13/9/2112"
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url=url,
#             config = CrawlerRunConfig(extraction_strategy=strategy)
#         )
#         # Save entire article content in Markdown
#         with open("../output/mdpi_ai.md", "w") as f:
#             f.write(result.markdown)

