from fastapi import FastAPI
from pydantic import BaseModel

from src.document_loader import load_all_pdfs
from src.chunker import split_documents
from src.embedder import load_embedding_model, embed_chunks
from src.vector_store import create_vector_store, store_chunks
from src.retriever import retrieve, format_context
from src.llm import build_prompt, ask_llm



# building fast api application
app = FastAPI(
    title = 'Medical RAG API',
    description = "Questions and answers from medical articles"


)



collecttion = None
model = None




# This function is executed once when the API is start
@app.on_event("startup")

def startup():
    global collection, model

    print('Launching.....')

    #load everything
    documents = load_all_pdfs("data")
    chunks = split_documents(documents)
    model = load_embedding_model()
    chunks_with_embeddings = embed_chunks(chunks, model)
    collection= create_vector_store()
    
    store_chunks(collection, chunks_with_embeddings)

    print(" api is ready")




# client question
class QuestionRequest(BaseModel):

    #question
    question: str

    ## How many chunks to look for, top-k
    n_results: int = 3



#model  answer
class AnswerResponse(BaseModel):

    #original question
    question: str

    # LLM Answer
    answer  : str

    #sources that answered
    sources : list




#priginal endpoint
@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    
    # s1: finding related texts
    retrieved = retrieve(collection, model, request.question, request.n_results)
    context   = format_context(retrieved)


    # s2: building prompt and getting answes
    prompt = build_prompt(request.question, context)
    answer = ask_llm(prompt)

    # gathering sorces
    sources = list(set([chunk["source"] for chunk in retrieved]))

    return AnswerResponse(
        question=request.question,
        answer=answer,
        sources=sources
    )




# simple endpoint for checking api 
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Medical RAG API is running ....."}