from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json

@dataclass
class AgentResponse:
    """Standard response format for agent interactions"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    next_steps: Optional[List[str]] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

class PCOSAgent(ABC):
    """Base class for all PCOS care agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.required_data = []
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process the input data and return a response"""
        pass
    
    def get_required_data(self) -> List[str]:
        """Return a list of required data fields for this agent"""
        return self.required_data
    
    def get_info(self) -> Dict[str, Any]:
        """Return agent metadata"""
        return {
            "name": self.name,
            "description": self.description,
            "required_data": self.required_data
        }
