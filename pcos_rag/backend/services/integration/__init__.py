"""
Integration services for external tools and APIs.

This package contains modules for integrating with various external services
like the ARC Institute's tools and other research resources.
"""

from .arc_integration import (
    ARCIntegrationService,
    arc_integration,
    get_arc_service
)

__all__ = [
    'ARCIntegrationService',
    'arc_integration',
    'get_arc_service'
]
