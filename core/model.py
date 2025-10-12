from crewai import LLM


# llm = LLM(
#     model="groq/llama-3.3-70b-versatile",
#     temperature=0.7,
# )


llm = LLM(
    provider="deepseek",
    model="deepseek/deepseek-chat",
    api_key="sk-d6fa04f2a09049c99b13c58b720dc5b6",
    temperature=0.7,
)