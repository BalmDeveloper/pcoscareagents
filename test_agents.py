"""Test script for PCOS Care Agents."""
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pcos_agents import (
    create_pcos_specialist,
    create_nutritionist,
    create_fitness_coach,
    create_user_proxy_agent,
    get_config
)

def test_gemini_connection():
    """Test the connection to the Gemini API."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Configure Gemini
        gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content("Say hello!")
        print("✅ Successfully connected to Gemini API")
        return True
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        return False

def test_agents():
    """Test the PCOS Care Agents."""
    # Load environment variables
    load_dotenv()
    
    # Create output directory if it doesn't exist
    os.makedirs("_output", exist_ok=True)
    
    # Test Gemini connection first
    if not test_gemini_connection():
        print("Skipping agent tests due to Gemini connection issues.")
        return
    
    try:
        # Create agents
        print("\n=== Creating Agents ===")
        print("Creating PCOS Specialist...")
        pcos_specialist = create_pcos_specialist()
        print("Creating Nutritionist...")
        nutritionist = create_nutritionist()
        print("Creating Fitness Coach...")
        fitness_coach = create_fitness_coach()
        
        # Create user proxy agent
        print("Creating User Proxy...")
        user_proxy = create_user_proxy_agent("User_Proxy")
        
        # Test PCOS Specialist
        print("\n=== Testing PCOS Specialist ===")
        user_proxy.initiate_chat(
            pcos_specialist,
            message="What are the common symptoms of PCOS?"
        )
        
        # Test Nutritionist
        print("\n=== Testing Nutritionist ===")
        user_proxy.initiate_chat(
            nutritionist,
            message="What kind of diet would you recommend for someone with PCOS?"
        )
        
        # Test Fitness Coach
        print("\n=== Testing Fitness Coach ===")
        user_proxy.initiate_chat(
            fitness_coach,
            message="What type of exercises are beneficial for PCOS?"
        )
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        raise

if __name__ == "__main__":
    test_agents()
