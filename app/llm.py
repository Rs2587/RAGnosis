import ollama


def generate_answer(question, context):

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the DOCUMENT CONTEXT below.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Instructions:
- If the answer exists in the document context, answer it directly.
- Do not say that the answer is missing if the information is present.
- Do not use outside knowledge.
- Do not invent information.
- Keep the answer clear and concise.
- If the answer truly does not exist in the context, say:
  I could not find the answer in the provided document.

ANSWER:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"].strip()