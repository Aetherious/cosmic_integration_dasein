
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import astropy.units as u
from typing import Union, Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

import os
import glob
from collections import defaultdict
import pandas as pd



@dataclass
class DCOParameters:
    """Container for Double Compact Object parameters"""
    metallicities: np.ndarray
    delay_times: np.ndarray
    formation_efficiencies: np.ndarray
    dco_masses_1: np.ndarray
    dco_masses_2: np.ndarray
    primary_masses: np.ndarray
    secondary_masses: np.ndarray
    chirp_masses: np.ndarray
    mixture_weights: np.ndarray
    total_mass_evolved: float
    n_systems: int




def get_folder_path_convolution_output(catalog, author, dataset):
    """
    Get the full path to an HDF5 file where we want to save the SSPC convolution
    for a specific author and dataset.
    """
    if author not in catalog:
        raise ValueError(f"Author '{author}' not found in catalog")
    
    if dataset not in catalog[author]['paths']:
        raise ValueError(f"Dataset '{dataset}' not found for author '{author}'")
    
#     path = 

    return catalog[author]['paths'][dataset]



        
def get_file_path(catalog, author, dataset):
    """
    Get the full path to an HDF5 file for a specific author and dataset.
    """
    if author not in catalog:
        raise ValueError(f"Author '{author}' not found in catalog")
    
    if dataset not in catalog[author]['paths']:
        raise ValueError(f"Dataset '{dataset}' not found for author '{author}'")
    
    path = catalog[author]['paths'][dataset]
    file_name = catalog[author]['file_name']
    return os.path.join(path, file_name)

def list_authors(catalog):
    """Get list of all authors."""
    return list(catalog.keys())

def list_datasets(catalog, author):
    """Get list of all datasets for a specific author."""
    if author not in catalog:
        raise ValueError(f"Author '{author}' not found in catalog")
    return catalog[author]['datasets']
        

def print_catalog_summary(catalog):
    """Print a summary of the catalog structure."""
    print("GROWL Catalog Summary:")
    print("=" * 50)
    
    for author in sorted(catalog.keys()):
        print(f"\nAuthor: {author}")
        print(f"  File: {catalog[author]['file_name']}")
        print(f"  Datasets ({len(catalog[author]['datasets'])}):")
        for dataset in catalog[author]['datasets']:
            print(f"    - {dataset}")

        

def build_growl_catalog(base_path='/Volumes/GROWL/GROWL_bps_compact'):
    """
    Build a dictionary structure for GROWL catalog with authors and their datasets.
    
    Structure:
    {
        'author_name': {
            'datasets': ['dataset1', 'dataset2', ...],
            'file_name': 'COMPAS_Output_Weighted.h5',
            'paths': {
                'dataset1': '/Volumes/GROWL/GROWL_bps/Boesky24/alpha0_1beta0_25/',
                'dataset2': '/Volumes/GROWL/GROWL_bps/Boesky24/alpha0_1beta0_5/'
            }
            'labels':{'dataset1': r'$\alpha 0.1 \ \beta=0.25$',
                      'dataset2': r'$\alpha 0.1 \ \beta=0.5$'
            
            }
        }
    }
    """
    catalog = {}
    
    if not os.path.exists(base_path):
        print(f"Base path {base_path} does not exist")
        return catalog
    
    # Get all author directories
    author_dirs = [d for d in os.listdir(base_path) 
                  if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]
    
    for author in author_dirs:
        author_path = os.path.join(base_path, author)
        
        # Get all dataset directories for this author
        dataset_dirs = [d for d in os.listdir(author_path) 
                       if os.path.isdir(os.path.join(author_path, d)) and not d.startswith('.')]
        
        if not dataset_dirs:
            continue
            
        # Find the common HDF5 file name by checking the first dataset
        first_dataset_path = os.path.join(author_path, dataset_dirs[0])
        h5_files = glob.glob(os.path.join(first_dataset_path, '*.h5'))
        
        if not h5_files:
            print(f"Warning: No HDF5 files found in {first_dataset_path}")
            continue
            
        # Assume the first HDF5 file is the standard one
        file_name = os.path.basename(h5_files[0])
        
        # Build paths dictionary
        paths = {}
        for dataset in dataset_dirs:
            dataset_path = os.path.join(author_path, dataset)
            # Verify the HDF5 file exists in this dataset
            expected_file = os.path.join(dataset_path, file_name)
            if os.path.exists(expected_file):
                paths[dataset] = dataset_path + '/'
            else:
                print(f"Warning: {expected_file} not found")
        
        catalog[author] = {
            'datasets': sorted(dataset_dirs),
            'file_name': file_name,
            'paths': paths
        }
    
    return catalog
