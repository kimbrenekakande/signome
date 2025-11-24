from pprint import pprint
import chromadb , uuid
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings



def embbed(state):  
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="documents")

    doc_path = Path("core/study.md").read_text()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(doc_path)

    #generate embeddings
    embeddingsModel = OllamaEmbeddings(model="nomic-embed-text:latest")


    print("============  Generating embeddings  ============ \n")

    # Generate embedding for the chunk
    embeddings = embeddingsModel.embed_documents(chunks)    

    # Add embeddings to the chroma db
    collection.add(ids = [str(uuid.uuid4()) for _ in range(len(chunks))], documents=chunks)

    # results=collection.query(
    #     query_texts = [
    #         "how many experiments were done",
    #     ],
    #     n_results = 3
    # )
    
    return state
