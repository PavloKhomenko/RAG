import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

def generate_response(query, context_chunks):
    prompt = f"Answer the question: {query}\n\nBased on the following:\n\n{context_chunks}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with deep knowledge in AI/ML."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content