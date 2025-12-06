"""
Multi-agent customer-support + product-search chatbot
----------------------------------------------------

Dependencies (tested 2025-06-12):

    pip install -U \
        langchain-core langchain-community langgraph \
        langchain-groq langgraph-supervisor \
        langchain-huggingface langchain-chroma

The script creates:
    • product_agent   – answers catalog questions via a Chroma vector store
    • complaints_agent – handles refunds / returns / escalations
    • supervisor (LLM) – decides which agent should respond
State & continuity:
    • in_memory_store   – optional long-term store
    • checkpointer      – thread-level checkpoint shared by all agents
"""
from fastapi import FastAPI
from pydantic import BaseModel
import os, json, uuid
from datetime import datetime
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from typing_extensions import TypedDict

# ── LangChain / LangGraph core ──────────────────────────────────────────
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langgraph.store.memory import InMemoryStore
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver

# ── LLM & Embeddings ────────────────────────────────────────────────────
from langchain_chroma import Chroma                              # new import
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings # new import

# ════════════════════════════════════════════════════════════════════════
# Initialisation
# ════════════════════════════════════════════════════════════════════════
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embedding_model,
    collection_name="product_titles",
)

# Shared memory objects
checkpointer = InMemorySaver()
in_memory_store = InMemoryStore()

# ════════════════════════════════════════════════════════════════════════
# Tools
# ════════════════════════════════════════════════════════════════════════
@tool("product_details", parse_docstring=True)
def product_details(query: str, k: int = 10) -> str:
    """
    Retrieve product titles similar to the search query.

    Args:
        query (str): Search phrase such as `"gaming laptop"`.
        k (int, optional): Number of results to return. Defaults to `10`.

    Returns:
        str: A newline-separated list of product titles with categories.
    """
    if not query.strip():
        raise ValueError("Query must be a non-empty string")

    try:
        k_int = int(k)
        k_int = k_int if k_int > 0 else 10
    except Exception:
        k_int = 10

    docs: List[Document] = vector_store.similarity_search(query, k=k_int)
    if not docs:
        return "No matching products found."

    return "\n".join(
        f"{i+1}. {d.page_content} (Category: {d.metadata.get('category')})"
        for i, d in enumerate(docs)
    )


@tool("policy", parse_docstring=True)
def policy() -> str:
    """
    Return the company’s refund / return policy text.

    Returns:
        str: Full policy document contents.
    """
    with open("policy.txt", encoding="utf-8") as f:
        return f.read()


@tool("escalation", parse_docstring=True)
def escalation() -> str:
    """
    Escalate the customer’s issue to a human agent.

    Returns:
        str: Confirmation message that escalation has been logged.
    """
    return (
        "Your request has been escalated. "
        "A dedicated specialist will contact you within 24 hours."
    )

# ════════════════════════════════════════════════════════════════════════
# Worker agents
# ════════════════════════════════════════════════════════════════════════
complaints_agent = create_react_agent(
    model=llm.bind_tools([policy, escalation]),
    name="complaints_agent",
    prompt=(
        "You are **Complaints Agent**.\n"
        "• Handle queries involving refunds, returns, replacements, warranties, or complaints.\n"
        "• Use `policy` to quote exact policy text when needed.\n"
        "• Use `escalation` if the user requests a human or their case is exceptional.\n"
        "Respond politely and concisely."
    ),
    tools=[policy, escalation],
    store=in_memory_store,
)

product_agent = create_react_agent(
    model=llm.bind_tools([product_details]),
    name="product_agent",
    prompt=(
        "You are **Product Search Agent**.\n"
        "• Help users locate products or compare items.\n"
        "• Always call `product_details` to fetch catalogue answers.\n"
        "• If the query is unrelated to products, pass control back."
    ),
    tools=[product_details],
    store=in_memory_store,
)
# custom_agent = create_react_agent(
#     model=llm,
#     name="custom_agent",
#     prompt=(
        
# )

