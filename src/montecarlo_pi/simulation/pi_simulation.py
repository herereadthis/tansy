"""
Simulate pi via Monte Carlo, with multiprocessing.
"""

from decimal import Decimal
import logging
from multiprocessing import Pool
import os
import random
import numpy as np

# there is no need to set config here, since it will inherit from the main CLI
logger = logging.getLogger(__name__)

# Chunk size for multiprocessing
# This value defines how many tasks are sent to each worker at a time
# Large chunk sizees use less CPU resources but may not finish evenly
# Small chunk sizes use more CPU resources but finish more evenly
CHUNK_SIZE = 3
# Split the runs into blocks to reduce memory usage
# Larger block sizes use more memory but run faster
# Smaller block sizes use less memory but taxe the CPU more
BLOCK_SIZE = 10_000

def get_pi_single(runs):
    """
    Simulates Pi using the most inefficient method possible.
    """
    inside_circle = 0
    outside_circle = 0

    count = 0

    while count < runs:
        x = random.random()
        y = random.random()

        distance = x**2 + y**2

        if distance <= 1:
            inside_circle += 1
        else:
            outside_circle += 1
        count += 1

    pi_estimate = 4 * inside_circle / runs
    return pi_estimate

# Using Numpy for vectorized operations is much faster
def get_inside_circle(runs):
    """
    Uses arrays to simulate pi
    """
    x = np.random.rand(runs)
    y = np.random.rand(runs)
    inside_circle = np.sum(x*x + y*y <= 1)
    # pi_estimate = 4 * inside_circle / runs
    return inside_circle

def get_inside_circle_blocked(runs, block_size = BLOCK_SIZE):
    """
    Uses arrays in blocks to simulate pi, which reduces memory usage.
    """
    inside_circle = 0
    for start in range(0, runs, block_size):
        size = min(block_size, runs - start)
        x = np.random.rand(size)
        y = np.random.rand(size)
        inside_circle += np.sum(x**2 + y**2 <= 1)
    return inside_circle

def get_split_runs(total_runs, cpu_count):
    """
    Splits the total number of runs into chunks for each CPU core.
    """
    logger.info(f"cpu count:            {cpu_count}")
    runs_per_process = [total_runs // cpu_count for cpu_index in range(cpu_count)]
    remainder = total_runs % cpu_count

    for i in range(remainder):
        runs_per_process[i] += 1

    return runs_per_process

def simulate_pi(runs):
    """
    Simulates pi using multiprocessing.
    """
    logger.info(f"Number of runs:       {runs}")

    cpu_count = os.process_cpu_count()
    runs_per_process = get_split_runs(runs, cpu_count)
    logger.info(f"runs per process:     {runs_per_process[0]}")
    # Uncomment to test error handling
    # foo = 0 / 0

    # Pool manages multiple processes
    # The following line tells how many processes to spawn
    with Pool(processes=cpu_count) as pool:
        results = pool.map(get_inside_circle_blocked, runs_per_process, chunksize=CHUNK_SIZE)

    inside_circle_total = sum(Decimal(int(r)) for r in results)
    total_runs = Decimal(runs)
    pi_estimate = Decimal(4) * inside_circle_total / total_runs

    return pi_estimate
