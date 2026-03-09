

from src.chunker import split_documents
from src.embedder import load_embedding_model, embed_chunks
from src.llm import build_prompt

# check chunking
def test_chunking():


    # a fake doc
    fake_documents = [{
        "source": "test.pdf",

        #a long sentences
        "text"  : "Diabetes is a disease. " * 50 
    }]

    chunks = split_documents(fake_documents)

    # their is at least 1 chunk
    assert len(chunks) > 0



    # every chunk should have text and source
    assert "text"   in chunks[0]
    assert "source" in chunks[0]

    print(f" Chunking OK - {len(chunks)} chunks was build")


#check embedding
def test_embedding():



    model = load_embedding_model()

    fake_chunks = [{
        "source" : "test.pdf",
        "chunk_id" : 0,
        "text": "Diabetes causes skin problems."
    }]

    chunks_with_embeddings = embed_chunks(fake_chunks, model)



    # must have embedding
    assert "embedding" in chunks_with_embeddings[0]


    # embedding must be a vector
    assert len(chunks_with_embeddings[0]["embedding"]) > 0

    print(f" Embedding OK - len: {len(chunks_with_embeddings[0]['embedding'])}")



# check promt
def test_prompt_builder():


    question = "what is diabetes?"
    context  = "Diabetes is a metabolic disease."

    prompt = build_prompt(question, context)


    # prompt must have context and question
    assert question in prompt
    assert context  in prompt

    print(" Prompt Builder OK")