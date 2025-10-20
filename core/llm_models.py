from crewai import LLM
from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()

groq = LLM(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True
)

deepseek = LLM(
    provider="deepseek",
    model="deepseek/deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

gemini = LLM(
    model="gemini/gemini-2.5-pro",
    api_key=os.getenv("GEMINI_API_KEY")
)

open = LLM(
    model="openrouter/moonshotai/kimi-k2-instruct-0905",
    api_key=os.getenv("MOONSHOT_API_KEY")
)

claude = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",  # This is the correct model name for Claude 3.5 Sonnet
    api_key=os.getenv("ANTHROPIC_API_KEY"),  # Make sure to use ANTHROPIC_API_KEY in your .env file
    temperature=0.7
)