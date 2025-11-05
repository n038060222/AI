from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Load environment variables ---
load_dotenv()

# --- 1. LOAD DOCUMENTS FROM WEB ---
loader = WebBaseLoader(
   [
       "https://angular.dev/guide/signals",
       "https://angular.dev/guide/signals/linked-signal",
       "https://angular.dev/guide/signals/resource",
   ]
)
docs = loader.load()

# --- 2. SPLIT TEXT ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=100, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

# --- 3. CREATE VECTOR STORE ---
vectorstore = Chroma.from_documents(
    documents=all_splits,
    embedding=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"),
)

# --- 4. CREATE RETRIEVER ---
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# --- 5. DEFINE LLM ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- 6. PROMPT TEMPLATE ---
prompt = """
You are an assistant that answers questions about Angular Signals.
Use the provided context to answer clearly and briefly (3 sentences max).
If you don't know — say you don't know.

Include at the end of your answer:
"📚 Source: [link_to_the_original_page]"

Question:
{question}

Context:
{context}

Answer:
"""

# --- 7. FORMAT FUNCTIONS ---
def format_docs(original_docs):
    """Format retrieved documents including their source URLs."""
    formatted = []
    for doc in original_docs:
        source = getattr(doc.metadata, "source", None) or doc.metadata.get("source", "")
        formatted.append(f"Source: {source}\n{doc.page_content}")
    return "\n\n".join(formatted)

# --- 8. RAG CHAIN ---
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 9. STREAM FUNCTION ---
def stream_rag_chain(text):
    """Stream the model's output for a given user question."""
    for chunk in rag_chain.stream(text):
        yield chunk
