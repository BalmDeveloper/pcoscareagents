from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class LabsAgent(PCOSAgent):
    """Agent responsible for recommending necessary lab tests based on patient data"""
    
    # Define standard PCOS-related lab panels
    LAB_PANELS = {
        "initial_pcos_evaluation": {
            "name": "Initial PCOS Evaluation Panel",
            "description": "Comprehensive initial lab workup for PCOS diagnosis and evaluation",
            "tests": [
                "CBC with differential",
                "Comprehensive Metabolic Panel (CMP)",
                "Lipid Panel",
                "Hemoglobin A1c (HbA1c)",
                "Fasting Insulin",
                "Fasting Glucose",
                "25-Hydroxy Vitamin D",
                "Thyroid Stimulating Hormone (TSH)",
                "Free T4",
                "Thyroid Peroxidase Antibodies (TPO)",
                "Prolactin",
                "Total Testosterone",
                "Free Testosterone",
                "DHEA-Sulfate",
                "Sex Hormone Binding Globulin (SHBG)",
                "Luteinizing Hormone (LH)",
                "Follicle Stimulating Hormone (FSH)",
                "Estradiol",
                "Progesterone (day 21 of cycle)",
                "AMH (Anti-Müllerian Hormone)",
                "C-Reactive Protein (hs-CRP)",
                "Fasting Lipid Profile"
            ],
            "frequency": "As needed for diagnosis and initial evaluation",
            "notes": "Best performed during days 3-5 of menstrual cycle if possible"
        },
        "insulin_resistance": {
            "name": "Insulin Resistance Panel",
            "description": "Tests to evaluate for insulin resistance and glucose metabolism",
            "tests": [
                "Fasting Insulin",
                "Fasting Glucose",
                "Hemoglobin A1c (HbA1c)",
                "2-hour Oral Glucose Tolerance Test (OGTT)",
                "C-Peptide",
                "HOMA-IR (calculated from fasting glucose and insulin)"
            ],
            "frequency": "Annually or as clinically indicated",
            "notes": "Fasting required for 8-12 hours before testing"
        },
        "androgen_panel": {
            "name": "Androgen Panel",
            "description": "Evaluation of androgen levels and metabolism",
            "tests": [
                "Total Testosterone",
                "Free Testosterone",
                "DHEA-Sulfate",
                "Androstenedione",
                "Sex Hormone Binding Globulin (SHBG)",
                "Free Androgen Index (FAI, calculated)"
            ],
            "frequency": "As needed for diagnosis and monitoring",
            "notes": "Best performed in the morning during days 3-5 of menstrual cycle"
        },
        "adrenal_panel": {
            "name": "Adrenal Function Panel",
            "description": "Evaluation of adrenal gland function and steroidogenesis",
            "tests": [
                "DHEA-Sulfate",
                "17-Hydroxyprogesterone (17-OHP)",
                "Cortisol (AM and PM)",
                "ACTH",
                "24-hour Urinary Free Cortisol",
                "Aldosterone",
                "Renin Activity"
            ],
            "frequency": "As clinically indicated",
            "notes": "Timing of collection is important for some tests"
        },
        "inflammation_panel": {
            "name": "Inflammation and Autoimmunity Panel",
            "description": "Markers of inflammation and autoimmune activity",
            "tests": [
                "C-Reactive Protein (hs-CRP)",
                "Erythrocyte Sedimentation Rate (ESR)",
                "Antinuclear Antibody (ANA)",
                "Thyroid Peroxidase Antibodies (TPO)",
                "Thyroglobulin Antibodies",
                "Interleukin-6 (IL-6)",
                "Tumor Necrosis Factor-alpha (TNF-α)",
                "Homocysteine"
            ],
            "frequency": "As clinically indicated",
            "notes": "Fasting not required"
        },
        "nutrient_deficiency": {
            "name": "Nutrient Deficiency Panel",
            "description": "Assessment of common nutrient deficiencies in PCOS",
            "tests": [
                "25-Hydroxy Vitamin D",
                "Magnesium (RBC)",
                "Zinc",
                "Selenium",
                "Vitamin B12",
                "Folate (RBC)",
                "Ferritin",
                "Iron and Total Iron Binding Capacity (TIBC)",
                "Omega-3 Index"
            ],
            "frequency": "Annually or as indicated",
            "notes": "Fasting not required"
        },
        "cardiovascular_risk": {
            "name": "Cardiovascular Risk Panel",
            "description": "Assessment of cardiovascular risk factors",
            "tests": [
                "Lipid Panel (Total Cholesterol, HDL, LDL, Triglycerides)",
                "Lipoprotein(a)",
                "Apolipoprotein B",
                "Homocysteine",
                "hs-CRP",
                "Fasting Insulin",
                "Hemoglobin A1c (HbA1c)",
                "Uric Acid"
            ],
            "frequency": "Annually or as indicated",
            "notes": "Fasting required for lipid panel"
        },
        "fertility_panel": {
            "name": "Fertility and Reproductive Panel",
            "description": "Evaluation of reproductive hormones and fertility markers",
            "tests": [
                "Luteinizing Hormone (LH)",
                "Follicle Stimulating Hormone (FSH)",
                "Estradiol",
                "Progesterone (day 21)",
                "Prolactin",
                "AMH (Anti-Müllerian Hormone)",
                "Inhibin B",
                "Thyroid Stimulating Hormone (TSH)",
                "Free T4"
            ],
            "frequency": "As part of fertility evaluation",
            "notes": "Timing in menstrual cycle is critical for accurate results"
        }
    }
    
    def __init__(self):
        super().__init__(
            name="Labs Agent",
            description="Recommends necessary lab tests based on patient profile and missing information"
        )
        self.required_data = [
            'patient_id',
            'previous_labs',
            'symptoms',
            'medical_history',
            'current_medications'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Analyze patient data and recommend necessary lab tests"""
        try:
            # Check for missing data
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data for lab recommendations: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Get previously completed labs
            previous_labs = input_data.get('previous_labs', [])
            
            # Determine which labs are needed
            recommended_labs = self._determine_needed_labs(input_data, previous_labs)
            
            # Prioritize recommendations
            prioritized_labs = self._prioritize_labs(recommended_labs, input_data)
            
            # Generate follow-up instructions
            follow_up = self._generate_follow_up_instructions(prioritized_labs)
            
            return AgentResponse(
                success=True,
                message="Lab recommendations generated successfully",
                data={
                    "recommended_labs": prioritized_labs,
                    "follow_up_instructions": follow_up,
                    "all_lab_panels": self.LAB_PANELS
                },
                next_steps=["dietician", "obgyn"]
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error generating lab recommendations: {str(e)}"
            )
    
    def _determine_needed_labs(self, patient_data: Dict[str, Any], previous_labs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Determine which lab tests are needed based on patient data"""
        needed_labs = []
        
        # Always recommend initial PCOS evaluation if no previous comprehensive testing
        if not self._has_comprehensive_evaluation(previous_labs):
            needed_labs.append({
                **self.LAB_PANELS["initial_pcos_evaluation"],
                "priority": "high",
                "reason": "No previous comprehensive PCOS evaluation found"
            })
        
        # Check for specific conditions that require additional testing
        symptoms = patient_data.get('symptoms', {})
        medical_history = patient_data.get('medical_history', {})
        
        # Check for signs of insulin resistance
        if any([
            symptoms.get('weight_gain'),
            symptoms.get('acanthosis_nigricans'),
            medical_history.get('prediabetes'),
            medical_history.get('diabetes'),
            'insulin_resistance' in medical_history.get('conditions', [])
        ]):
            needed_labs.append({
                **self.LAB_PANELS["insulin_resistance"],
                "priority": "high",
                "reason": "Signs or history suggesting insulin resistance"
            })
        
        # Check for hyperandrogenism
        if any([
            symptoms.get('hirsutism'),
            symptoms.get('acne'),
            symptoms.get('androgenic_alopecia')
        ]):
            needed_labs.append({
                **self.LAB_PANELS["androgen_panel"],
                "priority": "medium",
                "reason": "Signs of hyperandrogenism present"
            })
        
        # Check for inflammation markers
        if any([
            symptoms.get('fatigue'),
            symptoms.get('joint_pain'),
            medical_history.get('autoimmune_disease'),
            'inflammation' in medical_history.get('conditions', [])
        ]):
            needed_labs.append({
                **self.LAB_PANELS["inflammation_panel"],
                "priority": "medium",
                "reason": "Signs of chronic inflammation"
            })
        
        # Check for fertility concerns
        if patient_data.get('reproductive_goals', {}).get('pregnancy_planning'):
            needed_labs.append({
                **self.LAB_PANELS["fertility_panel"],
                "priority": "high",
                "reason": "Pregnancy planning or fertility concerns"
            })
        
        # Always check for nutrient deficiencies in PCOS
        needed_labs.append({
            **self.LAB_PANELS["nutrient_deficiency"],
            "priority": "medium",
            "reason": "Routine screening for common PCOS nutrient deficiencies"
        })
        
        # Check for cardiovascular risk factors
        if any([
            medical_history.get('hypertension'),
            medical_history.get('high_cholesterol'),
            medical_history.get('heart_disease'),
            patient_data.get('family_history', {}).get('heart_disease'),
            patient_data.get('lifestyle_factors', {}).get('smoking')
        ]):
            needed_labs.append({
                **self.LAB_PANELS["cardiovascular_risk"],
                "priority": "high",
                "reason": "Cardiovascular risk factors present"
            })
        
        # Remove duplicates
        seen = set()
        unique_labs = []
        for lab in needed_labs:
            if lab['name'] not in seen:
                seen.add(lab['name'])
                unique_labs.append(lab)
        
        return unique_labs
    
    def _has_comprehensive_evaluation(self, previous_labs: List[Dict[str, Any]]) -> bool:
        """Check if patient has had a comprehensive PCOS evaluation"""
        if not previous_labs:
            return False
            
        # Check if any previous lab set includes most of the initial evaluation panel
        required_tests = set([test.lower() for test in self.LAB_PANELS["initial_pcos_evaluation"]["tests"]])
        
        for lab_set in previous_labs:
            completed_tests = set([test['name'].lower() for test in lab_set.get('tests', [])])
            # If at least 70% of required tests are present, consider it comprehensive
            if len(required_tests.intersection(completed_tests)) / len(required_tests) >= 0.7:
                # Check if tests are recent (within 1 year)
                lab_date = datetime.strptime(lab_set.get('date', '2000-01-01'), '%Y-%m-%d')
                if (datetime.now() - lab_date) < timedelta(days=365):
                    return True
        
        return False
    
    def _prioritize_labs(self, labs: List[Dict[str, Any]], patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sort and prioritize lab recommendations"""
        # Sort by priority (high, medium, low) and then by name
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(
            labs,
            key=lambda x: (priority_order.get(x.get('priority', 'low'), 2), x['name'])
        )
    
    def _generate_follow_up_instructions(self, labs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate instructions for follow-up based on recommended labs"""
        instructions = {
            "pre_test_preparation": [],
            "timing_considerations": [],
            "follow_up_schedule": []
        }
        
        # Check if any tests require fasting
        if any('fasting' in lab.get('notes', '').lower() for lab in labs):
            instructions["pre_test_preparation"].append(
                "Fast for 8-12 hours before testing (water is allowed). Schedule early morning appointments when possible."
            )
        
        # Check for menstrual cycle timing requirements
        if any('menstrual cycle' in lab.get('notes', '') for lab in labs):
            instructions["timing_considerations"].append(
                "Schedule hormone tests (LH, FSH, estradiol) on days 3-5 of your menstrual cycle. "
                "Progesterone should be tested on day 21 of a 28-day cycle."
            )
        
        # General follow-up schedule
        instructions["follow_up_schedule"].extend([
            "Schedule a follow-up appointment 1-2 weeks after completing lab tests to review results",
            "Bring copies of any previous lab results for comparison"
        ])
        
        # Add specific instructions for abnormal results
        instructions["follow_up_schedule"].append(
            "If any results are abnormal, additional testing or specialist referral may be recommended"
        )
        
        return instructions
