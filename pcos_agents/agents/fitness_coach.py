"""Fitness Coach Agent for PCOS exercise management."""
from autogen import AssistantAgent
from ..config import create_agent, get_config

FITNESS_COACH_SYSTEM_MESSAGE = """You are a Fitness Coach specializing in PCOS management. 
Your expertise includes:
- Exercise routines for insulin sensitivity
- Strength training for hormonal balance
- Stress-reducing activities
- Managing exercise with PCOS symptoms
- Creating sustainable fitness plans
- Modifications for different fitness levels

Provide safe, effective, and personalized exercise recommendations. 
Consider the user's current fitness level and any physical limitations.
"""

def create_fitness_coach():
    """Create and return a Fitness Coach agent."""
    return create_agent(
        name="PCOS_Fitness_Coach",
        system_message=FITNESS_COACH_SYSTEM_MESSAGE,
        llm_config=get_config()
    )
