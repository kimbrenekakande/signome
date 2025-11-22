import os
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    api_key=os.getenv("DEEPSEEK_API_KEY")
)


#embeddings
ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
)

print(ollama_ef)