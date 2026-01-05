import sys
import time
from montecarlo_pi.simulation.pi_simulation import simulate_pi
from montecarlo_pi.simulation.chudnovsky import compute_pi
from montecarlo_pi.utilities.util import get_decimal_precision, get_decimal_difference

DEFAULT_RUNS = 10_000_000_000


def main():
    print("\nMonte Carlo π Simulation\n")
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RUNS
    start_time = time.time()
    pi_estimate = simulate_pi(runs)
    end_time = time.time()

    print(f"Estimated value of π: {pi_estimate}")
    pi_precision = get_decimal_precision(pi_estimate)
    computed_pi = compute_pi(pi_precision)
    print(f"precision (decimals): {pi_precision}")

    print(f"Chudnovsky π value:   {computed_pi}")

    pi_difference = get_decimal_difference(computed_pi, pi_estimate)
    print(f"Difference:           {pi_difference}")

    elapsed_time = end_time - start_time

    elapsed_time_formatted = 0
    if elapsed_time < 60:
        elapsed_time_formatted = f"{elapsed_time} seconds"
    else:
        elapsed_time_formatted = f"{elapsed_time / 60} minutes"

    print(f"Time elapsed:         {elapsed_time_formatted}")
    print("\n")
