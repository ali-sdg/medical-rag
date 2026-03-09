
#document_laoder.py
# from src.document_loader import load_all_pdfs



# # read all pdf files on data folder
# documents = load_all_pdfs("data")

# # showing result
# for doc in documents:
#     print("\n" + "="*50)
#     print(f" file: {doc['source']}")
#     print(f" character count:  {len(doc['text'])}")
#     print(f" first 200 char: \n{doc['text'][:200]}")






# # chunker.py
# from src.document_loader import load_all_pdfs
# from src.chunker import split_documents

# # first step: reading pdfs
# print("reading PDFs ...")
# documents = load_all_pdfs("data")

# # step2: chunking
# print("\n  chunking..")
# chunks = split_documents(documents)

# # showing results
# print("\n" + "="*50)
# print(f"all of chuns:  {len(chunks)}")
# print("\n first 3chunks")

# for chunk in chunks[:3]:
#     print(f"\n chunk num: {chunk['chunk_id']}")
#     print(f"from {chunk['source']} file" )
#     print(f" text:\n{chunk['text']}")







# embedding.py

# from src.document_loader import load_all_pdfs
# from src.chunker import split_documents
# from src.embedder import load_embedding_model, embed_chunks


# # step1: reading pdf file
# print("reading pdf files..")
# documents = load_all_pdfs("data")

# # chunkig step2
# print("\n chunking ...")
# chunks = split_documents(documents)

# # 3 Embedding
# model = load_embedding_model()
# chunks_with_embeddings = embed_chunks(chunks, model)

# # showing result
# print("\n" + "="*50)
# first_chunk = chunks_with_embeddings[0]
# print(f"text of first chunk \n{first_chunk['text'][:100]}...")
# print(f"\n len ofEmbedding: {len(first_chunk['embedding'])}")
# print(f"first 5 Embedding: {first_chunk['embedding'][:5]}")








# vector_store.py

# from src.document_loader import load_all_pdfs
# from src.chunker import split_documents
# from src.embedder import load_embedding_model, embed_chunks
# from src.vector_store import create_vector_store, store_chunks, search_similar

# # 1
# print("readingPDF s..")
# documents = load_all_pdfs("data")

# # 2 Chunking
# print("chunking..")
# chunks = split_documents(documents)

# #3 Embedding
# model = load_embedding_model()
# chunks_with_embeddings = embed_chunks(chunks, model)

# # 4 store at vector Store
# collection = create_vector_store()
# store_chunks(collection, chunks_with_embeddings)

# # 5 searching test

# print("\n" + "="*50)
# results = search_similar(
#     collection,
#     model,
#     query="what are skin problems in diabetes?",
#     n_results=2
# )

# print("\n result of searching")
# for i, doc in enumerate(results["documents"][0]):
#     print(f"\n result {i+1} ")
#     print(f"fils {results['metadatas'][0][i]['source']}")
#     print(f"texts \n {doc[:200]}")






#retriever.py


# from src.document_loader import load_all_pdfs
# from src.chunker import split_documents
# from src.embedder import load_embedding_model, embed_chunks
# from src.vector_store import create_vector_store, store_chunks
# from src.retriever import retrieve, format_context

# # get ready evrything from 1to 4
# print(" reading PDF ..")
# documents = load_all_pdfs("data")

# print(" chunking...")
# chunks = split_documents(documents)

# print(" embedding...")
# model = load_embedding_model()
# chunks_with_embeddings = embed_chunks(chunks, model)

# print("  vector Store...")
# collection = create_vector_store()
# store_chunks(collection, chunks_with_embeddings)

# # 5 Retriever
# print("\n" + "="*50)
# query = "what are skin problems in diabetes?"

# retrieved = retrieve(collection, model, query, n_results=3)
# context   = format_context(retrieved)

# print(f" question : {query}")
# print(f"\n  retrieved texts: \n")
# print(context)
# print(f" relevance score of each piece:")
# for chunk in retrieved:
#     print(f"  - {chunk['source']} → score: {chunk['score']:.4f}")





#llm.py


# test_loader.py

from src.document_loader import load_all_pdfs
from src.chunker import split_documents
from src.embedder import load_embedding_model, embed_chunks
from src.vector_store import create_vector_store, store_chunks
from src.retriever import retrieve, format_context
from src.llm import build_prompt, ask_llm

# 1 to 4
print("reading PDF ...")
documents = load_all_pdfs("data")

print(" Chunking...")
chunks = split_documents(documents)

print("Embedding...")
model = load_embedding_model()
chunks_with_embeddings = embed_chunks(chunks, model)

print(" Vector Store...")
collection = create_vector_store()
store_chunks(collection, chunks_with_embeddings)

#5 Retriever
query = "what are skin problems in diabetes?"
retrieved = retrieve(collection, model, query, n_results=3)
context= format_context(retrieved)

# 6 Prompt + LLM
print("\n" + "="*50)
print(f" question: {query}")

prompt = build_prompt(query, context)
answer = ask_llm(prompt)

print(f"\n anwser LLM:\n{answer}")