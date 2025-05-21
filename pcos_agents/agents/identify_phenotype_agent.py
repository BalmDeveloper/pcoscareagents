from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional

class IdentifyPhenotypeAgent(PCOSAgent):
    """Agent responsible for identifying PCOS phenotypes based on symptoms and lab results"""
    
    # Rotterdam criteria for PCOS diagnosis (need 2 out of 3):
    # 1. Oligo-ovulation or anovulation
    # 2. Clinical and/or biochemical signs of hyperandrogenism
    # 3. Polycystic ovaries on ultrasound
    
    PHENOTYPES = {
        "A": {
            "name": "Classic PCOS (Hyperandrogenic, Oligo-ovulatory, Polycystic Ovaries)",
            "description": "Classic PCOS with all three Rotterdam criteria met",
            "prevalence": "~50% of PCOS cases",
            "characteristics": [
                "Irregular or absent periods",
                "Elevated androgens (clinical or biochemical)",
                "Polycystic ovaries on ultrasound",
                "Often associated with insulin resistance"
            ]
        },
        "B": {
            "name": "Ovulatory PCOS (Hyperandrogenic, Ovulatory, Polycystic Ovaries)",
            "description": "PCOS with hyperandrogenism and polycystic ovaries but regular cycles",
            "prevalence": "~20% of PCOS cases",
            "characteristics": [
                "Regular menstrual cycles",
                "Signs of hyperandrogenism (hirsutism, acne, etc.)",
                "Polycystic ovaries on ultrasound"
            ]
        },
        "C": {
            "name": "Non-Polycystic Ovary PCOS (Hyperandrogenic, Oligo-ovulatory, Normal Ovaries)",
            "description": "PCOS with hyperandrogenism and ovulatory dysfunction but normal ovaries",
            "prevalence": "~20% of PCOS cases",
            "characteristics": [
                "Irregular or absent periods",
                "Signs of hyperandrogenism",
                "Normal ovarian morphology on ultrasound"
            ]
        },
        "D": {
            "name": "Non-Hyperandrogenic PCOS (Normoandrogenic, Oligo-ovulatory, Polycystic Ovaries)",
            "description": "PCOS with ovulatory dysfunction and polycystic ovaries but no hyperandrogenism",
            "prevalence": "~10% of PCOS cases",
            "characteristics": [
                "Irregular or absent periods",
                "No clinical or biochemical hyperandrogenism",
                "Polycystic ovaries on ultrasound"
            ]
        },
        "Non-PCOS": {
            "name": "No PCOS Diagnosis",
            "description": "Insufficient evidence for PCOS diagnosis",
            "characteristics": [
                "Does not meet Rotterdam criteria",
                "May need evaluation for other conditions"
            ]
        }
    }
    
    def __init__(self):
        super().__init__(
            name="Identify Phenotype Agent",
            description="Identifies the PCOS phenotype based on symptoms and test results"
        )
        self.required_data = [
            'menstrual_cycle_regularity',
            'clinical_hyperandrogenism',
            'biochemical_hyperandrogenism',
            'ultrasound_results'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Determine the PCOS phenotype based on input data"""
        try:
            # Check for missing data
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data for phenotype identification: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Evaluate Rotterdam criteria
            criteria_met = self._evaluate_rotterdam_criteria(input_data)
            
            # Determine phenotype based on criteria met
            phenotype = self._determine_phenotype(criteria_met, input_data)
            
            # Get management recommendations
            management = self._get_management_recommendations(phenotype, input_data)
            
            return AgentResponse(
                success=True,
                message=f"Phenotype identification complete: {phenotype}",
                data={
                    "phenotype": phenotype,
                    "criteria_met": criteria_met,
                    "management_recommendations": management,
                    "all_phenotypes": self.PHENOTYPES
                },
                next_steps=["root_cause_analysis", "dietician"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error identifying phenotype: {str(e)}"
            )
    
    def _evaluate_rotterdam_criteria(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Evaluate which Rotterdam criteria are met"""
        # Criterion 1: Oligo-ovulation or anovulation
        oligo_ovulation = data.get('menstrual_cycle_regularity', '') in ['oligomenorrhea', 'amenorrhea']
        
        # Criterion 2: Clinical and/or biochemical hyperandrogenism
        clinical_hyperandrogenism = data.get('clinical_hyperandrogenism', False)
        biochemical_hyperandrogenism = data.get('biochemical_hyperandrogenism', False)
        hyperandrogenism = clinical_hyperandrogenism or biochemical_hyperandrogenism
        
        # Criterion 3: Polycystic ovaries on ultrasound
        polycystic_ovaries = data.get('ultrasound_results', {}).get('pcos_morphology', False)
        
        return {
            "oligo_anovulation": oligo_ovulation,
            "hyperandrogenism": hyperandrogenism,
            "polycystic_ovaries": polycystic_ovaries
        }
    
    def _determine_phenotype(self, criteria: Dict[str, bool], data: Dict[str, Any]) -> str:
        """Determine the specific PCOS phenotype"""
        met = [k for k, v in criteria.items() if v]
        
        # Need at least 2 out of 3 criteria for PCOS diagnosis
        if len(met) < 2:
            return "Non-PCOS"
            
        # Phenotype A: All three criteria
        if len(met) == 3:
            return "A"
            
        # Phenotype B: Hyperandrogenism + Polycystic ovaries
        if criteria["hyperandrogenism"] and criteria["polycystic_ovaries"]:
            return "B"
            
        # Phenotype C: Hyperandrogenism + Oligo-anovulation
        if criteria["hyperandrogenism"] and criteria["oligo_anovulation"]:
            return "C"
            
        # Phenotype D: Oligo-anovulation + Polycystic ovaries
        if criteria["oligo_anovulation"] and criteria["polycystic_ovaries"]:
            return "D"
            
        return "Non-PCOS"
    
    def _get_management_recommendations(self, phenotype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate management recommendations based on phenotype"""
        recommendations = {
            "lifestyle": [],
            "medical": [],
            "monitoring": []
        }
        
        # Common recommendations for all PCOS types
        if phenotype != "Non-PCOS":
            recommendations["lifestyle"].extend([
                "Maintain a healthy weight through diet and exercise",
                "Engage in regular physical activity (150 minutes/week)",
                "Follow a balanced diet with emphasis on whole foods"
            ])
            recommendations["monitoring"].extend([
                "Regular monitoring of weight and BMI",
                "Annual screening for diabetes/impaired glucose tolerance",
                "Regular lipid profile assessment"
            ])
        
        # Phenotype-specific recommendations
        if phenotype in ["A", "B", "C"]:  # Hyperandrogenic phenotypes
            recommendations["medical"].append(
                "Consider anti-androgen therapy if hirsutism/acne is problematic"
            )
            
        if phenotype in ["A", "C", "D"]:  # Oligo-ovulatory phenotypes
            if data.get('fertility_goals', {}).get('pregnancy_desired', False):
                recommendations["medical"].append(
                    "Ovulation induction may be needed for fertility"
                )
            else:
                recommendations["medical"].append(
                    "Hormonal contraceptives may regulate cycles and reduce endometrial cancer risk"
                )
        
        # Additional considerations for insulin resistance
        if data.get('insulin_resistance', {}).get('present', False):
            recommendations["medical"].append(
                "Consider metformin or other insulin-sensitizing agents"
            )
        
        return recommendations
