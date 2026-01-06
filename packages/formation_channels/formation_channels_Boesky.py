import numpy as np
import h5py


def get_COMPAS_vars(compas_file, group, variables, mask=None):
    """Return a variable from the COMPAS output data

    Parameters
    ----------
    input_file : `hdf5 File`
        COMPAS file
    group : `str`
        Group within COMPAS file
    variables : `str` or `list`
        List of column names to access in group (or single column name)
    mask : `bool/array`
        Mask of binaries with same shape as each variable

    Returns
    -------
    var_list : `various`
        Single variable or list of variables (all masked)
    """
    var_list = None
    if isinstance(variables, str):
        var_list = compas_file[group][variables][...].squeeze()
        if mask is not None:
            var_list = var_list[mask]
    else:
        if mask is not None:
            var_list = [compas_file[group][var][...].squeeze()[mask]
                        for var in variables]
        else:
            var_list = [compas_file[group][var][...].squeeze()
                        for var in variables]

    return var_list



def identify_formation_channels(seeds, file):
    """Identify the formation channel that produced each seed. We consider 5
    main channels: classic, only stable, single core CEE, double core CEE and
    other. We define the channels as follows (the numbers are what is put in
    the ``channels`` output):

    Classic (1) -- In the first mass transfer, the primary overflows its
    Roche lobe stably and has a clear core-envelope structure (HG - TPAGB)
    whilst the secondary star is still on the main sequence. In the second mass
    transfer, the secondary overflows its Roche Lobe before stripping occurs
    and leads to a common envelope event.

    Only stable (2) -- As Classic, but the second mass transfer is stable.

    Single core CEE (3) -- In the first mass transfer, the primary overflows
    its Roche lobe unstably (leading to a CEE) and has a clear core-envelope
    structure (FGB - TPAGB) whilst the secondary star is still on the main
    sequence.

    Double core CEE (4) -- In the first mass transfer, the primary overflows
    its Roche lobe unstably (leading to a CEE) and both the primary and
    secondary have a clear core-envelope structure (FGB - TPAGB).

    Other (5) -- Anything else

    Parameters
    ----------
    seeds : `int/array`
        List of seeds that each correspond to a binary (this should be a subset
        of the seeds in the COMPAS output file)
    file : `hdf5 File`
        An open hdf5 file (returned by h5py.File) with the COMPAS output

    Returns
    -------
    channels : `int/array`
        List of channels through with each binary formed
    """
    all_rlof_seeds = get_COMPAS_vars(file, "BSE_RLOF", "SEED")
    rlof_mask = np.isin(all_rlof_seeds, seeds)
    rlof_seeds = all_rlof_seeds[rlof_mask]

    count, rlof_primary, rlof_secondary, cee_flag,\
        stellar_type_1, stellar_type_2 = get_COMPAS_vars(file,
                                                         "BSE_RLOF",
                                                         ["MT_Event_Counter",
                                                          "RLOF(1)>MT",
                                                          "RLOF(2)>MT",
                                                          "CEE>MT",
                                                          "Stellar_Type(1)<MT",
                                                          "Stellar_Type(2)<MT"],
                                                         rlof_mask)

    # CLASSIC channel
    # 1st transfer, stable RLOF from primary (post-MS, unstripped) onto MS
    classic_or_OS_MT1 = np.logical_and.reduce((count == 1,
                                               rlof_primary,
                                               np.logical_not(cee_flag),
                                               stellar_type_1 > 1,
                                               stellar_type_1 < 7,
                                               stellar_type_2 <= 1))
    # 2nd transfer, unstripped secondary RLOF into CE
    classic_MT2 = np.logical_and.reduce((count == 2,
                                         rlof_secondary,
                                         cee_flag,
                                         stellar_type_2 < 7))
    classic_seeds = np.intersect1d(rlof_seeds[classic_or_OS_MT1],
                                   rlof_seeds[classic_MT2])
    classic_mask = np.isin(seeds, classic_seeds)

    # ONLY STABLE channel
    # 1st transfer as classic, 2nd transfer unstripped secondary stable RLOF
    only_stable_MT2 = np.logical_and.reduce((count == 2,
                                             rlof_secondary,
                                             np.logical_not(cee_flag),
                                             stellar_type_2 < 7))
    only_stable_seeds = np.intersect1d(rlof_seeds[classic_or_OS_MT1],
                                       rlof_seeds[only_stable_MT2])
    only_stable_mask = np.isin(seeds, only_stable_seeds)

    # SINGLE CORE CEE channel
    # 1st transfer unstable, primary giant branch onto MS secondary
    single_core = np.logical_and.reduce((count == 1,
                                         rlof_primary,
                                         cee_flag,
                                         stellar_type_1 > 2,
                                         stellar_type_1 < 7,
                                         stellar_type_2 <= 1))
    single_core_mask = np.isin(seeds, rlof_seeds[single_core])

    # DOUBLE CORE CEE channel
    # 1st transfer unstable, primary giant branch onto giant branch secondary
    double_core = np.logical_and.reduce((count == 1,
                                         rlof_primary,
                                         cee_flag,
                                         stellar_type_1 > 2,
                                         stellar_type_1 < 7,
                                         stellar_type_2 > 2,
                                         stellar_type_2 < 7))
    double_core_mask = np.isin(seeds, rlof_seeds[double_core])
    

    #####################################################
    ####################### extra channels   ##########
    #####################################################

    all_cee_seeds = get_COMPAS_vars(file, 'BSE_Common_Envelopes', "SEED") 
    ##  case A MT1 channel & CE 

    # "flagRLOF1" is broken for case A mass transfer 
    classic_caseA_MT1 = np.logical_and.reduce((count == 1,
                                               np.logical_not(cee_flag),
                                               stellar_type_1 == 1,
                                               stellar_type_2 == 1))

    ####################################################
    ## only stable case A MT1 channel 
    # 1st transfer as classic case A, 2nd transfer unstripped secondary stable RLOF
    only_stable_caseA_seeds = rlof_seeds[classic_caseA_MT1] 
    # np.isin(rlof_seeds[classic_caseA_MT1],
                                   # all_cee_seeds, invert=True)
    only_stable_caseA_mask = np.isin(seeds, only_stable_caseA_seeds)

    # check if there is a CE, and overwrite these 
    # 2nd transfer, unstripped secondary RLOF into CE
    classic_caseA_seeds = np.isin(rlof_seeds[classic_caseA_MT1],
                                   all_cee_seeds)
    classic_caseA_mask = np.isin(seeds, classic_caseA_seeds)
    

    channels = np.zeros_like(seeds).astype(int)
    channels[classic_mask] = 1
    channels[only_stable_mask] = 2
    channels[single_core_mask] = 3
    channels[double_core_mask] = 4
    channels[classic_caseA_mask] = 1 # classify case A same as original channel
    channels[only_stable_caseA_mask] = 2 #  # classify case A same as original channel


    other_channel_mask_CE = np.in1d(seeds, all_cee_seeds)
    
    # within the other channel, assign other without CE  as -2
    mask_other_without_CE = (channels==0) & (other_channel_mask_CE==0)
    channels[mask_other_without_CE] = -2

    # within the other channel, assign other with CE  as -1
    mask_other_with_CE = (channels==0) & (other_channel_mask_CE==1)
    channels[mask_other_with_CE] = -1 


    return channels