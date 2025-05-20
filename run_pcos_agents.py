"""
PCOS Care Agents - A multi-agent system for PCOS care and support.

This script initializes and runs a group chat with specialized agents for PCOS care,
including a PCOS Specialist, Nutritionist, and Fitness Coach.
"""
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager

from pcos_agents import (
    create_pcos_specialist,
    create_nutritionist,
    create_fitness_coach,
    create_user_proxy_agent,
    get_config
)

def check_gemini_connection():
    """Check if we can connect to the Gemini API."""
    try:
        gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not gemini_api_key:
            print("❌ Error: GOOGLE_GEMINI_API_KEY not found in environment variables")
            return False
            
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content("Test connection")
        return True
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        return False

def print_welcome():
    """Print the welcome message and instructions."""
    print("\n" + "=" * 50)
    print("PCOS CARE AGENTS".center(50))
    print("Your Personal PCOS Support System".center(50))
    print("=" * 50)
    print("\nAgents available:")
    print("• PCOS Specialist: For medical information and treatment options")
    print("• Nutritionist: For dietary advice and meal planning")
    print("• Fitness Coach: For exercise recommendations")
    print("\nType 'exit' at any time to end the conversation.\n")

def main():
    """Run the PCOS Care Agents."""
    # Load environment variables
    load_dotenv()
    
    # Create output directory if it doesn't exist
    os.makedirs("_output", exist_ok=True)
    
    # Check Gemini connection
    if not check_gemini_connection():
        print("\nPlease check your internet connection and API key, then try again.")
        sys.exit(1)
    
    try:
        # Create agents
        print("\nInitializing agents...")
        pcos_specialist = create_pcos_specialist()
        nutritionist = create_nutritionist()
        fitness_coach = create_fitness_coach()
        
        # Create user proxy agent
        user_proxy = create_user_proxy_agent("User_Proxy")
        
        # Create group chat
        groupchat = GroupChat(
            agents=[user_proxy, pcos_specialist, nutritionist, fitness_coach],
            messages=[],
            max_round=12
        )
        
        # Create group chat manager
        llm_config = get_config()
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        # Print welcome message
        print_welcome()
        
        # Start the conversation
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ('exit', 'quit', 'bye'):
                    print("\nThank you for using PCOS Care Agents. Goodbye!")
                    break
                
                # Start the chat with the user's input
                print("\nProcessing your question...")
                user_proxy.initiate_chat(
                    manager,
                    message=user_input
                )
                
            except KeyboardInterrupt:
                print("\n\nThank you for using PCOS Care Agents. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again or type 'exit' to quit.")
                
    except Exception as e:
        print(f"\n❌ An error occurred while initializing the agents: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThank you for using PCOS Care Agents. Goodbye!")
        sys.exit(0)
