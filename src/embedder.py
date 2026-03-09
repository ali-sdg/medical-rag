from sentence_transformers import SentenceTransformer


# model name : specialy for medical text

def load_embedding_model():

    MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
    model = SentenceTransformer(MODEL_NAME)

    return model


def embed_chunks(chunks, model):
    
    # separate texts
    texts = [chunk['text'] for chunk in chunks]

    #  giving all text 
    embeddings = model.encode(
        texts,

        #show progres bar
        show_progress_bar = True,

        batch_size=32
    )

    # add embedings to every chunks
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i]


    return chunks

