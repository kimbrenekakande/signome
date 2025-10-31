from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction

# Initialize DeepSeek model
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
)


# Initialize Groq model
model = ChatGroq(
    model="deepseek-chat",
    temperature=0,
)


# Initialize Ollama embeddings
ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
)
