#!/usr/bin/env python3
"""
OpenFront Pro QA System Demo
Shows the system answering example questions automatically.
"""

import os
import sys
from openfront_cli import setup_qa_system

def run_demo():
    """Run a demo of the QA system with example questions."""
    print("🎮 OpenFront Pro QA System - Demo")
    print("=" * 50)
    
    # Check if website directory exists
    if not os.path.exists("./openfrontpro.com"):
        print("❌ Error: openfrontpro.com directory not found!")
        print("Make sure you're in the correct directory with your website files.")
        return
    
    # Set up the QA system
    print("🔄 Setting up QA system...")
    qa_system = setup_qa_system()
    if not qa_system:
        return
    
    # Demo questions
    demo_questions = [
        "How does the gold mechanic work?",
        "What are the best hotkeys?",
        "How do MIRVs work?",
        "What's the optimal population ratio?",
        "How do alliances work?"
    ]
    
    print("\n" + "=" * 50)
    print("🎯 Demo Questions")
    print("=" * 50)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. {question}")
        print("-" * 30)
        
        try:
            result = qa_system(question)
            print("Answer:", result["result"][:200] + "..." if len(result["result"]) > 200 else result["result"])
            print("Sources:", [doc.metadata['source'] for doc in result["source_documents"][:2]])
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("💡 Try running 'python openfront_cli.py' for interactive mode")
    print("=" * 50)

if __name__ == "__main__":
    run_demo() 