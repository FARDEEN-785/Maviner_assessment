import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question, context):
    prompt = f"""
You are a telecom standards assistant for 3GPP TS 23.501.

Answer the user's question using only the provided 3GPP evidence.

RULES:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the evidence does not support the answer, say exactly:
   "I don't have enough information for this question!."
4. Keep the answer concise and technically accurate.
5. Every factual statement must include its source page.
6. If multiple pieces of evidence are used, check each relevant page.
7. Do not mention information that is not present in the evidence.

OUTPUT FORMAT:

Answer:
<your concise answer>

Sources:
- 3GPP TS 23.501, Page <page number>

QUESTION:
{question}

3GPP EVIDENCE:
{context}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text