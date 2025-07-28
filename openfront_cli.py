#!/usr/bin/env python3
import os
import sys
import argparse
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Set your Gemini key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDG7H8-Zl031uAxJL5u3aXZ8wx_lt71_I8"

def load_local_html(base_path="./openfrontpro.com"):
    """Load and parse HTML files from the website directory."""
    documents = []
    print("📚 Loading HTML files...")
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".html"):
                try:
                    with open(os.path.join(root, file), encoding='utf-8', errors='ignore') as f:
                        soup = BeautifulSoup(f, "lxml")
                        for tag in soup(['script', 'style', 'nav', 'footer']):
                            tag.decompose()
                        text = soup.get_text(separator='\n', strip=True)
                        if text:
                            documents.append(Document(page_content=text, metadata={"source": file}))
                except Exception as e:
                    print(f"⚠️  Warning: Could not process {file}: {e}")
    print(f"✅ Loaded {len(documents)} HTML files")
    return documents

def setup_qa_system(rebuild=False):
    """Set up the QA system with embeddings and vector store."""
    vectorstore_path = "./openfront_vectorstore"
    
    # Check if vector store already exists and rebuild is not requested
    if os.path.exists(vectorstore_path) and not rebuild:
        print("📂 Loading existing vector store...")
        try:
            embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vectorstore = FAISS.load_local(vectorstore_path, embedding_model)
            print("✅ Vector store loaded from disk")
        except Exception as e:
            print(f"⚠️  Could not load existing vector store: {e}")
            print("🔄 Creating new vector store...")
            vectorstore = create_new_vectorstore()
            # Save the vector store
            print("💾 Saving vector store to disk...")
            vectorstore.save_local(vectorstore_path)
            print("✅ Vector store saved")
    else:
        if rebuild:
            print("🔄 Rebuilding vector store...")
        else:
            print("🔄 Creating new vector store...")
        vectorstore = create_new_vectorstore()
        
        # Save the vector store
        print("💾 Saving vector store to disk...")
        vectorstore.save_local(vectorstore_path)
        print("✅ Vector store saved")
    
    # Set up QA chain
    print("🔗 Setting up QA chain...")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", convert_system_message_to_human=True)
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    print("✅ QA system ready!")
    
    return qa

def create_new_vectorstore():
    """Create a new vector store from HTML files."""
    # Load documents
    docs = load_local_html()
    if not docs:
        print("❌ No documents found! Make sure the openfrontpro.com directory exists.")
        return None
    
    # Split into chunks
    print("✂️  Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Create embeddings and vector store
    print("🧠 Creating embeddings...")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    print("✅ Vector store created")
    
    return vectorstore

def ask_question(qa_system, question):
    """Ask a question and get an answer."""
    try:
        print(f"\n🤔 Question: {question}")
        print("🔍 Searching for relevant information...")
        
        result = qa_system(question)
        
        print("\n🧠 Answer:")
        print(result["result"])
        
        print("\n📄 Source files:")
        for doc in result["source_documents"]:
            print(f" - {doc.metadata['source']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main CLI interface."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="OpenFront.io QA System")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector store from scratch")
    args = parser.parse_args()
    
    print("🎮 OpenFront.io QA System")
    print("=" * 50)
    
    # Check if website directory exists
    if not os.path.exists("./openfrontpro.com"):
        print("❌ Error: openfrontpro.com directory not found!")
        print("Make sure you're in the correct directory with your website files.")
        return
    
    # Set up the QA system
    qa_system = setup_qa_system(rebuild=args.rebuild)
    if not qa_system:
        return
    
    print("\n" + "=" * 50)
    print("🎯 Ready to answer your OpenFront.io questions!")
    print("💡 Example questions:")
    print("  - How does the gold mechanic work?")
    print("  - What are the best hotkeys?")
    print("  - How do I win consistently?")
    print("  - What's the optimal population ratio?")
    print("  - How do MIRVs work?")
    print("  - What are the best spawn locations?")
    print("\n💾 Vector store saved to: ./openfront_vectorstore")
    print("🔄 To rebuild: python openfront_cli.py --rebuild")
    print("\n💭 Type 'quit' or 'exit' to leave")
    print("=" * 50)
    
    # Interactive loop
    while True:
        try:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not question:
                print("⚠️  Please enter a question.")
                continue
                
            ask_question(qa_system, question)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 