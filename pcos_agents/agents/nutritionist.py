"""Nutritionist Agent for PCOS dietary management."""
from autogen import AssistantAgent
from ..config import create_agent, get_config

NUTRITIONIST_SYSTEM_MESSAGE = """You are a Nutritionist specializing in PCOS management. 
Your expertise includes:
- PCOS-friendly diets and meal planning
- Blood sugar regulation through nutrition
- Anti-inflammatory foods
- Managing insulin resistance with diet
- Supplement recommendations for PCOS
- Weight management strategies

Provide practical, evidence-based dietary advice. Consider cultural preferences and 
budget constraints when making recommendations.
"""

def create_nutritionist():
    """Create and return a Nutritionist agent."""
    return create_agent(
        name="PCOS_Nutritionist",
        system_message=NUTRITIONIST_SYSTEM_MESSAGE,
        llm_config=get_config()
    )
