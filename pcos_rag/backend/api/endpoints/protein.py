"""
API endpoints for protein analysis and design using 310.ai platform.
Provides access to protein structure prediction, function analysis, and design.
"""
import logging
import base64
from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field, validator, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...services.protein.three_ten_ai import three_ten_ai_service
from ...config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/protein",
    tags=["protein"],
    responses={404: {"description": "Not found"}},
)

# Request/Response Models
class StructurePredictionRequest(BaseModel):
    """Request model for protein structure prediction."""
    sequence: str = Field(
        ...,
        min_length=10,
        description="Protein amino acid sequence"
    )
    method: str = Field(
        "alphafold2",
        description="Prediction method to use (alphafold2, rosettafold, etc.)"
    )
    include_confidence_scores: bool = Field(
        True,
        description="Whether to include confidence scores in the prediction"
    )

class ProteinFunctionRequest(BaseModel):
    """Request model for protein function analysis."""
    sequence: Optional[str] = Field(
        None,
        min_length=10,
        description="Protein amino acid sequence (alternative to pdb_data)"
    )
    pdb_data: Optional[str] = Field(
        None,
        description="PDB format string (alternative to sequence)"
    )
    analysis_types: List[str] = Field(
        ["domains", "binding_sites", "disorder"],
        description="List of analysis types to perform"
    )
    
    @validator('sequence', 'pdb_data')
    def check_sequence_or_pdb(cls, v, values):
        if not v and not values.get('pdb_data' if values.get('sequence') is None else 'sequence'):
            raise ValueError("Either sequence or pdb_data must be provided")
        return v

class ProteinDesignRequest(BaseModel):
    """Request model for protein design."""
    constraints: Dict[str, Any] = Field(
        ...,
        description="Dictionary of design constraints (e.g., secondary structure, binding sites)"
    )
    design_method: str = Field(
        "rfdiffusion",
        description="Design method to use (rfdiffusion, rosetta, etc.)"
    )
    num_designs: int = Field(
        1,
        ge=1,
        le=10,
        description="Number of alternative designs to generate"
    )

class ProteinVisualizationRequest(BaseModel):
    """Request model for protein visualization."""
    pdb_data: str = Field(
        ...,
        description="PDB format string or PDB ID"
    )
    style: str = Field(
        "cartoon",
        description="Visualization style (cartoon, stick, sphere, etc.)"
    )
    width: int = Field(
        800,
        ge=100,
        le=2000,
        description="Width of the visualization in pixels"
    )
    height: int = Field(
        600,
        ge=100,
        le=2000,
        description="Height of the visualization in pixels"
    )

class PPIPredictionRequest(BaseModel):
    """Request model for protein-protein interaction prediction."""
    sequence1: str = Field(
        ...,
        min_length=10,
        description="First protein sequence"
    )
    sequence2: str = Field(
        ...,
        min_length=10,
        description="Second protein sequence"
    )
    method: str = Field(
        "alphafold_multimer",
        description="Prediction method to use"
    )
    include_confidence_scores: bool = Field(
        True,
        description="Whether to include confidence scores in the prediction"
    )

