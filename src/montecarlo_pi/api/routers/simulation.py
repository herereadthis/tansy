"""
Simulation endpoints
"""

import os
import json
from fastapi import APIRouter, Query
from fastapi.responses import Response
from montecarlo_pi.simulation.service import run_simulation

router = APIRouter(tags=["simulation"])


DEFAULT_RUNS = int(os.getenv('DEFAULT_RUNS', '1000000'))


@router.get("/simulate/pi")
async def simulate(
    sample_size: int = Query(
        default=DEFAULT_RUNS,
        # ge=1000,
        # le=1_000_000_000,
        description="Number of random points (1k to 1B)"
    ),
    pretty: bool = False
):
    """Run Monte Carlo simulation to estimate π"""
    result = run_simulation(sample_size)

    response_data = {
        "pi_estimate": float(result['pi_estimate']),
        "sample_size": result['sample_size'],
        "pi": float(result['pi']),
        "accuracy_decimal_places": result['accuracy'],
        "elapsed_seconds": result['elapsed_seconds']
    }

    if pretty:
        return Response(
            content=json.dumps(response_data, indent=4),
            media_type="application/json"
        )
    return response_data
