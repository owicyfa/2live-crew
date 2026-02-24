import os
from dotenv import load_dotenv

# Load your API keys from .env
load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_KEY    = os.getenv("GROQ_API_KEY")

if not GOOGLE_KEY or not GROQ_KEY:
    print("Error: One or both API keys not found in .env")
    exit(1)

print("Keys loaded successfully.\n")

from crewai import LLM
from langchain_groq import ChatGroq

# ────────────────────────────────────────────────
# Prepare both models (using the working names from your previous test)
# ────────────────────────────────────────────────

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GOOGLE_KEY,
    temperature=0.1,           # very low → more factual, less creative
    max_tokens=120,
)

groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    temperature=0.1,
    max_tokens=120,
)

# ────────────────────────────────────────────────
# The two factual questions (same as you asked Grok)
# ────────────────────────────────────────────────

questions = [
    "What is the capital of Nigeria 🇳🇬",
    "Which country is Donald Trump the president of right now? Please include the current year or term information if known."
]

# ────────────────────────────────────────────────
# Ask both models and collect answers
# ────────────────────────────────────────────────

print("═" * 70)
print("Running factual accuracy test (February 2026)")
print("═" * 70 + "\n")

for q in questions:
    print(f"Question: {q}\n")

    # Gemini via CrewAI
    try:
        gemini_answer = gemini_llm.call(q).strip()
        print("Gemini 2.5-flash answer:")
        print(gemini_answer)
    except Exception as e:
        print("Gemini error:", str(e))
    
    print("-" * 50)

    # Groq
    try:
        groq_response = groq_llm.invoke(q)
        groq_answer = groq_response.content.strip()
        print("Groq (llama-3.3-70b-versatile) answer:")
        print(groq_answer)
    except Exception as e:
        print("Groq error:", str(e))
    
    print("=" * 70 + "\n")
