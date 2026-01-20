"""
Simulation endpoints
"""

import os
import json
import logging
from fastapi import APIRouter, Query
from fastapi.responses import Response
from montecarlo_pi.simulation.service import run_simulation
# Use BaseModel to validate request bodies
# from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(tags=["simulation"])


DEFAULT_RUNS = int(os.getenv('DEFAULT_RUNS', '1000000'))


@router.get("/simulate/pi")
async def simulate(
    sample_size: int = Query(
        default=DEFAULT_RUNS,
        gt=0,
        # ge=1000,
        # le=1_000_000_000,
        description="Number of random points (1k to 1B)"
    ),
    pretty: bool = False
):
    """Run Monte Carlo simulation to estimate π"""
    logger.info("Received simulation request: sample_size=%s", sample_size)
    result = run_simulation(sample_size)

    response_data = {
        "pi": float(result['pi']),
        "pi_estimate": float(result['pi_estimate']),
        "pi_rounded": float(result['pi_rounded']),
        "accuracy_decimal_places": result['accuracy'],
        "sample_size": result['sample_size'],
        "elapsed_seconds": result['elapsed_seconds']
    }

    result = response_data
    if pretty:
        result = Response(
            content=json.dumps(response_data, indent=4),
            media_type="application/json"
        )
    else:
        result = response_data
    logger.info(
        "Simulation completed successfully, accuracy: %s decimal places",
        response_data['accuracy_decimal_places']
    )
    return result
