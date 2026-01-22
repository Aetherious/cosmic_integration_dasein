# cosmic_integration/define_cosmo.py
import importlib
from typing import Union
from astropy import cosmology as cosmo

# Set the default cosmology to Planck18.
DEFAULT_COSMO = cosmo.Planck18

# Create COSMOLOGY default cache
# COSMOLOGY = [
#     DEFAULT_COSMO,
#     DEFAULT_COSMO.name()
# ]

# Define typings for cosmo
type_cosmo = Union[cosmo.FLRW, str, dict, None]

# Grab relevant cosmology dictionary from AstroPy library based on provided input.
def get_cosmology(provided_cosmo: type_cosmo) -> cosmo.FLRW:
    """
    Get an instance of a astropy.cosmology.FLRW subclass.

    Eg:
        define_cosmology.get_cosmology()
        define_cosmology.get_cosmology(astropy.cosmology.WMAP9)
        define_cosmology.get_cosmology("WMAP9")
        define_cosmology.get_cosmology(dict(H0=67.7, Om0=0.3, Ode0=0.7, w0=-1.0) --> wCDM
        define_cosmology.get_cosmology(dict(H0=67.7, Om0=0.3, Ode0=0.7) --> LambdaCDM


    Parameters
    ==========
    type_cosmo: cosmo.FLRW, str, dict, None
        Description of type_cosmo, one of:
            Instance of astropy.cosmology.FLRW subclass
            String with name of known Astropy cosmology, e.g., "Planck18"
            Dictionary with arguments required to instantiate the cosmology
            class.
            None - Use DEFAULT_COSMOLOGY
    """
    global COSMOLOGY

    if provided_cosmo is None:
        retrieved_cosmo = DEFAULT_COSMO

    # Instance of astropy.cosmology.FLRW subclass
    elif isinstance(provided_cosmo, cosmo.FLRW):
        retrieved_cosmo = provided_cosmo

    # String with name of known Astropy cosmology, e.g., "Planck18"
    elif isinstance(provided_cosmo, str):
        retrieved_cosmo = getattr(cosmo, provided_cosmo)

    # Set cosmology based on provided dictionary values.
    elif isinstance(provided_cosmo, dict):
        if 'Ode0' in provided_cosmo.keys():
            if 'w0' in provided_cosmo.keys():
                retrieved_cosmo = cosmo.wCDM(**provided_cosmo)
            else:
                retrieved_cosmo = cosmo.LambdaCDM(**provided_cosmo)
        else:
            retrieved_cosmo = cosmo.FlatLambdaCDM(**provided_cosmo)

    else:
        raise ValueError("Invalid format provided for cosmology.")

    # cache the cosmology
    # COSMOLOGY[0] = provided_cosmo
    # COSMOLOGY[1] = repr(provided_cosmo) if not provided_cosmo.name() else provided_cosmo.name()

    return retrieved_cosmo


# def set_cosmology(provided_cosmology: type_cosmo):
#     """

#     """
#     _set_default_cosmology()
#     if provided_cosmology is None:
#         cosmology = DEFAULT_COSMOLOGY

def set_cosmology(provided_cosmology="Planck18"):

    # Set cosmology using astropy, print a warning if TNG fit is used with Planck18 cosmology (since TNG uses Planck15)
    if provided_cosmology == "Planck18":
        print("USING PLANCK18 AS COSMOLOGY! If working with TNG fit, you may want to use Planck15 instead for self-consistency.")
    else:
        print("Using %s as cosmology!"%provided_cosmology)

    return getattr(importlib.import_module('astropy.cosmology'), provided_cosmology)
