from ..base_agent import PCOSAgent, AgentResponse
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class UploadLabsAgent(PCOSAgent):
    """Agent responsible for handling lab result uploads and processing"""
    
    # Common PCOS-related lab tests
    COMMON_PCOS_LABS = [
        'testosterone_total', 'testosterone_free', 'dheas', 'shbg',
        'fsh', 'lh', 'prolactin', 'tsh', 'fasting_glucose', 'fasting_insulin',
        'hba1c', 'lipid_panel', 'vitamin_d', 'amh'
    ]
    
    def __init__(self):
        super().__init__(
            name="Upload Labs Agent",
            description="Manages the upload and processing of lab results"
        )
        self.required_data = ['lab_results', 'patient_id']
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process uploaded lab results"""
        try:
            # Validate input
            if 'lab_results' not in input_data or not input_data['lab_results']:
                return AgentResponse(
                    success=False,
                    message="No lab results provided"
                )
            
            # Process each lab result
            processed_results = []
            missing_required = []
            
            for lab in input_data['lab_results']:
                processed = self._process_single_lab(lab)
                processed_results.append(processed)
                
                # Check for missing critical labs
                if processed.get('status') == 'missing_required':
                    missing_required.append(processed['test_name'])
            
            # Generate summary
            summary = self._generate_summary(processed_results)
            
            # Determine next steps
            next_steps = ["identify_phenotype"]
            if missing_required:
                next_steps.append("recommend_labs")
            
            return AgentResponse(
                success=True,
                message="Lab results processed successfully",
                data={
                    "processed_results": processed_results,
                    "summary": summary,
                    "missing_required_labs": missing_required
                },
                next_steps=next_steps
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Error processing lab results: {str(e)}"
            )
    
    def _process_single_lab(self, lab_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single lab result"""
        test_name = lab_data.get('test_name', '').lower()
        
        # Basic validation
        if not all(k in lab_data for k in ['test_name', 'value', 'unit', 'reference_range']):
            return {
                "status": "error",
                "test_name": test_name,
                "message": "Incomplete lab data"
            }
        
        # Check if test is in our known PCOS labs
        is_pcos_related = test_name in [t.lower() for t in self.COMMON_PCOS_LABS]
        
        # Parse and validate the value
        try:
            value = float(lab_data['value'])
            ref_low, ref_high = map(float, lab_data['reference_range'].split('-'))
            
            # Determine if value is abnormal
            status = "normal"
            if value < ref_low:
                status = "low"
            elif value > ref_high:
                status = "high"
                
            # Special handling for specific tests
            interpretation = self._interpret_lab_result(test_name, value, status)
            
            return {
                "status": status,
                "test_name": test_name,
                "value": value,
                "unit": lab_data['unit'],
                "reference_range": lab_data['reference_range'],
                "is_pcos_related": is_pcos_related,
                "interpretation": interpretation,
                "timestamp": lab_data.get('date', datetime.now().isoformat())
            }
            
        except (ValueError, AttributeError) as e:
            return {
                "status": "error",
                "test_name": test_name,
                "message": f"Invalid lab data format: {str(e)}"
            }
    
    def _interpret_lab_result(self, test_name: str, value: float, status: str) -> str:
        """Provide interpretation for specific lab results"""
        interpretations = {
            'testosterone_total': {
                'high': 'Elevated testosterone may indicate hyperandrogenism, common in PCOS.',
                'normal': 'Testosterone levels within normal range.',
                'low': 'Low testosterone levels, may need further evaluation.'
            },
            'fasting_insulin': {
                'high': 'Elevated insulin levels may indicate insulin resistance, common in PCOS.',
                'normal': 'Insulin levels within normal range.',
                'low': 'Low insulin levels, may not indicate insulin resistance.'
            },
            'hba1c': {
                'high': 'Elevated HbA1c may indicate prediabetes or diabetes, monitor glucose metabolism.',
                'normal': 'HbA1c within normal range.',
                'low': 'Low HbA1c may indicate hypoglycemia or other conditions.'
            },
            'lh': {
                'high': 'Elevated LH with normal/low FSH may suggest PCOS (LH:FSH ratio > 2:1).',
                'normal': 'LH levels within normal range.',
                'low': 'Low LH levels, may indicate other endocrine issues.'
            }
        }
        
        # Default interpretation if test not in our dictionary
        if test_name not in interpretations:
            return f"{status.capitalize()} result. Consult with healthcare provider for interpretation."
            
        return interpretations[test_name].get(status, 'Result interpretation not available.')
    
    def _generate_summary(self, processed_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of all lab results"""
        abnormal_results = [r for r in processed_results if r.get('status') in ['high', 'low'] and r.get('is_pcos_related')]
        critical_abnormal = [r for r in abnormal_results if r.get('interpretation', '').lower().startswith('elevated')]
        
        return {
            "total_tests": len(processed_results),
            "abnormal_results": len(abnormal_results),
            "critical_abnormal": len(critical_abnormal),
            "pcos_related_tests": sum(1 for r in processed_results if r.get('is_pcos_related')),
            "needs_attention": len(abnormal_results) > 0
        }
