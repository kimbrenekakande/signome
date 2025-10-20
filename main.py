import  os, asyncio, json, dotenv, zipfile
from pathlib import Path
from crewai.flow.flow import Flow, listen, start
from crewai_tools import PDFSearchTool
from pydantic import BaseModel, Field

#craw4ai
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, LLMConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

from core.crew import crew

class StudyMetaData(BaseModel):
    country: str = ""

class SigState(BaseModel):
    study_url: str = ""
    study_path: str = ""
    study_title: str = " "
    study_meta: StudyMetaData = None



class sigFlow(Flow[SigState]):
    @start()
    def ask(self):
        self.state.study_url = "https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-025-04242-7"
        return self.state

    @listen(ask)
    async def scrape(self, state):
        
        # downloads path
        knowledge_path = os.path.join(os.getcwd(), "knowledge")
        os.makedirs(knowledge_path, exist_ok=True)

        # # main input area
        # core = os.path.join(os.getcwd(), "core")
        # os.makedirs(core, exist_ok=True)

        browser_config = BrowserConfig(
            # downloadable files
            accept_downloads=True,
            downloads_path=knowledge_path,
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
            result = await crawler.arun(url=state.study_url, config=config)

            if result.downloaded_files:
                for file_path in result.downloaded_files:
                    if file_path.endswith(".zip"):
                        with zipfile.ZipFile(file_path, "r") as zip_ref:
                            zip_ref.extractall(knowledge_path)

            if result:
                # markdown
                md_file = "knowledge/study.md"
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
                    state.study_path = md_file

                # mhtml
                if result.mhtml:
                    mhtml_file = "advanced.mhtml"
                    with open(mhtml_file, "w", encoding="utf-8") as f:
                        f.write(result.mhtml)

                # media
                if result.media:
                    with open("knowledge/images.json", "w") as f:
                        json.dump(result.media.get("images", []), f)

        return self.state
    
    @listen(scrape)
    def converter(self):
        know = Path('knowledge')
        study = Path('knowledge/study.md')
        
        for file in know.iterdir():
            if file.suffix == '.json':
                with open(file, 'r') as f:
                    data = json.load(f)
                    with open(study, 'a') as md:
                        md.write('## Image Description Data' + '\n\n')
                        for item in data:
                            img_desc = item['desc']
                            md.write(img_desc + '\n\n')
                print(file.name)
                
            else:
                pass
            
        
        return self.state
    
    
    @listen(converter)
    def crew_call(self):
        output = os.path.join(os.getcwd(), 'output/')
        os.makedirs(output, exist_ok=True)
        
        inputs = {'study_path': self.state.study_path}
        crew.kickoff(inputs=inputs)
        return self.state
        

if __name__ == "__main__":
    sigFlow().kickoff()
