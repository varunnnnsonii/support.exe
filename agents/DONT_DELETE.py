# import uuid
# import pandas as pd
# from langchain_core.documents import Document
# from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# Load filtered data
# df = pd.read_csv("csvdatabase/filtered_final.csv")

# Prepare embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Convert DataFrame to LangChain Documents
# documents = [
#     Document(page_content=row["title"], metadata={"category": row["category_name"]})
#     for _, row in df.iterrows()
# ]

# # Create Chroma vector store
# vector_store = Chroma.from_documents(
#     documents=documents,
#     embedding=embedding_model,
#     persist_directory="./chroma_langchain_db",
#     collection_name="product_titles"
# )

# vector_store.persist()
# print("✅ Vector store created and persisted")
# Load store again (after restart)
vector_store = Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embedding_model,
    collection_name="product_titles"
)

query = "Lightweight men's training socks"
results = vector_store.similarity_search(query, k=10)

# Show top 10 results
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content} [{doc.metadata}]")
