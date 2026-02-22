import os
from dotenv import load_dotenv

load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))

from crewai import LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

print("\n=== Test 1: CrewAI LLM wrapper with updated Gemini (gemini-2.5-flash) ===")
try:
    gemini_llm = LLM(
        model="gemini/gemini-2.5-flash",  # Updated to current fast model (or try gemini/gemini-flash-latest)
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )
    response = gemini_llm.call("Respond with exactly: Gemini 2.5 connection successful!")
    print("Gemini response:", response.strip())
except Exception as e:
    print("Gemini (CrewAI) error:", str(e))

print("\n=== Test 2: Direct LangChain Gemini (gemini-2.5-flash) ===")
try:
    gemini_direct = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Current stable/fast model
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )
    direct_resp = gemini_direct.invoke("Respond with exactly: Direct Gemini 2.5 OK!")
    print("Direct Gemini response:", direct_resp.content.strip())
except Exception as e:
    print("Direct Gemini error:", str(e))

print("\n=== Test 3: Groq fallback with updated model (llama-3.3-70b-versatile) ===")
try:
    groq_llm = ChatGroq(
        model="llama-3.3-70b-versatile",  # Current replacement for 3.1-70b
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )
    groq_resp = groq_llm.invoke("Respond with exactly: Groq 3.3 is ready!")
    print("Groq response:", groq_resp.content.strip())
except Exception as e:
    print("Groq error:", str(e))
