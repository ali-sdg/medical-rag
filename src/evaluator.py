

from src.llm import ask_llm


def check_faithfulness(question, answer, context):



    prompt = f"""You are an evaluator. 
Check if the ANSWER is based ONLY on the CONTEXT provided.

CONTEXT:
{context}

QUESTION: {question}
ANSWER: {answer}

Reply with ONLY a number between 0 and 1:
- 1.0 = answer is completely based on context
- 0.5 = answer is partially based on context  
- 0.0 = answer is NOT based on context at all

Reply with ONLY the number, nothing else."""

    score_text = ask_llm(prompt).strip()


    try:
        score = float(score_text[:3])
        score = max(0.0, min(1.0, score))
        
    except:
        score = 0.5

    return score


def check_relevancy(question, answer):



    prompt = f"""You are an evaluator.
Check if the ANSWER is relevant to the QUESTION.

QUESTION: {question}
ANSWER: {answer}

Reply with ONLY a number between 0 and 1:
- 1.0 = answer is completely relevant to the question
- 0.5 = answer is partially relevant
- 0.0 = answer is NOT relevant at all

Reply with ONLY the number, nothing else."""

    score_text = ask_llm(prompt).strip()

    try:
        score = float(score_text[:3])
        score = max(0.0, min(1.0, score))
    except:
        score = 0.5

    return score


def evaluate_rag(questions, answers, contexts):


    faithfulness_scores = []
    relevancy_scores    = []

    for i in range(len(questions)):
       


        context_text = "\n".join(contexts[i])

        f_score = check_faithfulness(questions[i], answers[i], context_text)
        r_score = check_relevancy(questions[i], answers[i])

        faithfulness_scores.append(f_score)
        relevancy_scores.append(r_score)


        print(f"  Faithfulness : {f_score:.2f}")
        print(f"  Relevancy    : {r_score:.2f}")



    # average
    avg_faithfulness = sum(faithfulness_scores) / len(faithfulness_scores)
    avg_relevancy    = sum(relevancy_scores)    / len(relevancy_scores)

    return {
        "faithfulness"    : avg_faithfulness,
        "answer_relevancy": avg_relevancy
    }