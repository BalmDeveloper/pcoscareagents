"""Configuration for PCOS Care Agents."""
import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API
def configure_gemini():
    """Configure the Gemini API with the API key."""
    gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=gemini_api_key)
    return genai

def get_config():
    """Get the configuration for the agents."""
    # Configure Gemini
    configure_gemini()
    
    # For AutoGen, we'll use a dummy config since we'll be using Gemini directly
    config_list = [
        {
            "model": "gemini-1.5-pro-latest",
            "api_key": "dummy_key",  # Not used directly by AutoGen
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
        }
    ]
    
    # LLM configuration
    llm_config = {
        "config_list": config_list,
        "timeout": 120,
        "use_dummy": True,  # We'll handle the actual API calls with Gemini
    }
    
    return llm_config

def create_agent(name, system_message, llm_config):
    """Create an agent with the given name and system message."""
    return AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=llm_config,
    )

def create_user_proxy_agent(name, human_input_mode="NEVER"):
    """Create a user proxy agent."""
    return UserProxyAgent(
        name=name,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"work_dir": "_output"},
    )
