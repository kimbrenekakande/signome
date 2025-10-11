from crewai import LLM


llm = LLM(
    model="groq/moonshotai/kimi-k2-instruct-0905",
    temperature=0.7,
)