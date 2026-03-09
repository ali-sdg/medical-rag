import requests
import json

#local ollama addres 

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"




def build_prompt(query, context):

    prompt = f"""You are a helpful medical assistant.
Answer the question ONLY based on the context below.
If the answer is not in the context, say: "I could not find the answer in the provided documents."
Do NOT make up information.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""



    return prompt


def ask_llm(prompt):

    print(' \n thinking .....')


    response = requests.post(

        OLLAMA_URL,
        json = {
            'model' : MODEL_NAME,
            'prompt' : prompt,

            # Respond all at once, not in pieces
            'stream' : False
        }
    )



    #get answer
    result = response.json()
    answer = result["response"]




    return answer
