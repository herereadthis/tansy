"""
Main CLI for Monte Carlo π Simulation
"""

import argparse
import os
import logging
from montecarlo_pi.simulation.service import run_simulation
from montecarlo_pi.utilities import util

DEFAULT_RUNS = int(os.getenv('DEFAULT_RUNS', '1000000000'))

# for logging examples, see:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    main CLI function
    """
    logger.info("Monte Carlo π Simulation")

    parser = argparse.ArgumentParser(description="Monte Carlo simulation to calculate pi")
    help_text = f"Number of simulation runs (default: {DEFAULT_RUNS})"
    parser.add_argument('runs',type=int, nargs='?', default=DEFAULT_RUNS, help=help_text)
    args = parser.parse_args()

    result = run_simulation(args.runs)
    readable_time = util.get_readable_time_diff(0, result['elapsed_seconds'])

    logger.info("Estimated value of π: %s", result['pi_estimate'])
    logger.info("Chudnovsky π value: %s", result['chudnovsky_pi'])
    logger.info(
        "Accuracy:             %s decimal %s",
        result['accuracy'],
        'place' if result['accuracy'] == 1 else 'places'
    )
    logger.info("Time elapsed: %s", readable_time)
    logger.info("\n")

    return result['pi_estimate']
