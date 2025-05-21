from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional

class RootCauseAgent(PCOSAgent):
    """Agent responsible for analyzing and identifying root causes of PCOS symptoms"""
    
    COMMON_ROOT_CAUSES = {
        "insulin_resistance": {
            "name": "Insulin Resistance",
            "description": "Impaired ability of cells to respond to insulin, leading to compensatory hyperinsulinemia",
            "evidence_required": [
                "elevated_fasting_insulin",
                "elevated_hba1c",
                "acanthosis_nigricans",
                "weight_gain_around_abdomen"
            ],
            "prevalence": "70-80% of PCOS cases"
        },
        "chronic_inflammation": {
            "name": "Chronic Low-Grade Inflammation",
            "description": "Elevated inflammatory markers contributing to metabolic and reproductive dysfunction",
            "evidence_required": [
                "elevated_crp",
                "elevated_il6",
                "fatigue",
                "digestive_issues"
            ],
            "prevalence": "Common in PCOS"
        },
        "adrenal_hyperandrogenism": {
            "name": "Adrenal Hyperandrogenism",
            "description": "Excess androgen production from adrenal glands",
            "evidence_required": [
                "elevated_dheas",
                "normal_ovarian_imaging",
                "stress_history"
            ],
            "prevalence": "20-30% of PCOS cases"
        },
        "thyroid_dysfunction": {
            "name": "Thyroid Dysfunction",
            "description": "Hypothyroidism or Hashimoto's thyroiditis exacerbating PCOS symptoms",
            "evidence_required": [
                "elevated_tsh",
                "low_ft4",
                "thyroid_antibodies_present",
                "fatigue",
                "weight_gain"
            ],
            "prevalence": "Common comorbidity with PCOS"
        },
        "vitamin_d_deficiency": {
            "name": "Vitamin D Deficiency",
            "description": "Low vitamin D levels contributing to insulin resistance and inflammation",
            "evidence_required": [
                "low_vitamin_d",
                "bone_pain",
                "muscle_weakness"
            ],
            "prevalence": "67-85% of PCOS patients"
        },
        "gut_dysbiosis": {
            "name": "Gut Microbiome Imbalance",
            "description": "Altered gut microbiota contributing to inflammation and metabolic dysfunction",
            "evidence_required": [
                "digestive_issues",
                "food_intolerances",
                "history_of_antibiotic_use"
            ],
            "prevalence": "Common but underdiagnosed"
        },
        "sleep_apnea": {
            "name": "Sleep Apnea",
            "description": "Obstructive sleep apnea contributing to metabolic and hormonal imbalances",
            "evidence_required": [
                "daytime_sleepiness",
                "snoring",
                "morning_headaches",
                "elevated_bmi"
            ],
            "prevalence": "Up to 70% in obese PCOS patients"
        }
    }
    
    def __init__(self):
        super().__init__(
            name="Root Cause Analysis Agent",
            description="Identifies underlying causes and contributing factors to PCOS symptoms"
        )
        self.required_data = [
            'symptoms',
            'lab_results',
            'medical_history',
            'lifestyle_factors'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Analyze input data to identify potential root causes"""
        try:
            # Check for missing data
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data for root cause analysis: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Analyze potential root causes
            analysis = self._analyze_root_causes(input_data)
            
            # Prioritize root causes
            prioritized_causes = self._prioritize_causes(analysis, input_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(prioritized_causes, input_data)
            
            return AgentResponse(
                success=True,
                message="Root cause analysis completed",
                data={
                    "root_causes": prioritized_causes,
                    "recommendations": recommendations,
                    "all_possible_causes": self.COMMON_ROOT_CAUSES
                },
                next_steps=["labs_agent", "dietician"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error performing root cause analysis: {str(e)}"
            )
    
    def _analyze_root_causes(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Analyze data to identify potential root causes"""
        analysis = {}
        
        # Check each potential root cause
        for cause_id, cause_info in self.COMMON_ROOT_CAUSES.items():
            evidence = {}
            evidence_found = 0
            
            # Check for each piece of evidence
            for evidence_key in cause_info['evidence_required']:
                # Check symptoms
                if evidence_key in data.get('symptoms', []):
                    evidence[evidence_key] = {"present": True, "source": "symptoms"}
                    evidence_found += 1
                # Check lab results
                elif evidence_key in [r.get('test_name', '').lower() for r in data.get('lab_results', [])]:
                    evidence[evidence_key] = {"present": True, "source": "lab_results"}
                    evidence_found += 1
                # Check medical history
                elif evidence_key in data.get('medical_history', {}).get('conditions', []):
                    evidence[evidence_key] = {"present": True, "source": "medical_history"}
                    evidence_found += 1
                # Check lifestyle factors
                elif evidence_key in data.get('lifestyle_factors', {}):
                    evidence[evidence_key] = {"present": True, "source": "lifestyle_factors"}
                    evidence_found += 1
                else:
                    evidence[evidence_key] = {"present": False}
            
            # Calculate confidence score (percentage of evidence found)
            confidence = (evidence_found / len(cause_info['evidence_required'])) * 100
            
            analysis[cause_id] = {
                **cause_info,
                "evidence": evidence,
                "confidence_score": round(confidence, 1),
                "evidence_found": evidence_found,
                "total_evidence": len(cause_info['evidence_required'])
            }
        
        return analysis
    
    def _prioritize_causes(self, analysis: Dict[str, Any], data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize root causes based on evidence and confidence"""
        # Convert to list and sort by confidence score (descending)
        prioritized = sorted(
            analysis.values(),
            key=lambda x: x['confidence_score'],
            reverse=True
        )
        
        # Only include causes with at least some evidence
        prioritized = [cause for cause in prioritized if cause['confidence_score'] > 0]
        
        return prioritized
    
    def _generate_recommendations(self, causes: List[Dict[str, Any]], data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate personalized recommendations based on identified root causes"""
        recommendations = {
            "testing": [],
            "lifestyle": [],
            "medical": [],
            "monitoring": []
        }
        
        # Add general PCOS recommendations
        recommendations["lifestyle"].extend([
            "Maintain a balanced diet with adequate protein and fiber",
            "Engage in regular physical activity (both aerobic and resistance training)",
            "Practice stress-reduction techniques (mindfulness, yoga, meditation)",
            "Ensure adequate and consistent sleep (7-9 hours per night)"
        ])
        
        # Add cause-specific recommendations
        for cause in causes[:3]:  # Top 3 most likely causes
            cause_id = next((k for k, v in self.COMMON_ROOT_CAUSES.items() if v['name'] == cause['name']), None)
            
            if cause_id == "insulin_resistance" and cause['confidence_score'] >= 50:
                recommendations["lifestyle"].extend([
                    "Follow a low-glycemic index diet to manage blood sugar levels",
                    "Incorporate regular physical activity, especially after meals"
                ])
                recommendations["testing"].extend([
                    "Fasting insulin and glucose levels",
                    "Oral glucose tolerance test (OGTT)",
                    "HbA1c test"
                ])
                recommendations["medical"].append(
                    "Consider consultation for metformin or inositol supplements"
                )
            
            elif cause_id == "chronic_inflammation" and cause['confidence_score'] >= 50:
                recommendations["lifestyle"].extend([
                    "Incorporate anti-inflammatory foods (fatty fish, leafy greens, berries, nuts, olive oil)",
                    "Consider an elimination diet to identify food sensitivities"
                ])
                recommendations["testing"].extend([
                    "High-sensitivity C-reactive protein (hs-CRP)",
                    "Fasting insulin",
                    "Complete blood count (CBC)"
                ])
                recommendations["medical"].append(
                    "Consider omega-3 fatty acid supplementation"
                )
            
            # Add more cause-specific recommendations...
        
        # Add general monitoring recommendations
        recommendations["monitoring"].extend([
            "Track menstrual cycles and symptoms",
            "Regular monitoring of weight and waist circumference",
            "Annual comprehensive metabolic panel and lipid profile"
        ])
        
        # Remove duplicates while preserving order
        for key in recommendations:
            seen = set()
            recommendations[key] = [x for x in recommendations[key] if not (x in seen or seen.add(x))]
        
        return recommendations
