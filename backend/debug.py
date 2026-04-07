import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "company_data.xlsx")

print("=== LOADING EXCEL ===")
df = pd.read_excel(EXCEL_PATH)
df.columns = df.columns.str.strip()
print(f"Total rows loaded: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\n=== ALL ROWS ===")
for i, row in df.iterrows():
    print(f"Row {i}: Q={row.get('Question', row.get('Question ', '???'))} | A={row['Answer']}")

print("\n=== BUILDING VECTOR STORE ===")
documents = []
for _, row in df.iterrows():
    question = str(row.get("Question ", row.get("Question", ""))).strip()
    answer   = str(row["Answer"]).strip()
    content  = f"Question: {question}\nAnswer: {answer}"
    documents.append(Document(page_content=content))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embeddings)

print(f"\nTotal documents in vector store: {len(documents)}")

print("\n=== TEST SEARCH ===")
test_query = input("Type your test question: ")
results = vectorstore.similarity_search(test_query, k=1)
if results:
    print("\nBest match found:")
    print(results[0].page_content)
else:
    print("No results found.")