# ════════════════════════════════════════════════════════════════════════
# Supervisor
# ════════════════════════════════════════════════════════════════════════
supervisor_graph = create_supervisor(
    agents=[complaints_agent, product_agent,],
    model=llm,
    prompt=("""You are the **Supervisor Agent** overseeing two specialist agents in an Amazon-style customer support system. Your job is to carefully analyze the user’s message and **choose the best agent** to respond.

You can also choose to **respond yourself** if the agents are not suitable or their responses fail.

🔹 `complaints_agent` – Handles:
 • Returns, refunds, or replacements  
 • Faulty, damaged, or wrong items  
 • Escalations to human support  
 • Warranty questions  
 • Refund policy and complaint handling

🔹 `product_agent` – Handles:
 • Product search by keyword or category  
 • Product comparisons or recommendations  
 • Availability in catalog  
 • Alternatives or substitutes  

📌 **Supervisor Decision Logic**:
1. If the query is about orders, complaints, or policies → choose `complaints_agent`
2. If the query is about product search, types, categories → choose `product_agent`
3. If the query involves both (e.g., return + buy new) → prioritize `complaints_agent`
4. If the query is a **greeting** (e.g., "hi", "hello", "hey"), respond warmly and politely.  
5. If the query is **unclear or too vague**, ask the user politely to clarify what they need help with.  
6. If none of the agents are applicable, respond as a **friendly fallback assistant**
7. If an agent gives an **empty**, **failed**, or **error response**, respond directly instead of forwarding.  

✅ Your output must always be a helpful, user-facing message — no internal reasoning or debugging logs.

📦 **Example Routing**:
- "Where is my phone?" → `complaints_agent`
- "Suggest a smartwatch under ₹5000." → `product_agent`
- "I got a broken mixer and want to order another." → `complaints_agent`
- "How does this work?" (no context) → you answer yourself: “Could you please tell me more about what you need help with?”
- Agent returns empty or system error → you apologize and answer: “Sorry about that! Let me help you directly…”

🛑 **Do NOT forward broken or vague agent messages to the user.**  
Respond clearly, kindly, and professionally as if you are Amazon customer care.

Your goal is to make sure the user always gets a helpful and relevant response.
"""

    ),
    output_mode="last_message",  # don’t expose inner reasoning
)

app_llm = supervisor_graph.compile(
    checkpointer=checkpointer,
    store=in_memory_store,
)

# # ── FastAPI Setup ───────────────────────────────────────────────────────────────
# api = FastAPI(title="Multi-Agent Chatbot API")

# class ChatRequest(BaseModel):
#     message: str
#     thread_id: str

# class ChatResponse(BaseModel):
#     response: str

# @api.post("/chat", response_model=ChatResponse)
# def chat_endpoint(req: ChatRequest):
#     config = {"configurable": {"thread_id": req.thread_id}}
#     result = app.invoke({"messages": [{"role": "user", "content": req.message}]}, config=config)
#     # extract final agent message
#     for msg in reversed(result["messages"]):
#         if isinstance(msg, AIMessage):
#             return ChatResponse(response=msg.content)
#     return ChatResponse(response="Sorry, I couldn't generate a response.")

# # Optional: endpoint to fetch thread history
# @api.get("/history/{thread_id}")
# def get_history(thread_id: str):
#     # This endpoint would return stored conversation context if available.
#     return {"thread_id": thread_id, "info": "history retrieval not yet implemented"}

# ── FastAPI setup ───────────────────────────────────────────────────────
api = FastAPI(title="Multi-Agent Chatbot API")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific origin like http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

class ExitRequest(BaseModel):
    user_id: str
    thread_id: str

@api.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    res = app_llm.invoke({"messages":[{"role":"user","content":req.message}]}, config=config)
    for msg in reversed(res["messages"]):
        if isinstance(msg, AIMessage):
            # Save to per-user thread history
            _save_conversation(req.user_id, req.thread_id, "user", req.message)
            _save_conversation(req.user_id, req.thread_id, "assistant", msg.content)
            return ChatResponse(response=msg.content)
    raise HTTPException(status_code=500, detail="No assistant response produced")

@api.post("/exit")
def exit_endpoint(req: ExitRequest):
    # Gracefully close thread: write in-memory conversation to disk
    user_log_path = os.path.join("history", f"{req.user_id}.json")
    os.makedirs("history", exist_ok=True)
    full_history = _load_all_history(user_log_path)
    # Filter entries by thread_id
    threads = [h for h in full_history if h["thread_id"] == req.thread_id]
    if not threads:
        return {"message": "No conversation found for this user/thread."}
    # Write/update per-user file
    with open(user_log_path, "w", encoding="utf-8") as f:
        json.dump(full_history, f, indent=2, ensure_ascii=False)
    return {"message": f"Saved {len(threads)} messages from thread '{req.thread_id}' for user '{req.user_id}'."}

def _save_conversation(user_id, thread_id, role, content):
    user_log_path = os.path.join("history", f"{user_id}.json") 
    entry = {
        "thread_id": thread_id,
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    logs = _load_all_history(user_log_path)
    logs.append(entry)
    with open(user_log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def _load_all_history(path):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []