from browser_use import Agent
from browser_use.llm import ChatDeepSeek
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()

async def main():
    llm = ChatDeepSeek(base_url="https://api.deepseek.com/v1", model="deepseek/deepseek-chat", api_key=os.environ["DEEPSEEK_API_KEY"])
    task = """
        Go to https://www.mdpi.com/2076-2607/13/9/2112
        analyze the only the images and the tables in the study and extract the following information thats important in the curation of the study for BugSigDB database entries of this study
        make sure they to neglet inportant experiments in the study
        """
    agent = Agent(task=task, llm=llm, verbose=True)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())