# Endpoints
@router.post("/predict-structure", response_model=Dict[str, Any])
async def predict_protein_structure(
    request: StructurePredictionRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Predict the 3D structure of a protein from its amino acid sequence.
    
    Uses advanced deep learning models to predict the 3D structure of a protein
    from its primary sequence. Supports multiple prediction methods including
    AlphaFold2 and RoseTTAFold.
    
    Args:
        request: StructurePredictionRequest containing sequence and parameters
        
    Returns:
        Dictionary containing the predicted structure in PDB format and metadata
    """
    try:
        logger.info(f"Predicting structure for protein sequence (length: {len(request.sequence)})")
        
        result = await three_ten_ai_service.predict_structure(
            sequence=request.sequence,
            method=request.method,
            include_confidence_scores=request.include_confidence_scores
        )
        
        return {
            "status": "success",
            "prediction_id": result.get("prediction_id"),
            "sequence_length": len(request.sequence),
            "pdb_data": result.get("pdb_data"),
            "confidence_scores": result.get("confidence_scores") if request.include_confidence_scores else None,
            "metadata": {
                "method": request.method,
                "model_version": result.get("model_version", "unknown")
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in predict_protein_structure: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in predict_protein_structure: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting protein structure: {str(e)}"
        )

@router.post("/analyze-function", response_model=Dict[str, Any])
async def analyze_protein_function(
    request: ProteinFunctionRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze protein function from sequence or structure.
    
    Performs various functional analyses on protein sequences or structures,
    including domain prediction, binding site detection, and disorder prediction.
    
    Args:
        request: ProteinFunctionRequest containing sequence/PDB and analysis types
        
    Returns:
        Dictionary containing function analysis results
    """
    try:
        logger.info("Analyzing protein function")
        
        result = await three_ten_ai_service.analyze_protein_function(
            sequence=request.sequence,
            pdb_data=request.pdb_data,
            analysis_types=request.analysis_types
        )
        
        return {
            "status": "success",
            "analysis_types": request.analysis_types,
            "results": result,
            "metadata": {
                "sequence_length": len(request.sequence) if request.sequence else None,
                "analysis_timestamp": result.get("timestamp", "")
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in analyze_protein_function: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in analyze_protein_function: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing protein function: {str(e)}"
        )

@router.post("/design", response_model=Dict[str, Any])
async def design_protein(
    request: ProteinDesignRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Design a new protein based on specified constraints.
    
    Uses computational protein design methods to generate novel protein sequences
    that satisfy the provided constraints, such as desired secondary structure,
    binding sites, or stability requirements.
    
    Args:
        request: ProteinDesignRequest containing design constraints and parameters
        
    Returns:
        Dictionary containing the designed protein sequences and structures
    """
    try:
        logger.info(f"Designing protein with {len(request.constraints)} constraints")
        
        designs = []
        for i in range(request.num_designs):
            design = await three_ten_ai_service.design_protein(
                constraints=request.constraints,
                design_method=request.design_method
            )
            designs.append({
                "sequence": design.get("sequence"),
                "pdb_data": design.get("pdb_data"),
                "score": design.get("score"),
                "design_id": design.get("design_id")
            })
        
        return {
            "status": "success",
            "num_designs": len(designs),
            "designs": designs,
            "metadata": {
                "design_method": request.design_method,
                "constraints_used": list(request.constraints.keys())
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in design_protein: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in design_protein: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error designing protein: {str(e)}"
        )

@router.post("/visualize", response_model=Dict[str, Any])
async def visualize_protein(
    request: ProteinVisualizationRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate a 3D visualization of a protein structure.
    
    Creates an interactive 3D visualization of a protein structure that can be
    embedded in a web interface. Supports different visualization styles and
    customization options.
    
    Args:
        request: ProteinVisualizationRequest containing PDB data and display options
        
    Returns:
        Dictionary containing HTML/JavaScript for the 3D visualization
    """
    try:
        logger.info("Generating protein visualization")
        
        html_content = await three_ten_ai_service.visualize_structure(
            pdb_data=request.pdb_data,
            style=request.style,
            width=request.width,
            height=request.height
        )
        
        # Encode the HTML content for safe JSON serialization
        encoded_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        
        return {
            "status": "success",
            "visualization": {
                "html": encoded_html,
                "format": "base64_encoded_html",
                "width": request.width,
                "height": request.height,
                "style": request.style
            },
            "metadata": {
                "pdb_data_length": len(request.pdb_data),
                "visualization_type": "3dmol.js"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in visualize_protein: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating protein visualization: {str(e)}"
        )

@router.post("/predict-ppi", response_model=Dict[str, Any])
async def predict_protein_protein_interaction(
    request: PPIPredictionRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Predict protein-protein interaction and binding interface.
    
    Uses advanced deep learning models to predict whether two proteins interact
    and the structure of their complex if they do. Provides confidence scores
    and interface analysis.
    
    Args:
        request: PPIPredictionRequest containing the two protein sequences
        
    Returns:
        Dictionary containing interaction prediction results and complex structure
    """
    try:
        logger.info(f"Predicting interaction between two proteins (lengths: {len(request.sequence1)}, {len(request.sequence2)})")
        
        result = await three_ten_ai_service.predict_ppi(
            sequence1=request.sequence1,
            sequence2=request.sequence2,
            method=request.method
        )
        
        response = {
            "status": "success",
            "interaction_predicted": result.get("interaction_predicted", False),
            "confidence_score": result.get("confidence_score") if request.include_confidence_scores else None,
            "metadata": {
                "method": request.method,
                "sequence1_length": len(request.sequence1),
                "sequence2_length": len(request.sequence2)
            }
        }
        
        # Include complex structure if available
        if "complex_pdb" in result:
            response["complex_structure"] = result["complex_pdb"]
        
        # Include interface analysis if available
        if "interface_analysis" in result:
            response["interface_analysis"] = result["interface_analysis"]
        
        return response
        
    except ValueError as ve:
        logger.error(f"Validation error in predict_protein_protein_interaction: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in predict_protein_protein_interaction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting protein-protein interaction: {str(e)}"
        )
