from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):

    #build chunking tool
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        separators = ['\n\n', '\n', '.', ' ']
    )



    all_chunks = []

    for doc in documents:

        chunks = splitter.split_text(doc['text'])

        source = doc["source"]
        print(f"\n file: {source}")
        print(f" chunks count :  {len(chunks)}")

        for i, chunk in enumerate(chunks):
            all_chunks.append({

                #file_name
                "source": doc["source"],
                
                # num of chunk
                "chunk_id": i,
                
                #text of chunk
                "text": chunk
            })

    return all_chunks

        