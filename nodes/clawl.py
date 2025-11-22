
import os
import zipfile
import json

#craw4ai
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

async def scrape(state):
        
    # downloads path
    core_path = os.path.join(os.getcwd(), "core")
    os.makedirs(core_path, exist_ok=True)

    browser_config = BrowserConfig(
        # downloadable files
        accept_downloads=True,
        downloads_path=core_path,
    )

    config = CrawlerRunConfig(
        exclude_social_media_links=True,
        capture_mhtml=True,  # capture mhtml
        # exclude_external_links=True, #exclude external links from the result
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold_type="dynamic", threshold=0.5
            ),
            options={
                "ignore_images": True,
                "skip_internal_links": True,  # skip internal links inside the markdwon but allow it to be scraped.
                "ignore_links": True,
            },
        ),
        # javascript code to trigger file download
        js_code="""
            // Try to find and click supplementary material download links
            const suppLinks = document.querySelectorAll('a[href*="/s1"], a[href*="download"], .supplementary-material a');
            suppLinks.forEach(link => {
                if (link.href && !link.href.includes('#')) {
                    link.click();
                    console.log('Clickedl supplementary material link:', link.href);
                }
            });
        """,
        wait_for="5",  # wait for 5 seconds !important: this has to be a string not an integer
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=state['study_url'], config=config)

        if result.downloaded_files:
            for file_path in result.downloaded_files:
                if file_path.endswith(".zip"):
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(core_path)

        if result:
            # markdown
            md_file = "core/study.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(result.markdown)
                state['study_path'] = md_file

            # media
            if result.media:
                with open("core/images.json", "w") as f:
                    json.dump(result.media.get("images", []), f)

    return state
