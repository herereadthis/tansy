"""
FastAPI application entry point
"""

from fastapi import FastAPI
from .routers import health

app = FastAPI(
    title="Monte Carlo π Simulation API",
    description="Calculate π using Monte Carlo simulation via REST API",
    version="1.0.0"
)

app.include_router(health.router)
