import os
import re
import pandas as pd

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "company_data.xlsx")

# Load Excel
df = pd.read_excel(EXCEL_PATH)
df.columns = df.columns.str.strip()
q_col = "Question " if "Question " in df.columns else "Question"

# Build lookup dict
qa_dict = {}
for _, row in df.iterrows():
    q = str(row[q_col]).strip().lower()
    a = str(row["Answer"]).strip()
    qa_dict[q] = a

print(f"Chatbot ready! Loaded {len(qa_dict)} Q&A pairs.", flush=True)

# Remove common filler words for better matching
STOPWORDS = {"do", "you", "your", "is", "are", "the", "a", "an", "i", "what",
             "how", "can", "we", "our", "does", "have", "has", "me", "please",
             "tell", "about", "us", "give", "provide", "offer", "get", "for"}

def keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(w for w in words if w not in STOPWORDS and len(w) > 2)

def ask_question(query: str) -> str:
    query_clean = query.strip().lower()

    # 1 Exact match
    if query_clean in qa_dict:
        return qa_dict[query_clean]

    # 2 Substring match
    for q, a in qa_dict.items():
        if query_clean in q or q in query_clean:
            return a

    # 3 Keyword overlap (ignoring stopwords)
    query_kw  = keywords(query_clean)
    best_ans  = None
    best_score = 0

    for q, a in qa_dict.items():
        q_kw    = keywords(q)
        overlap = len(query_kw & q_kw)
        # Bonus: if all query keywords found in question
        if query_kw and query_kw.issubset(q_kw):
            overlap += 5
        if overlap > best_score:
            best_score = overlap
            best_ans   = a

    if best_score >= 1 and best_ans:
        return best_ans

    return "Sorry, I don't have information about that. Please contact us at info@kvontech.com or call +91-74248 39191."