from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

class OBGYNAgent(PCOSAgent):
    """
    OBGYN Agent provides specialized gynecological care and support for PCOS patients.
    Focuses on menstrual health, fertility, and hormonal balance.
    """
    
    # Common PCOS symptoms and their potential management strategies
    SYMPTOM_MANAGEMENT = {
        "irregular_periods": {
            "description": "Irregular or absent menstrual cycles",
            "management": [
                "Hormonal birth control (pills, patch, ring, IUD)",
                "Progestin therapy",
                "Lifestyle modifications (diet, exercise, stress management)",
                "Inositol supplements",
                "Metformin (if insulin resistance is present)"
            ]
        },
        "heavy_bleeding": {
            "description": "Heavy or prolonged menstrual bleeding",
            "management": [
                "Hormonal birth control",
                "Nonsteroidal anti-inflammatory drugs (NSAIDs)",
                "Tranexamic acid",
                "Endometrial ablation (in severe cases)",
                "Hormonal IUD"
            ]
        },
        "pelvic_pain": {
            "description": "Pelvic pain or discomfort",
            "management": [
                "Over-the-counter pain relievers (ibuprofen, naproxen)",
                "Heat therapy",
                "Hormonal birth control",
                "Physical therapy",
                "Lifestyle modifications"
            ]
        },
        "hirsutism": {
            "description": "Excessive hair growth (face, chest, back)",
            "management": [
                "Hair removal methods (shaving, waxing, laser, electrolysis)",
                "Anti-androgen medications (spironolactone, flutamide)",
                "Topical eflornithine cream",
                "Hormonal birth control"
            ]
        },
        "acne": {
            "description": "Acne or oily skin",
            "management": [
                "Topical retinoids",
                "Antibacterial washes",
                "Oral antibiotics (for moderate to severe cases)",
                "Hormonal birth control",
                "Spironolactone"
            ]
        },
        "hair_loss": {
            "description": "Female pattern hair loss or thinning",
            "management": [
                "Minoxidil topical solution",
                "Spironolactone",
                "Low-level laser therapy",
                "Nutritional supplements (biotin, iron, zinc)",
                "Gentle hair care practices"
            ]
        }
    }
    
    # Fertility treatment options
    FERTILITY_TREATMENTS = {
        "lifestyle_modifications": {
            "description": "Weight management, diet, and exercise",
            "success_rate": "Varies, but can improve fertility in overweight/obese women with PCOS",
            "considerations": "First-line treatment, recommended for all women with PCOS who are overweight or obese"
        },
        "ovulation_induction": {
            "description": "Medications to stimulate ovulation",
            "options": [
                "Clomiphene citrate (Clomid, Serophene)",
                "Letrozole (Femara)",
                "Gonadotropins (injectable hormones)"
            ],
            "success_rate": "~20-60% pregnancy rate per cycle, depending on the medication and patient factors",
            "considerations": "Requires monitoring with ultrasound and blood work"
        },
        "metformin": {
            "description": "Insulin-sensitizing medication",
            "success_rate": "Modest improvement in ovulation and pregnancy rates, especially in women with insulin resistance",
            "considerations": "Often used in combination with other fertility treatments"
        },
        "intrauterine_insemination": {
            "description": "Placing washed sperm directly into the uterus",
            "success_rate": "~10-20% per cycle (higher when combined with ovulation induction)",
            "considerations": "Often used with ovulation induction medications"
        },
        "in_vitro_fertilization": {
            "description": "Fertilization of eggs with sperm in a lab, then transferring embryos to the uterus",
            "success_rate": "~30-50% per cycle in women with PCOS under 35",
            "considerations": "Higher risk of ovarian hyperstimulation syndrome (OHSS) in women with PCOS"
        },
        "ovarian_drilling": {
            "description": "Laparoscopic procedure to make small punctures in the ovary",
            "success_rate": "~30-50% pregnancy rate within 6-12 months",
            "considerations": "Second-line treatment, typically reserved for women who don't respond to medication"
        }
    }
    
    # Contraception options for women with PCOS
    CONTRACEPTION_OPTIONS = {
        "combined_hormonal": {
            "types": ["Pill", "Patch", "Vaginal ring"],
            "benefits": [
                "Regulates menstrual cycles",
                "Reduces androgen levels",
                "Improves acne and hirsutism",
                "Reduces risk of endometrial cancer"
            ],
            "risks": [
                "Increased risk of blood clots (especially in women with other risk factors)",
                "May worsen insulin resistance",
                "Not recommended for women over 35 who smoke"
            ]
        },
        "progestin_only": {
            "types": ["Mini-pill", "Implant", "Injection", "Hormonal IUD"],
            "benefits": [
                "Fewer side effects than combined methods",
                "Safe for women who can't use estrogen",
                "Hormonal IUD can reduce heavy bleeding"
            ],
            "risks": [
                "May cause irregular bleeding",
                "Some methods may worsen insulin resistance",
                "Weight gain possible with injection"
            ]
        },
        "non_hormonal": {
            "types": ["Copper IUD", "Barrier methods", "Fertility awareness"],
            "benefits": [
                "No hormonal side effects",
                "Copper IUD is highly effective and long-lasting",
                "No impact on future fertility"
            ],
            "risks": [
                "No improvement in PCOS symptoms",
                "Copper IUD may worsen menstrual cramps and bleeding",
                "Barrier methods have higher failure rates with typical use"
            ]
        }
    }
    
    def __init__(self):
        super().__init__(
            name="OBGYN Agent",
            description="Provides specialized gynecological care and support for PCOS patients"
        )
        self.required_data = [
            'age',
            'menstrual_history',
            'contraception_needs',
            'fertility_goals',
            'current_symptoms',
            'medical_history',
            'previous_treatments'
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process gynecological concerns and provide recommendations"""
        try:
            # Check for missing data
            missing_data = [field for field in self.required_data if field not in input_data]
            if missing_data:
                return AgentResponse(
                    success=False,
                    message=f"Missing required data for OBGYN recommendations: {', '.join(missing_data)}",
                    data={"missing_fields": missing_data}
                )
            
            # Generate personalized recommendations
            recommendations = self._generate_recommendations(input_data)
            
            # Generate next steps
            next_steps = ["dietician_agent", "fitness_agent"]
            if input_data.get('fertility_goals', {}).get('planning_pregnancy'):
                next_steps.append("fertility_specialist")
            
            return AgentResponse(
                success=True,
                message="OBGYN recommendations generated successfully",
                data=recommendations,
                next_steps=next_steps
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error generating OBGYN recommendations: {str(e)}"
            )
    
    def _generate_recommendations(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized OBGYN recommendations"""
        recommendations = {
            "menstrual_health": {},
            "contraception": {},
            "fertility": {},
            "symptom_management": {},
            "screening_recommendations": []
        }
        
        # Menstrual health recommendations
        recommendations["menstrual_health"] = self._assess_menstrual_health(input_data)
        
        # Contraception recommendations if needed
        if input_data.get('contraception_needs', {}).get('needs_contraception', False):
            recommendations["contraception"] = self._recommend_contraception(input_data)
        
        # Fertility recommendations if planning pregnancy
        if input_data.get('fertility_goals', {}).get('planning_pregnancy', False):
            recommendations["fertility"] = self._assess_fertility(input_data)
        
        # Symptom management
        recommendations["symptom_management"] = self._manage_symptoms(input_data)
        
        # Screening recommendations
        recommendations["screening_recommendations"] = self._get_screening_recommendations(input_data)
        
        return recommendations
    
    def _assess_menstrual_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess and make recommendations for menstrual health"""
        menstrual_history = input_data.get('menstrual_history', {})
        assessment = {
            "cycle_regularity": "",
            "concerns": [],
            "recommendations": []
        }
        
        # Evaluate cycle regularity
        cycle_length = menstrual_history.get('average_cycle_length')
        if cycle_length:
            if 21 <= cycle_length <= 35:
                assessment["cycle_regularity"] = "Regular"
            else:
                assessment["cycle_regularity"] = "Irregular"
                assessment["concerns"].append(f"Irregular cycle length ({cycle_length} days)")
        
        # Check for heavy bleeding
        if menstrual_history.get('heavy_bleeding', False):
            assessment["concerns"].append("Heavy menstrual bleeding")
            assessment["recommendations"].extend([
                "Consider iron supplementation if heavy bleeding continues",
                "NSAIDs can help reduce bleeding and cramping"
            ])
        
        # Check for absent periods
        if menstrual_history.get('absent_periods', False):
            assessment["concerns"].append("Absent periods (amenorrhea)")
            assessment["recommendations"].append("Hormonal therapy may be needed to induce periods")
        
        # General recommendations
        if not assessment["recommendations"] and assessment["cycle_regularity"] == "Regular":
            assessment["recommendations"].append("Your menstrual cycle appears to be within normal parameters.")
        
        return assessment
    
    def _recommend_contraception(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend appropriate contraception methods"""
        contraception_needs = input_data.get('contraception_needs', {})
        preferences = contraception_needs.get('preferences', {})
        
        recommendations = {
            "methods": [],
            "considerations": []
        }
        
        # Filter based on preferences and medical history
        if preferences.get('hormonal_ok', True):
            if not input_data.get('medical_history', {}).get('history_of_blood_clots', False):
                recommendations["methods"].append({
                    "type": "Combined hormonal methods",
                    "options": self.CONTRACEPTION_OPTIONS["combined_hormonal"]["types"],
                    "benefits": self.CONTRACEPTION_OPTIONS["combined_hormonal"]["benefits"],
                    "considerations": "Ideal for women who also want to manage PCOS symptoms"
                })
            
            recommendations["methods"].append({
                "type": "Progestin-only methods",
                "options": self.CONTRACEPTION_OPTIONS["progestin_only"]["types"],
                "benefits": self.CONTRACEPTION_OPTIONS["progestin_only"]["benefits"],
                "considerations": "Good option for women who cannot take estrogen"
            })
        
        # Always include non-hormonal options
        recommendations["methods"].append({
            "type": "Non-hormonal methods",
            "options": self.CONTRACEPTION_OPTIONS["non_hormonal"]["types"],
            "benefits": self.CONTRACEPTION_OPTIONS["non_hormonal"]["benefits"],
            "considerations": "No impact on PCOS symptoms but no hormonal side effects"
        })
        
        # Add general considerations
        recommendations["considerations"].extend([
            "The most effective method is the one you'll use consistently and correctly",
            "Consider your future fertility plans when choosing a method",
            "Discuss any concerns about side effects with your healthcare provider"
        ])
        
        return recommendations
    
    def _assess_fertility(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess fertility and provide recommendations"""
        fertility_goals = input_data.get('fertility_goals', {})
        time_trying = fertility_goals.get('months_trying_to_conceive', 0)
        
        assessment = {
            "fertility_status": "",
            "recommendations": [],
            "treatment_options": []
        }
        
        # Basic fertility assessment
        if time_trying < 6:
            assessment["fertility_status"] = "Early stage of trying to conceive"
            assessment["recommendations"].extend([
                "Track ovulation using basal body temperature or ovulation predictor kits",
                "Have regular, unprotected intercourse during your fertile window",
                "Consider preconception counseling if you have concerns"
            ])
        elif 6 <= time_trying < 12:
            assessment["fertility_status"] = "Moderate duration of trying to conceive"
            assessment["recommendations"].append("Consider a basic fertility evaluation")
        else:
            assessment["fertility_status"] = "Prolonged time trying to conceive"
            assessment["recommendations"].append("Recommend formal fertility evaluation")
        
        # Add PCOS-specific fertility considerations
        assessment["recommendations"].extend([
            "Weight management can improve fertility in women with PCOS",
            "Ovulation induction is often first-line treatment for anovulatory PCOS",
            "Consider seeing a reproductive endocrinologist if not pregnant within 6 months of trying"
        ])
        
        # Add treatment options
        assessment["treatment_options"] = [
            {
                "name": "Lifestyle Modifications",
                "description": self.FERTILITY_TREATMENTS["lifestyle_modifications"]["description"],
                "success_rate": self.FERTILITY_TREATMENTS["lifestyle_modifications"]["success_rate"]
            },
            {
                "name": "Ovulation Induction",
                "description": self.FERTILITY_TREATMENTS["ovulation_induction"]["description"],
                "success_rate": self.FERTILITY_TREATMENTS["ovulation_induction"]["success_rate"]
            },
            {
                "name": "In Vitro Fertilization (IVF)",
                "description": self.FERTILITY_TREATMENTS["in_vitro_fertilization"]["description"],
                "success_rate": self.FERTILITY_TREATMENTS["in_vitro_fertilization"]["success_rate"]
            }
        ]
        
        return assessment
    
    def _manage_symptoms(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide symptom management recommendations"""
        current_symptoms = input_data.get('current_symptoms', {})
        management = {}
        
        for symptom, details in current_symptoms.items():
            if symptom in self.SYMPTOM_MANAGEMENT:
                management[symptom] = {
                    "description": self.SYMPTOM_MANAGEMENT[symptom]["description"],
                    "management_options": self.SYMPTOM_MANAGEMENT[symptom]["management"],
                    "self_care_tips": self._get_self_care_tips(symptom)
                }
        
        return management
    
    def _get_self_care_tips(self, symptom: str) -> List[str]:
        """Get self-care tips for specific symptoms"""
        tips = {
            "irregular_periods": [
                "Maintain a healthy weight",
                "Exercise regularly but avoid excessive exercise",
                "Manage stress through relaxation techniques"
            ],
            "heavy_bleeding": [
                "Use a menstrual cup or period underwear for better management",
                "Stay hydrated",
                "Consider iron-rich foods or supplements"
            ],
            "pelvic_pain": [
                "Apply heat to the lower abdomen",
                "Practice relaxation techniques",
                "Try gentle stretching or yoga"
            ],
            "hirsutism": [
                "Consider hair removal methods that work for you",
                "Be gentle with your skin to prevent irritation",
                "Speak with a dermatologist about treatment options"
            ],
            "acne": [
                "Follow a gentle skincare routine",
                "Avoid picking or squeezing pimples",
                "Consider non-comedogenic makeup and skincare products"
            ],
            "hair_loss": [
                "Be gentle when brushing and styling hair",
                "Avoid tight hairstyles that pull on the hair",
                "Consider a volumizing shampoo and conditioner"
            ]
        }
        
        return tips.get(symptom, [
            "Maintain a healthy lifestyle with balanced nutrition and regular exercise",
            "Stay hydrated and get adequate sleep",
            "Manage stress through relaxation techniques"
        ])
    
    def _get_screening_recommendations(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommended health screenings"""
        age = input_data.get('age', 25)  # Default to 25 if age not provided
        screenings = []
        
        # Blood pressure screening
        screenings.append({
            "name": "Blood Pressure",
            "frequency": "Annually",
            "importance": "High blood pressure is more common in women with PCOS"
        })
        
        # Cholesterol and lipid profile
        screenings.append({
            "name": "Cholesterol/Lipid Profile",
            "frequency": "Every 1-3 years",
            "importance": "Women with PCOS are at higher risk for dyslipidemia"
        })
        
        # Diabetes screening
        if any([
            input_data.get('medical_history', {}).get('obesity', False),
            input_data.get('family_history', {}).get('diabetes', False),
            input_data.get('previous_glucose_intolerance', False)
        ]):
            screenings.append({
                "name": "Diabetes Screening (OGTT or A1C)",
                "frequency": "Every 1-3 years",
                "importance": "PCOS increases risk of insulin resistance and type 2 diabetes"
            })
        
        # Endometrial biopsy (if indicated)
        if input_data.get('menstrual_history', {}).get('irregular_periods', False) and \
           input_data.get('menstrual_history', {}).get('absent_periods', False) and \
           age >= 35:
            screenings.append({
                "name": "Endometrial Biopsy",
                "frequency": "As recommended by your doctor",
                "importance": "To rule out endometrial hyperplasia or cancer in women with prolonged amenorrhea"
            })
        
        # Depression and anxiety screening
        screenings.append({
            "name": "Mental Health Screening",
            "frequency": "Annually",
            "importance": "Higher rates of depression and anxiety in women with PCOS"
        })
        
        # Sleep apnea screening if symptomatic
        if input_data.get('symptoms', {}).get('daytime_sleepiness', False) or \
           input_data.get('symptoms', {}).get('loud_snoring', False):
            screenings.append({
                "name": "Sleep Apnea Screening",
                "frequency": "As needed",
                "importance": "Higher risk of sleep apnea in women with PCOS"
            })
        
        return screenings
