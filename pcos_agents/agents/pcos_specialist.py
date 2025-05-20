"""PCOS Specialist Agent."""
from autogen import AssistantAgent
from ..config import create_agent, get_config

PCOS_SPECIALIST_SYSTEM_MESSAGE = """You are a PCOS Specialist with deep knowledge of Polycystic Ovary Syndrome. 
Your expertise includes:
- Symptoms and diagnosis of PCOS
- Treatment options and management strategies
- Lifestyle modifications and dietary recommendations
- Hormonal imbalances and their effects
- Fertility issues related to PCOS
- Latest research and treatment options

When providing information, be empathetic, evidence-based, and clear. 
Always ask for clarification if the user's question is unclear.
"""

def create_pcos_specialist():
    """Create and return a PCOS Specialist agent."""
    return create_agent(
        name="PCOS_Specialist",
        system_message=PCOS_SPECIALIST_SYSTEM_MESSAGE,
        llm_config=get_config()
    )
