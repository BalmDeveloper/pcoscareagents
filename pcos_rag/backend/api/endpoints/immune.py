"""
API endpoints for immune system analysis using Adaptive Biotechnologies platform.
Provides access to immune repertoire sequencing and analysis.
"""
import logging
from typing import List, Optional, Dict, Any, Tuple
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field, validator, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...services.immune.adaptive_biotech import adaptive_biotech_service
from ...config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/immune",
    tags=["immune"],
    responses={404: {"description": "Not found"}},
)

# Request/Response Models
class ImmuneRepertoireRequest(BaseModel):
    """Request model for immune repertoire analysis."""
    sample_ids: List[str] = Field(
        ...,
        min_items=1,
        description="List of sample IDs to analyze"
    )
    receptor_type: str = Field(
        "TCR",
        description="Type of immune receptor (TCR or BCR)",
        regex="^(TCR|BCR)$"
    )
    include_sequences: bool = Field(
        False,
        description="Whether to include full sequence data in the response"
    )

class ImmuneSignatureRequest(BaseModel):
    """Request model for immune signature analysis."""
    sequences: List[Dict[str, str]] = Field(
        ...,
        min_items=1,
        description="List of sequence records with 'sequence' and 'id' fields"
    )
    analysis_type: str = Field(
        "clonality",
        description="Type of analysis to perform (clonality, diversity, vj_usage, etc.)"
    )

class PCOSBiomarkersRequest(BaseModel):
    """Request model for PCOS biomarker analysis."""
    age_range: Optional[Tuple[int, int]] = Field(
        None,
        description="Optional age range filter as (min_age, max_age)"
    )
    pcos_subtype: Optional[str] = Field(
        None,
        description="Optional PCOS subtype filter"
    )

class ImmuneProfileComparisonRequest(BaseModel):
    """Request model for comparing immune profiles."""
    profile1: Dict[str, Any] = Field(
        ...,
        description="First immune profile"
    )
    profile2: Dict[str, Any] = Field(
        ...,
        description="Second immune profile"
    )
    comparison_metrics: Optional[List[str]] = Field(
        None,
        description="List of metrics to compare (None for all available)"
    )

# Endpoints
@router.post("/repertoire", response_model=Dict[str, Any])
async def get_immune_repertoire(
    request: ImmuneRepertoireRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve immune repertoire data for the specified samples.
    
    This endpoint provides access to T-cell or B-cell receptor sequencing data
    from the Adaptive Biotechnologies platform.
    
    Args:
        request: ImmuneRepertoireRequest containing sample IDs and parameters
        
    Returns:
        Dictionary containing immune repertoire data for each sample
    """
    try:
        logger.info(f"Fetching immune repertoire for {len(request.sample_ids)} samples")
        
        results = {}
        for sample_id in request.sample_ids:
            try:
                repertoire = await adaptive_biotech_service.get_immune_repertoire(
                    sample_id=sample_id,
                    receptor_type=request.receptor_type
                )
                
                # Optionally filter out sequence data to reduce payload size
                if not request.include_sequences and "sequences" in repertoire:
                    repertoire.pop("sequences", None)
                    repertoire["sequence_count"] = len(repertoire.get("sequences", []))
                
                results[sample_id] = repertoire
                
            except Exception as e:
                logger.error(f"Error processing sample {sample_id}: {str(e)}")
                results[sample_id] = {"error": str(e), "status": "error"}
        
        return {
            "status": "success",
            "receptor_type": request.receptor_type,
            "results": results,
            "metadata": {
                "samples_processed": len(results),
                "samples_with_errors": sum(1 for r in results.values() if "error" in r)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in get_immune_repertoire: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving immune repertoire: {str(e)}"
        )

@router.post("/analyze-signature", response_model=Dict[str, Any])
async def analyze_immune_signature(
    request: ImmuneSignatureRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze immune signature from sequence data.
    
    Performs various analyses on immune receptor sequences, including:
    - Clonality analysis
    - Diversity metrics
    - V(D)J gene usage
    - CDR3 length distribution
    
    Args:
        request: ImmuneSignatureRequest containing sequences and analysis type
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        logger.info(f"Analyzing immune signature for {len(request.sequences)} sequences")
        
        result = await adaptive_biotech_service.analyze_immune_signature(
            sequences=request.sequences,
            analysis_type=request.analysis_type
        )
        
        return {
            "status": "success",
            "analysis_type": request.analysis_type,
            "results": result,
            "metadata": {
                "sequences_analyzed": len(request.sequences),
                "analysis_timestamp": result.get("timestamp", "")
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in analyze_immune_signature: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in analyze_immune_signature: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing immune signature: {str(e)}"
        )

@router.get("/pcos-biomarkers", response_model=Dict[str, Any])
async def get_pcos_biomarkers(
    age_min: Optional[int] = Query(None, ge=0, le=120, description="Minimum age filter"),
    age_max: Optional[int] = Query(None, ge=0, le=120, description="Maximum age filter"),
    pcos_subtype: Optional[str] = Query(None, description="PCOS subtype filter"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieve known PCOS-related immune biomarkers.
    
    Provides information about immune markers that have been associated with PCOS,
    including T-cell and B-cell receptor signatures, cytokine profiles, and other
    immune-related biomarkers.
    
    Args:
        age_min: Optional minimum age filter
        age_max: Optional maximum age filter
        pcos_subtype: Optional PCOS subtype filter
        
    Returns:
        Dictionary containing PCOS biomarkers and their characteristics
    """
    try:
        logger.info("Fetching PCOS biomarkers")
        
        # Prepare age range if provided
        age_range = None
        if age_min is not None or age_max is not None:
            age_range = (age_min or 0, age_max or 120)
        
        biomarkers = await adaptive_biotech_service.get_pcos_biomarkers(
            age_range=age_range,
            pcos_subtype=pcos_subtype
        )
        
        return {
            "status": "success",
            "biomarkers": biomarkers,
            "filters": {
                "age_range": age_range,
                "pcos_subtype": pcos_subtype
            },
            "metadata": {
                "biomarker_count": len(biomarkers.get("markers", [])),
                "last_updated": biomarkers.get("last_updated", "")
            }
        }
        
    except Exception as e:
        logger.error(f"Error in get_pcos_biomarkers: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving PCOS biomarkers: {str(e)}"
        )

@router.post("/compare-profiles", response_model=Dict[str, Any])
async def compare_immune_profiles(
    request: ImmuneProfileComparisonRequest,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Compare two immune profiles and identify significant differences.
    
    This endpoint compares various aspects of two immune profiles, including:
    - Clonality metrics
    - V/J gene usage patterns
    - CDR3 characteristics
    - Sample metadata
    
    Args:
        request: ImmuneProfileComparisonRequest containing the profiles to compare
        
    Returns:
        Dictionary containing comparison results and statistical significance
    """
    try:
        logger.info("Comparing immune profiles")
        
        comparison = await adaptive_biotech_service.compare_immune_profiles(
            profile1=request.profile1,
            profile2=request.profile2,
            comparison_metrics=request.comparison_metrics
        )
        
        return {
            "status": "success",
            "comparison": comparison,
            "metadata": {
                "metrics_compared": comparison.get("metrics_compared", []),
                "significant_differences": comparison.get("significant_differences", 0)
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in compare_immune_profiles: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error in compare_immune_profiles: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error comparing immune profiles: {str(e)}"
        )
