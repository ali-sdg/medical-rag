
def retrieve(collection, model, query, n_results = 3):
    
    #transfer question to embed
    query_embedding = model.encode([query])[0].tolist()

    #searching on chromaDB
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = n_results
    )


    # transfer results to a clean and simple list

    retrieved_chunks = []


    for i in range(len(results['documents'][0])):
        retrieved_chunks.append({
            'text': results['documents'][0][i],
            'source' : results["metadatas"][0][i]["source"],

            #distance = ho much relative
            'score' : results["distances"][0][i] 

        })


        return retrieved_chunks



def format_context(retrieved_chunks):
    
    context = ""

    for i, chunk in enumerate(retrieved_chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n"
        context += f"{chunk['text']}\n"


        context += "-" * 40 + "\n"


    return context