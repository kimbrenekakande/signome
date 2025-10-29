import chromadb, uuid
from pathlib import Path
from pprint import pprint
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter


client = chromadb.Client()
collection = client.get_or_create_collection(name="documents")


ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
)


doc_path = Path("study.md").read_text()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2024,
    chunk_overlap=256,
)

chunks = text_splitter.split_text(doc_path)


def embbedder(chuck):
    embedd = ollama_ef([chunk])
    return embedd[0][0]


print(f"============  Generating embeddings  ============ \n")

for chunk in chunks:
    # Generate embedding for the chunk
    embedding = ollama_ef([chunk])[0]
    print(embedding)
    
    # Add document with its embedding to the collection
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[chunk],
        embeddings=[embedding]
    )


# pprint(collection.peek())



# collection = chroma_client.get_or_create_collection(name="documents")
# collection.add(
#     documents=[doc_path], 
#     ids=["study"]
# )

# results = collection.query(
#     query_texts=['define sonder'],
#     n_results=1,
#     where_document={"$contains": "purpose"}
# )

# pprint(embeddings)