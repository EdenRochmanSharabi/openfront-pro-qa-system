#!/usr/bin/env python3
"""
OpenFront.io Real-Time AI Assistant
Takes screenshots every 5 seconds, analyzes them, and provides live strategic advice.
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageGrab
import io
import base64
from openfront_cli import setup_qa_system
import google.generativeai as genai

# Load environment variables
load_dotenv()

class OpenFrontRealtimeAssistant:
    def __init__(self):
        self.qa_system = None
        self.running = False
        self.screenshot_interval = 5  # seconds - increased for reliability
        
        # Initialize Gemini for vision
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY environment variable not set!")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel('gemini-1.5-pro')
        
        print("🎮 OpenFront.io Real-Time AI Assistant")
        print("=" * 50)
    
    def setup_systems(self):
        """Set up the QA system."""
        print("🔄 Setting up AI systems...")
        
        # Set up QA system for knowledge base
        self.qa_system = setup_qa_system()
        if not self.qa_system:
            print("❌ Failed to set up QA system")
            return False
        
        print("✅ AI systems ready!")
        return True
    
    def take_screenshot(self):
        """Take a screenshot of the entire screen."""
        try:
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return None
    
    def encode_image(self, image):
        """Convert PIL image to base64 for Gemini."""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def analyze_screenshot(self, screenshot):
        """Analyze the screenshot and provide strategic advice."""
        try:
            # Encode image for Gemini
            image_data = self.encode_image(screenshot)
            
            # Simple, direct prompt
            prompt = """
            You are an expert OpenFront.io player. Look at this screenshot and:

            1. If you see OpenFront.io game (map with territories, troop numbers, leaderboard), provide strategic advice in 2-3 sentences about what the player should do next.

            2. If you don't see OpenFront.io, respond with exactly: "Not OpenFront.io detected"

            Be specific and actionable with your advice.
            """
            
            # Generate response using Gemini Vision
            response = self.vision_model.generate_content([
                prompt,
                {
                    "mime_type": "image/png",
                    "data": image_data
                }
            ])
            
            return response.text.strip()
            
        except Exception as e:
            return f"❌ Analysis error: {e}"
    
    def get_knowledge_advice(self, game_state_description):
        """Get strategic advice from the knowledge base."""
        try:
            # Create a question based on the game state
            question = f"Based on this game state: {game_state_description}, what should I do next in OpenFront.io?"
            
            result = self.qa_system(question)
            return result["result"]
        except Exception as e:
            return f"❌ Knowledge base error: {e}"
    
    def display_advice(self, vision_advice, knowledge_advice):
        """Display the advice in a formatted way."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n🕐 {timestamp} - Real-Time Advice")
        print("=" * 50)
        
        if "Not OpenFront.io detected" in vision_advice:
            print("👀 Waiting for OpenFront.io game...")
        else:
            print("🎯 STRATEGIC ADVICE:")
            print(f"   {vision_advice}")
            
            if knowledge_advice and "❌" not in knowledge_advice:
                print("\n📚 EXPERT INSIGHTS:")
                print(f"   {knowledge_advice}")
        
        print("=" * 50)
    
    def screenshot_loop(self):
        """Main loop for taking screenshots and analyzing them."""
        print("📸 Starting screenshot analysis...")
        print("💡 Press Ctrl+C to stop")
        print("🎮 Make sure OpenFront.io is visible on your screen!")
        
        while self.running:
            try:
                # Take screenshot
                screenshot = self.take_screenshot()
                if not screenshot:
                    time.sleep(self.screenshot_interval)
                    continue
                
                # Analyze screenshot
                vision_advice = self.analyze_screenshot(screenshot)
                
                # Get knowledge base advice if it's OpenFront.io
                knowledge_advice = ""
                if "Not OpenFront.io detected" not in vision_advice:
                    knowledge_advice = self.get_knowledge_advice(vision_advice)
                
                # Display advice
                self.display_advice(vision_advice, knowledge_advice)
                
                # Wait for next screenshot
                time.sleep(self.screenshot_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping assistant...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error in screenshot loop: {e}")
                time.sleep(self.screenshot_interval)
    
    def start(self):
        """Start the real-time assistant."""
        if not self.setup_systems():
            return
        
        self.running = True
        
        try:
            self.screenshot_loop()
        except KeyboardInterrupt:
            print("\n👋 Assistant stopped!")
        finally:
            self.running = False

def main():
    """Main function to run the assistant."""
    print("🎮 OpenFront.io Real-Time AI Assistant")
    print("=" * 50)
    print("This assistant will:")
    print("📸 Take screenshots every 5 seconds")
    print("🤖 Analyze your OpenFront.io gameplay")
    print("💡 Provide real-time strategic advice")
    print("📚 Use the knowledge base for expert tips")
    print("\n💭 Make sure OpenFront.io is visible on your screen!")
    print("=" * 50)
    
    assistant = OpenFrontRealtimeAssistant()
    assistant.start()

if __name__ == "__main__":
    main() 