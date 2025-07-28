import os
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# STEP 0: Set your Gemini key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDG7H8-Zl031uAxJL5u3aXZ8wx_lt71_I8"  # or set via environment variable

# STEP 1: Parse HTML files
def load_local_html(base_path="./openfrontpro.com"):
    documents = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f, "lxml")
                    for tag in soup(['script', 'style', 'nav', 'footer']):
                        tag.decompose()
                    text = soup.get_text(separator='\n', strip=True)
                    if text:
                        documents.append(Document(page_content=text, metadata={"source": file}))
    return documents

docs = load_local_html()

# STEP 2: Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# STEP 3: Use Gemini embeddings + FAISS
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(chunks, embedding_model)

# STEP 4: Build Gemini-based Retriever + LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", convert_system_message_to_human=True)
retriever = vectorstore.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

# STEP 5: Ask questions
query = "What does the gold mechanic do?"
result = qa(query)

print("\n🧠 Answer:")
print(result["result"])

print("\n📄 Source files:")
for doc in result["source_documents"]:
    print(f" - {doc.metadata['source']}") 