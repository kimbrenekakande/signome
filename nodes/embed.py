from pprint import pprint
import chromadb 
import uuid
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ollama_ef



def embbed(state):
    
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="documents")



    doc_path = Path("study.md").read_text()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2024,
        chunk_overlap=256,
    )

    chunks = text_splitter.split_text(doc_path)


    def embbedder(chuck):
        embedd = ollama_ef([chunk])
        return embedd[0][0]


    print("============  Generating embeddings  ============ \n")

    for chunk in chunks:
        # Generate embedding for the chunk

        # Add document with its embedding to the collection
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            # embeddings=[embedding]
        )


    results=collection.query(
        query_texts = [
            "what is sonder",
            'what does sonder represent'
        ],
        n_results = 5
    )


    for i, query_res in enumerate(results['documents']): 
        print(i)
        pprint(query_res)
        print('\n')
    
    return state
