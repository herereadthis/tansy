"""
Simulation orchestration service
"""

from .pi_simulation import simulate_pi
from ..utilities import util
from ..utilities import constants
from ..exceptions import SimulationError
# from .chudnovsky import compute_pi

def run_simulation(sample_size):
    """
    Execute Monte Carlo simulation and calculate accuracy.
    """
    if sample_size <= 0:
        raise ValueError("Sample size must be a positive integer")
    
    try:
        with util.timer() as t:
            pi_estimate = simulate_pi(sample_size)
    except Exception as e:
        raise SimulationError("Simulation failed") from e

    pi_precision = util.get_decimal_precision(pi_estimate)
    # computed_pi = compute_pi(pi_precision)
    computed_pi = round(constants.PI, pi_precision)
    accuracy = util.get_accuracy(computed_pi, pi_estimate)

    return {
        'pi_estimate': pi_estimate,
        'sample_size': sample_size,
        # 'chudnovsky_pi=computed_pi,
        'pi': computed_pi,
        'accuracy': accuracy,
        'elapsed_seconds': t['seconds']
    }
