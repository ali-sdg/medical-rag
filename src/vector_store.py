
import chromadb


def create_vector_store(collection_name="medical_docs"):

    # build client ChromaDB - datas is stored on disk
    client = chromadb.PersistentClient(path="./chroma_db")


    # build or open a collection
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={'description': "Medical RAG documents"}
    )


    return collection


def store_chunks(collection, chunks_with_embeddings):


    # get ready datas to ChromaDB
    
    #every chunks shuld hace uniq ID
    ids = []

    # number vectores 
    embeddings= []

    #original texts
    documents = []

    # additional infos
    metadatas= []

    for chunk in chunks_with_embeddings:

        # Create a unique ID from the file name and chunk number
        unique_id = f"{chunk['source']}_chunk_{chunk['chunk_id']}"

        ids.append(unique_id)


        # numpy to list
        embeddings.append(chunk["embedding"].tolist())
        documents.append(chunk["text"])
        metadatas.append({"source": chunk["source"]})


    # Store everything in one place in ChromaDB

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


    print(f"all of docs inside of DB: {collection.count()}")


def search_similar(collection, model, query, n_results=3):


    # transform question to embed
    query_embedding = model.encode([query])[0].tolist()

    # search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )



    return results

