import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from langchain_groq import ChatGroq
from ddgs import DDGS
from typing import Optional

load_dotenv()

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GOOGLE_KEY or not GROQ_KEY:
    print("Error: Missing API keys in .env")
    exit(1)

print("API keys loaded OK.\n")

# ────────────────────────────────────────────────
# Custom DDGS Search Tool using BaseTool subclass
# ────────────────────────────────────────────────
class DDGSSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = (
        "Search the web using DuckDuckGo (free, no key needed). "
        "Use this for current events, recent news, facts after 2024, "
        "or anything your knowledge might miss. Returns list of title + snippet + url."
    )

    def _run(self, query: str) -> str:
        """Run DuckDuckGo search and format results."""
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=5)]
            if not results:
                return "No results found."
            formatted = []
            for r in results:
                formatted.append(
                    f"Title: {r.get('title', 'N/A')}\n"
                    f"URL: {r.get('href', 'N/A')}\n"
                    f"Snippet: {r.get('body', 'N/A')[:300]}...\n"
                )
            return "\n".join(formatted) if formatted else "No useful results."
        except Exception as e:
            return f"Search error: {str(e)}"

# Instantiate the tool
search_tool = DDGSSearchTool()

# ────────────────────────────────────────────────
# LLMs (your working config)
# ────────────────────────────────────────────────
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GOOGLE_KEY,
    temperature=0.2,
)

groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_KEY,
    temperature=0.2,
)

# ────────────────────────────────────────────────
# Test Agent that uses the DDGS tool
# ────────────────────────────────────────────────
research_agent = Agent(
    role="Current Events Researcher",
    goal="Answer factual questions using only up-to-date web information from 2025–2026.",
    backstory=(
        "You are a real-time fact checker in February 2026. "
        "NEVER use outdated internal knowledge. ALWAYS use the DuckDuckGo Search tool first. "
        "Summarize only recent, credible results. Cite sources."
    ),
    llm=gemini_llm,  # Primary = Gemini
    tools=[search_tool],
    verbose=True,      # Fixed to boolean
    allow_delegation=False,
)

# ────────────────────────────────────────────────
# Tasks for your two questions
# ────────────────────────────────────────────────
questions = [
    "What is the capital of Nigeria 🇳🇬",
    "Which country is Donald Trump the president of right now? Include term and year info."
]

tasks = []
for q in questions:
    task = Task(
        description=f"Answer this question using ONLY current web information: {q}",
        expected_output="A short, factual answer with sources cited. If no recent data, say so.",
        agent=research_agent,
    )
    tasks.append(task)

# ────────────────────────────────────────────────
# Run the mini-crew
# ────────────────────────────────────────────────
print("Starting DDGS + LLM test...\n")
crew = Crew(
    agents=[research_agent],
    tasks=tasks,
    verbose=True,      # Fixed to boolean (was 2 → error)
    process="sequential",
)

result = crew.kickoff()
print("\n" + "="*70)
print("FINAL RESULTS:")
print(result)
print("="*70)
