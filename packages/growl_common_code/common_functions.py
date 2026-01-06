import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as c
import astropy.units  as u
from typing import Union

def get_primary_secondary(
    m1: Union[float, np.ndarray, u.Quantity] = 0 * u.Msun,
    m2: Union[float, np.ndarray, u.Quantity] = 0 * u.Msun
):
    """
    Return (primary, secondary) where primary >= secondary element-wise.
    
    Parameters
    ----------
    m1, m2 : float, list, np.ndarray, or astropy.units.Quantity
        Component masses. Units are preserved; results always in Msun.
    
    Returns
    -------
    primary, secondary : Quantity
        More massive (primary) and less massive (secondary), in Msun.
    """
    # Convert to Quantity with units
    if not isinstance(m1, u.Quantity):
        m1 = np.asarray(m1) * u.Msun
    if not isinstance(m2, u.Quantity):
        m2 = np.asarray(m2) * u.Msun

    # Convert both to Msun
    m1 = m1.to(u.Msun)
    m2 = m2.to(u.Msun)

    primary = np.maximum(m1, m2)
    secondary = np.minimum(m1, m2)

    return primary, secondary


def chirp_mass(
    m1: Union[float, np.ndarray, u.Quantity] = 0 * u.Msun,
    m2: Union[float, np.ndarray, u.Quantity] = 0 * u.Msun
):
    """
    Compute the chirp mass given component masses m1 and m2.
    
    Parameters
    ----------
    m1, m2 : float, list, np.ndarray, or astropy.units.Quantity
        Component masses. Units are preserved; results always in Msun.
    
    Returns
    -------
    Mc : Quantity
        Chirp mass in Msun.
    """
    if not isinstance(m1, u.Quantity):
        m1 = np.asarray(m1, dtype=float) * u.Msun
    if not isinstance(m2, u.Quantity):
        m2 = np.asarray(m2, dtype=float) * u.Msun

    # Convert both to Msun
    m1 = m1.to(u.Msun)
    m2 = m2.to(u.Msun)

    mc = (m1 * m2) ** (3/5) / ((m1 + m2) ** (1/5))
    return mc.to(u.Msun)

