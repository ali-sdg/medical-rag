
from src.document_loader import load_all_pdfs
from src.chunker import split_documents
from src.embedder import load_embedding_model, embed_chunks
from src.vector_store import create_vector_store, store_chunks
from src.retriever import retrieve, format_context
from src.llm import build_prompt, ask_llm
from src.evaluator import evaluate_rag




# geting ready pipeline
print("geting readypipeline...")
documents = load_all_pdfs("data")
chunks= split_documents(documents)
model = load_embedding_model()
chunks_with_embeddings = embed_chunks(chunks, model)
collection = create_vector_store()

store_chunks(collection, chunks_with_embeddings)

# test questions

test_questions = [
    "what are skin problems in diabetes?",
    "what is the prevalence of skin disease in diabetic patients?",
    "what medications cause skin problems in diabetes?"
]

# Collecting Answers
questions = []
answers   = []
contexts  = []

print("\n Getting answers...")

for question in test_questions:
    retrieved = retrieve(collection, model, question, n_results=3)
    context_text = format_context(retrieved)
    prompt= build_prompt(question, context_text)
    answer = ask_llm(prompt)

    questions.append(question)
    answers.append(answer)
    contexts.append([chunk["text"] for chunk in retrieved])

    print(f"✅ {question[:45]}...")

# evaluate

print("\n" + "="*50)
results = evaluate_rag(questions, answers, contexts)

print("\n" + "="*50)
print(f"  Faithfulness : {results['faithfulness']:.2f}")
print(f"  Relevancy: {results['answer_relevancy']:.2f}")
