from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any

class BiologyAgent(PCOSAgent):
    """Agent responsible for understanding patient biology and symptoms"""
    
    def __init__(self):
        super().__init__(
            name="Biology Agent",
            description="Handles initial patient intake and biological assessment"
        )
        self.required_data = [
            'age', 'weight', 'height', 'menstrual_cycle_regularity',
            'symptoms', 'medical_history', 'family_history'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process biological and symptom data"""
        try:
            # Basic validation
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Basic assessment
            bmi = self._calculate_bmi(input_data['weight'], input_data['height'])
            assessment = self._perform_initial_assessment(input_data, bmi)
            
            return AgentResponse(
                success=True,
                message="Biological assessment completed",
                data={"assessment": assessment, "bmi": bmi},
                next_steps=["upload_labs", "identify_phenotype"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error processing biological data: {str(e)}"
            )
    
    def _calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate BMI from weight in kg and height in cm"""
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 1)
    
    def _perform_initial_assessment(self, data: Dict[str, Any], bmi: float) -> Dict[str, Any]:
        """Perform initial assessment based on biological data"""
        assessment = {
            "bmi_category": self._get_bmi_category(bmi),
            "symptoms_analysis": self._analyze_symptoms(data['symptoms']),
            "risk_factors": self._identify_risk_factors(data)
        }
        return assessment
    
    def _get_bmi_category(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def _analyze_symptoms(self, symptoms: list) -> Dict[str, Any]:
        """Analyze reported symptoms"""
        common_pcos_symptoms = [
            'irregular_periods', 'hirsutism', 'acne', 'hair_loss',
            'weight_gain', 'fatigue', 'mood_swings', 'infertility'
        ]
        
        present_symptoms = [s for s in symptoms if s in common_pcos_symptoms]
        symptom_severity = len(present_symptoms) / len(common_pcos_symptoms)
        
        return {
            "present_symptoms": present_symptoms,
            "symptom_severity": symptom_severity,
            "concern_level": "high" if symptom_severity > 0.5 else "moderate"
        }
    
    def _identify_risk_factors(self, data: Dict[str, Any]) -> list:
        """Identify potential risk factors"""
        risk_factors = []
        
        # Family history risks
        if data.get('family_history', {}).get('pcos', False):
            risk_factors.append("Family history of PCOS")
        
        # Weight-related risks
        bmi = self._calculate_bmi(data['weight'], data['height'])
        if bmi >= 25:
            risk_factors.append(f"Elevated BMI ({bmi})")
            
        # Age-related considerations
        age = data.get('age')
        if age < 18:
            risk_factors.append("Adolescent patient - special considerations needed")
        elif age > 35:
            risk_factors.append("Advanced maternal age - fertility considerations")
            
        return risk_factors
