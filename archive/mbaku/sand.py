import asyncio, os, json, dotenv, zipfile,shutil
from sys import version
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, LLMConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter, LLMContentFilter
from numpy import number



dotenv.load_dotenv()

async def basic():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://doi.org/10.3390/microorganisms13092112")
        
        # save to md file in the current directory
        md_file = 'raw.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(result.markdown)
            print(f"Results saved to {os.path.abspath(md_file)}")
            print(result.cleaned_html)


async def ai():
    
    config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            # content_filter=PruningContentFilter(threshold_type = 'dynamic', threshold = 0.5),
            content_filter=LLMContentFilter(
                    llm_config=LLMConfig(provider="anthropic/claude-3-5-sonnet", api_token=os.getenv('ANTHROPIC_API_KEY'), base_url="https://api.anthropic.com/v1"),
                    instruction="""
                        Extract the core study in its entirety. 
                        exclude navigation, sidebar, footer, and any other non-core content.
                        advertisement. follow links to table and extract em too
                        return data based fit for bugsigdb study curation
                    """,
                    verbose=True,
                    chunk_token_threshold=2000,
                ),
            
            options={
                "ignore_images": True,
                'skip_internal_links' : True,
                'ignore_links' : True,
            } 
            
        )
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://doi.org/10.3390/microorganisms13092112", config=config)
        
        md_file = 'ai.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(result.markdown)
            print(f"Results saved to {os.path.abspath(md_file)}")            
        

async def advanced():
    
    config = CrawlerRunConfig(
        exclude_social_media_links=True,
        capture_mhtml=True, #capture mhtml
        # exclude_external_links=True, #exclude external links from the result
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold_type = 'dynamic', threshold = 0.5),
            options={ "ignore_images": True, 
                    'skip_internal_links' : True, #skip internal links inside the markdwon but allow it to be scraped.
                    'ignore_links' : True
                } 
        )
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://doi.org/10.3390/microorganisms13092112", config=config)
        

        if result:  
            # markdown
            md_file = 'advanced.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(result.markdown)
            
            # mhtml
            if result.mhtml:
                mhtml_file = 'advanced.mhtml'
                with open(mhtml_file, 'w', encoding='utf-8') as f:
                    f.write(result.mhtml)
                
    
            #links
            if result.links:
                os.makedirs('links', exist_ok=True)
            
                with open('links/external_links.json', 'w') as f: 
                    json.dump(result.links.get('external', []), f)
                    
                with open('links/internal_links.json', 'w') as f: 
                    json.dump(result.links.get('internal', []), f)
            
            # media
            if result.media:
                os.makedirs('media', exist_ok=True)
                
                with open('media/images.json', 'w') as f:
                    json.dump(result.media.get('images', []), f)
                
                with open('media/videos.json', 'w') as f:
                    json.dump(result.media.get('videos', []), f)
                
                with open('media/audios.json', 'w') as f:
                    json.dump(result.media.get('audios', []), f) 
                
        
async def downloader():
    #downloads path
    downloads_path=os.path.join(os.getcwd(), 'downloads')
    os.makedirs(downloads_path, exist_ok=True)
    
    #suplimentary path
    suplimentary_path=os.path.join(os.getcwd(), 'suplimentary')
    os.makedirs(suplimentary_path, exist_ok=True)
    
    

    browser_config = BrowserConfig(
        
        #downloadable files
        accept_downloads=True,
        downloads_path=downloads_path, 
    )
    
    config = CrawlerRunConfig(
        exclude_social_media_links=True,
        capture_mhtml=True, #capture mhtml
        # exclude_external_links=True, #exclude external links from the result
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold_type = 'dynamic', threshold = 0.5),
            options={ "ignore_images": True, 
                    'skip_internal_links' : True, #skip internal links inside the markdwon but allow it to be scraped.
                    'ignore_links' : True
                } 
        ),
        
        #javascript code to trigger file download
        js_code="""
            // Try to find and click supplementary material download links
            const suppLinks = document.querySelectorAll('a[href*="/s1"], a[href*="download"], .supplementary-material a');
            suppLinks.forEach(link => {
                if (link.href && !link.href.includes('#')) {
                    link.click();
                    console.log('Clicked supplementary material link:', link.href);
                }
            });
        """,
        wait_for='5' #wait for 5 seconds !important: this has to be a string not an integer
    
    )
    
    

    async with AsyncWebCrawler(config=browser_config) as crawler:
        
        result = await crawler.arun(url="https://doi.org/10.3390/microorganisms13092112", config=config)
        
        if result.downloaded_files:
        
            for file_path in result.downloaded_files:
                if file_path.endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(suplimentary_path)
                        
                
            
        
        """
        if result:  
            
            # markdown
            md_file = 'advanced.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(result.markdown)
            
            # mhtml
            if result.mhtml:
                mhtml_file = 'advanced.mhtml'
                with open(mhtml_file, 'w', encoding='utf-8') as f:
                    f.write(result.mhtml)
                
    
            #links
            if result.links:
                os.makedirs('links', exist_ok=True)
            
                with open('links/external_links.json', 'w') as f: 
                    json.dump(result.links.get('external', []), f)
                    
                with open('links/internal_links.json', 'w') as f: 
                    json.dump(result.links.get('internal', []), f)
            
            # media
            if result.media:
                os.makedirs('media', exist_ok=True)
                
                with open('media/images.json', 'w') as f:
                    json.dump(result.media.get('images', []), f)
                
                with open('media/videos.json', 'w') as f:
                    json.dump(result.media.get('videos', []), f)
                
                with open('media/audios.json', 'w') as f:
                    json.dump(result.media.get('audios', []), f) 
            
            #downloads
            # if result.downloaded_files:
            #     for path in result.downloaded_files:
            #         print(path)
        """

if __name__ == "__main__":
    asyncio.run(ai())