from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction


model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)


#embeddings
ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
)

print(ollama_ef)