"""
FastAPI application entry point
"""

import logging
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request
from .routers import health, simulation
from ..exceptions import SimulationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Monte Carlo π Simulation API",
    description="Calculate π using Monte Carlo simulation via REST API",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(simulation.router)


# Middleware
# See also https://fastapi.tiangolo.com/advanced/middleware/
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware for logging: requests and responses
    Do not add try/except to middleware, let the exception handlers handle it.
    """
    start_time = time.perf_counter()
    logger.info("Request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    logger.info(
        "Response: %s %s - %d in %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )
    return response


# At some point, the number of error handlers may get too large for main.py.
# When that happens, create a new file called exception_handlers.py. Then do
# app.add_exception_handler(CustomError, custom_error_handler) in that file
# and import it here.

@app.exception_handler(SimulationError)
async def simulation_error_handler(request: Request, exc: SimulationError):
    """Handle SimulationError exceptions globally."""
    logger.exception(
        "Simulation error occurred: %s %s",
        request.method,
        request.url.path
    )  # Logs full traceback
    return JSONResponse(
        status_code=500,
        content={
            "error": "Simulation failed",
            # Error handling in FastAPI, see:
            # https://fastapi.tiangolo.com/tutorial/handling-errors/
            "detail": str(exc)
        }
    )
