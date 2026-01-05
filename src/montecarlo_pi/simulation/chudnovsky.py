"""
I did not make this.
The Chudnovsky algorithm calculates pi to a high precision, efficiently.

The following was taken from:
"Generating Values Of Pi To A Specified Number Of Decimal Places"
by Joshua Salako
https://archive.is/Rrmjv
"""

# Import modules
import decimal

def compute_pi(n):
    """
    This function calculates the value of pi to 'n' number of decimal places
    Args:
    n:   precision(Decimal places)
    Returns:
    pi:   the value of pi to n-decimal places
    """

    decimal.getcontext().prec = n + 3
    decimal.getcontext().Emax = 999999999

    chudnovsky_constant = 426880 * decimal.Decimal(10005).sqrt()
    # K = decimal.Decimal(6)
    multiplier_term = decimal.Decimal(1)
    exponential_term = decimal.Decimal(1)
    linear_sum = decimal.Decimal(13591409)
    series_sum = linear_sum

    # For better precision, we calculate to n+3 and truncate the last two digits
    for i in range(1, n+3):
        multiplier_term = decimal.Decimal(multiplier_term* ((1728*i*i*i)-(2592*i*i)+(1104*i)-120)/(i*i*i))
        linear_sum = decimal.Decimal(545140134+linear_sum)
        exponential_term = decimal.Decimal(-262537412640768000*exponential_term)
        series_sum += decimal.Decimal((multiplier_term*linear_sum) / exponential_term)

    return str(chudnovsky_constant/series_sum)[:-2] # Pi is C/series_sum
