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
    api_key="sk-d6fa04f2a09049c99b13c58b720dc5b6",
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
    