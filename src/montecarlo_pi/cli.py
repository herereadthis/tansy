"""
Main CLI for Monte Carlo π Simulation
"""

import argparse
import os
import logging
from montecarlo_pi.simulation.pi_simulation import simulate_pi
from montecarlo_pi.simulation.chudnovsky import compute_pi
import montecarlo_pi.utilities.util as util

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

    with util.timer() as t:
        pi_estimate = simulate_pi(args.runs)

    pi_precision = util.get_decimal_precision(pi_estimate)
    computed_pi = compute_pi(pi_precision)
    accuracy = util.get_accuracy(computed_pi, pi_estimate)
    readable_time = util.get_readable_time_diff(0, t['seconds'])

    logger.info(f"Estimated value of π: {pi_estimate}")
    logger.info(f"Chudnovsky π value:   {computed_pi}")
    logger.info(f"Accuracy:             {accuracy} decimal {format('place' if accuracy == 1 else 'places')}")
    logger.info(f"Time elapsed:         {readable_time}")
    logger.info("\n")

    return pi_estimate

"""
Future work, signal handling

import signal
import sys

def signal_handler(signum, frame):
    print("Received signal, shutting down gracefully...")
    sys.exit(0)

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)  # K8s sends SIGTERM
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    
# ... rest of your argparse code
"""
