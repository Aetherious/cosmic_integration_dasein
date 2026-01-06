# from __future__ import division # in case this script is used in python 2 
import h5py as h5

import os
import numpy as np
import string



import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec


import matplotlib.gridspec as gridspec
# import matplotlib
import matplotlib.pyplot as plt
# for e.g., minor ticks 
from matplotlib.ticker import (FormatStrFormatter,
                               AutoMinorLocator)
#Set latex environment for plots/labels
import matplotlib
# matplotlib.rc('font', **{'family': 'sans-serif'})#, 'sans-serif': ['Helvetica']})
# matplotlib.rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath'])



from matplotlib.offsetbox import AnchoredText
from matplotlib import rc                                                                                                                                                                                                                    
from matplotlib import rcParams
import seaborn as sns

from astropy import units as u
from astropy import constants as const


from scipy.spatial.distance import cdist

# from KDEpy import FFTKDE
from scipy.stats import norm




## For SSPC use ##

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





## For SSPC use ##








rc('font', family='serif', weight = 'bold')
rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'
rc('axes', linewidth=2)

matplotlib.rcParams['xtick.major.size'] = 12
matplotlib.rcParams['ytick.major.size'] = 12
matplotlib.rcParams['xtick.minor.size'] = 8
matplotlib.rcParams['ytick.minor.size'] = 8
matplotlib.rcParams['font.weight']= 'bold'
matplotlib.rcParams.update({'font.weight': 'bold'})

fs = 24 # fontsize for plots
rc('axes', linewidth=2)





def layoutAxes(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, labelpad_x=None, labelpad_y=None,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5


    if labelpad:
        labelpad_x = labelpad
        labelpad_y = labelpad

    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')


    if labelSizeMajor==10:
        ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad_x)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad_y)#, fontweight='bold')    
    else:
        ax.set_xlabel(nameX, fontsize=labelSizeMajor,labelpad=labelpad_x)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=labelSizeMajor,labelpad=labelpad_y)#, fontweight='bold')  

    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 

    return ax



def layoutAxesNoXandYlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, labelpad_x=None, labelpad_y=None,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5
    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
    # ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    
    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())


    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 



    return ax


def layoutAxesNoXlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, rotation=90,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5
    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
    if labelSizeMajor==10:
        # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    else:
        # ax.set_xlabel(nameX, fontsize=labelSizeMajor,labelpad=labelpad)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=labelSizeMajor,labelpad=labelpad)#, fontweight='bold')     


    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 


    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    return ax






def layoutAxesNoYlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, rotation=0,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5


    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        # for tick in ax.yaxis.get_major_ticks():
        #     tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        # for tick in ax.yaxis.get_major_ticks():
        #     tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad, rotation=rotation)#,fontweight='bold')
    # ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    
    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

     # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 



    return ax



bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.75) # for box around text in plot






zorderlist = { 'stable B':10, 'stable B no CEE':13, \
                    'case B immediate CE':12,'stable C':15,\
                    r'case C immediate CE':17, 
                    'stable A':14, \
                 r'double-core CE':11, 'other':16\
                 }








dictChannelsBHNSListBolt_temp = [r'\textbf{(I) Classic}', r'\textbf{(X) Classic: case A}', r'\textbf{(IIb) OSMT: case A as first mass transfer}',\
                            r'\textbf{(II) Only stable mass transfer (OSMT)}',\
                            r'\textbf{(III) Single-core CE as first mass transfer}',\
                             r'\textbf{(IV) Double-core CE as first mass transfer}', r'\textbf{(V) Other}']
temp_list = [ 'classic',  'vi','vii', 'stable B no CEE', 'immediate CE', r'double-core CE',  'other']
dictChannelsBHNSListBolt =  {temp_list[i]: dictChannelsBHNSListBolt_temp[i] for i in range(7)}



channelColorDict = {'classic':'#118AB2', 'stable B no CEE':'orange',  'immediate CE': '#EF476F'  , r'double-core CE':'#073B4C', 'other':'gray', 'vi':'cyan', 'vii':'#FFD166'}
List_formationchannelOptions = ['All',  'classic',  'stable B no CEE',  'immediate CE',  r'double-core CE', 'vi', 'vii', 'other']
ind_formationchannelOptions = [7,  1, 2, 3, 4, 5, 6, 0]
dictFormationChannelIndex =  {List_formationchannelOptions[i]: ind_formationchannelOptions[i] for i in range(len(List_formationchannelOptions))}
ind_number_values = int(len(ind_formationchannelOptions)*2)
headerDict_Z  = { 5:'channel VI',     6:'channel VII',    7:'All',     0:'channel V', 1:'channel I', 2:'channel II', 3:'channel III', 4:'channel IV'}    

headerDict_Z_rev = {'classic':'channel I', 'stable B no CEE':'channel II', 'vii':'channel VII',  'immediate CE':'channel III',  r'double-core CE':'channel IV', 'other':'channel V', 'vi':'channel VI'} #['I_classic', 'II_only_stable_MT', 'III_single_core_CE', 'IV_double_core_CE', 'V_other']




dictChannelsBHNSList = ['classic', \
                      'stable B no CEE', \
                    'immediate CE',\
                 r'double-core CE', 'other']




zorderlist = { 'classic':10, 'stable B no CEE':13, \
                    'immediate CE':12,\
                 r'double-core CE':11, 'other':16\
                 }


# default settings for labels and names of BPS models 



DCOname_dict = {'BHNS':'BHNS', 'BBH':'BHBH', 'BNS':'NSNS'}
    


nModels=20 # 
BPSnameslist = list(string.ascii_uppercase)[0:nModels]
modelDirList = ['fiducial', 'massTransferEfficiencyFixed_0_25', 'massTransferEfficiencyFixed_0_5', 'massTransferEfficiencyFixed_0_75', \
               'unstableCaseBB', 'unstableCaseBB','alpha0_1', 'alpha0_5', 'alpha2_0', 'alpha10', 'fiducial', 'rapid', 'maxNSmass2_0', 'maxNSmass3_0', 'noPISN',  'ccSNkick_100km_s', 'ccSNkick_30km_s', 'noBHkick', 'wolf_rayet_multiplier_0_1', 'wolf_rayet_multiplier_5']

alphabetDirDict =  {BPSnameslist[i]: modelDirList[i] for i in range(len(BPSnameslist))}
BPScolors       = sns.color_palette("husl", nModels)
colorDirDict =  {BPSnameslist[i]: BPScolors[i] for i in range(len(BPSnameslist))}


markershapes = ["*", "o", "v",  "p", "H", "^", ">", 'X', "+","<", 'x', "3","d","1", "|", "D", "P", "X", "+", "d"]
dictMarkerShape = {BPSnameslist[i]: markershapes[i] for i in range(len(BPSnameslist))}



# physicalNamesBPSmodels = [r'\textbf{fiducial}',\
#                            r'$\beta=0.25$', r'$\beta=0.5$',  r'$\beta=0.75$',r'\textbf{unstable case BB}',r'\textbf{unstable case BB + optimistic CE}',\
#                            r'$\alpha_{\rm{CE}}=0.1$', r'$\alpha_{\rm{CE}}=0.5$',  r'$\alpha_{\rm{CE}}=2$', r'$\alpha_{\rm{CE}}=10$', r'\textbf{optimistic CE}',\
#                           r'\textbf{rapid SN}', r'$\rm{max} \ m_{\rm{NS}}=2.0\,\rm{M}_{\odot}$', r'$\rm{max} \ m_{\rm{NS}}=3.0\,\rm{M}_{\odot}$',\
#                           r'\textbf{no PISN}', r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}=100\,\rm{km}\,\rm{s}^{-1}$',r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}=30\,\rm{km}\,\rm{s}^{-1}$',\
#                           r'\textbf{SN} '+ r'$v_{\rm{k,BH}}=0\,\rm{km}\,\rm{s}^{-1}$', r'$\rm{f}_{\rm{WR}} = 0.1$', r'$\rm{f}_{\rm{WR}} = 5$' ]



physicalNamesBPSmodels = [r'\textbf{fiducial}',\
                           r'$\beta=0.25$', r'$\beta=0.5$',  r'$\beta=0.75$',r'\textbf{unstable case BB}',r'\textbf{E + K}',\
                           r'$\alpha_{\rm{CE}}=0.1$', r'$\alpha_{\rm{CE}}=0.5$',  r'$\alpha_{\rm{CE}}=2$', r'$\alpha_{\rm{CE}}=10$', r'\textbf{optimistic CE}',\
                          r'\textbf{rapid SN}', r'$\rm{max} \ m_{\rm{NS}}=2.0\,\rm{M}_{\odot}$', r'$\rm{max} \ m_{\rm{NS}}=3.0\,\rm{M}_{\odot}$',\
                          r'\textbf{no PISN}', r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}=100\,\rm{km}\,\rm{s}^{-1}$',r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}=30\,\rm{km}\,\rm{s}^{-1}$',\
                          r'\textbf{SN} '+ r'$v_{\rm{k,BH}}=0\,\rm{km}\,\rm{s}^{-1}$', r'$\rm{f}_{\rm{WR}} = 0.1$', r'$\rm{f}_{\rm{WR}} = 5$' ]



DCOtypeColorsDict = {'BHNS':'#66c2a5', 'BHBH':'#8da0cb', 'BBH':'#8da0cb', 'NSNS':'#fc8d62', 'BNS':'#fc8d62'}


alphabetPhysicalNameDict =  {BPSnameslist[i]: physicalNamesBPSmodels[i] for i in range(len(BPSnameslist))}





physicalNamesBPSmodelsWithEnter = [r'\textbf{fiducial}',\
                           r'$\beta=0.25$', r'$\beta=0.5$',  r'$\beta=0.75$',r'\textbf{unstable}' + '\n'+ r'\textbf{case BB}',  r'\textbf{E + K}',\
                           r'$\alpha_{\rm{CE}}=0.1$', r'$\alpha_{\rm{CE}}=0.5$',  r'$\alpha_{\rm{CE}}=2$', r'$\alpha_{\rm{CE}}=10$',  r'\textbf{optimistic}' +'\n' + r'\textbf{CE}',\
                          r'\textbf{rapid SN}', r'$\rm{max} \ m_{\rm{NS}}$' +'\n' + r'$2.0\,\rm{M}_{\odot}$', r'$\rm{max} \ m_{\rm{NS}}$' +'\n' + r'$3.0\,\rm{M}_{\odot}$',\
                          r'\textbf{no PISN}', r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}$' +'\n' + r'$100\,\rm{km}\,\rm{s}^{-1}$',r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}$' +'\n' + r'$30\,\rm{km}\,\rm{s}^{-1}$',\
                          r'\textbf{SN} '+ r'$v_{\rm{k,BH}}$' +'\n' + r'$0\,\rm{km}\,\rm{s}^{-1}$' , r'$\rm{f}_{\rm{WR}} = 0.1$', r'$\rm{f}_{\rm{WR}} = 5$']

alphabetPhysicalNameDictWithEnter =  {BPSnameslist[i]: physicalNamesBPSmodelsWithEnter[i] for i in range(len(BPSnameslist))}




# physicalNamesBPSmodelsWithEnter = [r'\textbf{fiducial}',\
#                            r'$\beta=0.25$', r'$\beta=0.5$',  r'$\beta=0.75$',r'\textbf{unstable}' + '\n'+ r'\textbf{case BB}',\
#                            r'$\alpha_{\rm{CE}}=0.5$',  r'$\alpha_{\rm{CE}}=2$', r'\textbf{optimistic CE}',\
#                           r'\textbf{rapid SN}', r'$\rm{max} \ m_{\rm{NS}}$' +'\n' + r'$2.0\,\rm{M}_{\odot}$', r'$\rm{max} \ m_{\rm{NS}}$' +'\n' + r'$3.0\,\rm{M}_{\odot}$',\
#                           r'\textbf{no PISN}', r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}$' +'\n' + r'$100\,\rm{km}\,\rm{s}^{-1}$',r'\textbf{SN} '+ r'$\sigma_{\rm{rms}}^{\rm{1D}}$' +'\n' + r'$30\,\rm{km}\,\rm{s}^{-1}$',\
#                           r'\textbf{SN} '+ r'$v_{\rm{k,BH}}$' +'\n' + r'$0\,\rm{km}\,\rm{s}^{-1}$' , r'$\rm{f}_{\rm{WR}} = 0.1$', r'$\rm{f}_{\rm{WR}} = 5$']

# alphabetPhysicalNameDictWithEnter =  {BPSnameslist[i]: physicalNamesBPSmodelsWithEnter[i] for i in range(len(BPSnameslist))}



colorlist = [ '#118AB2', '#EF476F', '#FFD166', '#073B4C', 'gray']


GWTC_indexDict = {'Mass1':0, 'Mass2':1, 'Mtot':2, 'Mchirp':3, 'q':4}




def obtainDataSTROOPWAFEL(param, pathToDirectory):
    """returns for STROOPWAFEL (AIS) simulation the data of wanted variable
    combines the data from AIS_oratory and AIS_sampling 
    
    param = [xparam, fxparam] ,  are the name of the variable and hdf5 keyname where it is in
    e.g. param = ['M1', 'doubleCompactObjects'] (see also: print(list(f.keys())))
    pathToDirectory is pathname to Directory where AIS_oratory & AIS_sampling directories are
    """ 

    xparam, fxparam = param

    pathAIS = pathToDirectory +'/COMPASOutput.h5'    

    fAIS = h5.File(pathAIS)
      
        
    ##### get parameter from two directories and combine them ############
    xvalues         = fAIS[fxparam][xparam][...].squeeze()
    return   xvalues



def maskTargetDCOsSTROOPWAFEL(DCOtype, boolDCOmask, f, otherSelection, otherparam):
    """returns mask of DCOs of interest
    fxparam  is hdf5 keyname of file where variable for which you want to mask DCOs is in 
    DCOtype = 'BBH' / 'ALL' / 'BHNS' or 'BNS' 
    boolDCOmask = [Hubble, RLOF, Pessimistic] # boolean values whether to mask mergers in a HUbble time, 
    binaries that have RLOFSecondaryAfterCEE = True, and Pessimistic binaries (i.e. optimisticCEFlag == 0)
    pathToDirectory is pathname to Directory where _oratory & _sampling directories are
    """
    
    Hubble, RLOF, Pessimistic = boolDCOmask
    

 
    
    fDCO = f['doubleCompactObjects']
    
    
    
    
    # mask binaries of given DCO type
    if DCOtype == 'BNS':
        mask0 = ((fDCO['stellarType1'][...] == 13) & (fDCO['stellarType2'][...] == 13))
    elif (DCOtype == 'BHNS') | (DCOtype == 'NSBH'):
        mask0 = ((fDCO['stellarType1'][...] == 13) & (fDCO['stellarType2'][...] == 14)) | \
            ((fDCO['stellarType1'][...] == 14) & (fDCO['stellarType2'][...] == 13) )          
    elif DCOtype == 'BBH':
        mask0 = ((fDCO['stellarType1'][...] == 14) & (fDCO['stellarType2'][...] == 14))
    elif (DCOtype == 'all') | (DCOtype == 'ALL') :
        mask0 = ((fDCO['stellarType1'][...] == 14) | (fDCO['stellarType1'][...] == 13))
    else:
        print('error: DCO type not known')
        
    # Hubble mask
    if Hubble:
        mask1 = (fDCO['mergesInHubbleTimeFlag'][...]==True) 
    elif not Hubble:
        mask1 = (fDCO['mergesInHubbleTimeFlag'][...]==True) |  (fDCO['mergesInHubbleTimeFlag'][...]==False) 
    # RLOF mask
    if RLOF:
        mask2 = (fDCO['RLOFSecondaryAfterCEE'][...]==False)
    elif not RLOF:
        mask2 = (fDCO['RLOFSecondaryAfterCEE'][...]==False) | (fDCO['RLOFSecondaryAfterCEE'][...]==True)
    # Pessimistic mask :  if True mask systems that have optimistic CE flag ==1
    if Pessimistic:
        mask3 = np.logical_not(fDCO["optimisticCEFlag"][...] == 1)
    elif not Pessimistic:
        mask3 = np.logical_not(fDCO["optimisticCEFlag"][...] == 1) + \
        np.logical_not(fDCO["optimisticCEFlag"][...] == 0)   
    
    # combine the different masks and the oratory and refinement masks
    combinedmask = mask0 * mask1 * mask2 * mask3
    combinedmask = combinedmask.squeeze()
    if otherSelection =='UFD':
        KpcToKM = 3.086 * 10**(16) # kpc to km  
        MyrToYr = 1E6 # yrs
        YrToSec = 3.154 *1E7 #sec        
        UFD_epsilon = otherparam[0]
        UFD_Rvir = otherparam[1]
        Xbh1 = otherparam[2]
        Rns = otherparam[3]

        fSN = f['supernovae']
        seedsOfIntererst = fDCO['seed'][...].squeeze()
        seedsSN = fSN['randomSeed'][...].squeeze()
        bools = np.in1d(seedsSN, seedsOfIntererst)        
        
        tc  = fDCO['tc'][...].squeeze()
        vsys = fSN['systemicVelocity'][...].squeeze()[bools]
        vsysSN2 = vsys[1:][::2]
        traveldistance = tc * vsysSN2 *  MyrToYr * YrToSec
        radiusUFDgalaxy = UFD_epsilon * UFD_Rvir * KpcToKM
        maskCandidatesUFD = (traveldistance <= radiusUFDgalaxy) | ((vsysSN2 <= 44) & (tc * MyrToYr *YrToSec<= radiusUFDgalaxy)) 
        
        combinedmask = maskCandidatesUFD*combinedmask
    

    
    return combinedmask






def obtainweightsSTROOPWAFEL(pathToDirectory):
    """returns weights for all DCOs and all systems for STROOPWAFEL
    pathToDirectory is pathname to Directory where AIS_oratory & AIS_sampling directories are 
    """
    
    pathAIS = pathToDirectory +'/COMPASOutput.h5'   # '/home/floor/Data_Thesis/bdMC/Z0_002'

    fAIS = h5.File(pathAIS)


    ##### get the DCO and all system weights  ############
    DCOsweights          = fAIS['doubleCompactObjects']['weight'][...].squeeze()


    
    systemsweights          = fAIS['systems']['weight'][...].squeeze()

    
    
    return DCOsweights, systemsweights


def chirpmass(m1, m2):
    numer = (m1*m2)**(3./5)
    denom = (m1+m2)**(1./5)
    
    return numer/denom




def obtainM1BHandM2BHassymetric(m1, m2):
    m1bh, m2bh = np.zeros_like(m1), np.zeros_like(m1)
    maskm1heavier = ( m1 >= m2)
    maskm2heavier = (m1 < m2)
    
    m1bh[maskm1heavier] = m1[maskm1heavier] 
    m1bh[maskm2heavier] = m2[maskm2heavier]
    m2bh[maskm1heavier] = m2[maskm1heavier]
    m2bh[maskm2heavier] = m1[maskm2heavier]
    
    return m1bh, m2bh # m1bh has all the heaviest systems









def getMaskBHNS(m1bh, m2bh):
    # add later on the 2nd explodes first 
    
    maskBHNS = m1bh >= m2bh # we have a BH=NS

    
    return maskBHNS



def below3Msun(m1bh):
    # add later on the 2nd explodes first 
    
    maskBHNS = m1bh <= 3 # we have a BH=NS

    
    return maskBHNS







class gaussian_kde(object):
    """Representation of a kernel-density estimate using Gaussian kernels.

    Kernel density estimation is a way to estimate the probability density
    function (PDF) of a random variable in a non-parametric way.
    `gaussian_kde` works for both uni-variate and multi-variate data.   It
    includes automatic bandwidth determination.  The estimation works best for
    a unimodal distribution; bimodal or multi-modal distributions tend to be
    oversmoothed.

    Parameters
    ----------
    dataset : array_like
        Datapoints to estimate from. In case of univariate data this is a 1-D
        array, otherwise a 2-D array with shape (# of dims, # of data).
    bw_method : str, scalar or callable, optional
        The method used to calculate the estimator bandwidth.  This can be
        'scott', 'silverman', a scalar constant or a callable.  If a scalar,
        this will be used directly as `kde.factor`.  If a callable, it should
        take a `gaussian_kde` instance as only parameter and return a scalar.
        If None (default), 'scott' is used.  See Notes for more details.
    weights : array_like, shape (n, ), optional, default: None
        An array of weights, of the same shape as `x`.  Each value in `x`
        only contributes its associated weight towards the bin count
        (instead of 1).

    Attributes
    ----------
    dataset : ndarray
        The dataset with which `gaussian_kde` was initialized.
    d : int
        Number of dimensions.
    n : int
        Number of datapoints.
    neff : float
        Effective sample size using Kish's approximation.
    factor : float
        The bandwidth factor, obtained from `kde.covariance_factor`, with which
        the covariance matrix is multiplied.
    covariance : ndarray
        The covariance matrix of `dataset`, scaled by the calculated bandwidth
        (`kde.factor`).
    inv_cov : ndarray
        The inverse of `covariance`.

    Methods
    -------
    kde.evaluate(points) : ndarray
        Evaluate the estimated pdf on a provided set of points.
    kde(points) : ndarray
        Same as kde.evaluate(points)
    kde.pdf(points) : ndarray
        Alias for ``kde.evaluate(points)``.
    kde.set_bandwidth(bw_method='scott') : None
        Computes the bandwidth, i.e. the coefficient that multiplies the data
        covariance matrix to obtain the kernel covariance matrix.
        .. versionadded:: 0.11.0
    kde.covariance_factor : float
        Computes the coefficient (`kde.factor`) that multiplies the data
        covariance matrix to obtain the kernel covariance matrix.
        The default is `scotts_factor`.  A subclass can overwrite this method
        to provide a different method, or set it through a call to
        `kde.set_bandwidth`.

    Notes
    -----
    Bandwidth selection strongly influences the estimate obtained from the KDE
    (much more so than the actual shape of the kernel).  Bandwidth selection
    can be done by a "rule of thumb", by cross-validation, by "plug-in
    methods" or by other means; see [3]_, [4]_ for reviews.  `gaussian_kde`
    uses a rule of thumb, the default is Scott's Rule.

    Scott's Rule [1]_, implemented as `scotts_factor`, is::

        n**(-1./(d+4)),

    with ``n`` the number of data points and ``d`` the number of dimensions.
    Silverman's Rule [2]_, implemented as `silverman_factor`, is::

        (n * (d + 2) / 4.)**(-1. / (d + 4)).

    Good general descriptions of kernel density estimation can be found in [1]_
    and [2]_, the mathematics for this multi-dimensional implementation can be
    found in [1]_.

    References
    ----------
    .. [1] D.W. Scott, "Multivariate Density Estimation: Theory, Practice, and
           Visualization", John Wiley & Sons, New York, Chicester, 1992.
    .. [2] B.W. Silverman, "Density Estimation for Statistics and Data
           Analysis", Vol. 26, Monographs on Statistics and Applied Probability,
           Chapman and Hall, London, 1986.
    .. [3] B.A. Turlach, "Bandwidth Selection in Kernel Density Estimation: A
           Review", CORE and Institut de Statistique, Vol. 19, pp. 1-33, 1993.
    .. [4] D.M. Bashtannyk and R.J. Hyndman, "Bandwidth selection for kernel
           conditional density estimation", Computational Statistics & Data
           Analysis, Vol. 36, pp. 279-298, 2001.

    Examples
    --------
    Generate some random two-dimensional data:

    >>> from scipy import stats
    >>> def measure(n):
    >>>     "Measurement model, return two coupled measurements."
    >>>     m1 = np.random.normal(size=n)
    >>>     m2 = np.random.normal(scale=0.5, size=n)
    >>>     return m1+m2, m1-m2

    >>> m1, m2 = measure(2000)
    >>> xmin = m1.min()
    >>> xmax = m1.max()
    >>> ymin = m2.min()
    >>> ymax = m2.max()

    Perform a kernel density estimate on the data:

    >>> X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    >>> positions = np.vstack([X.ravel(), Y.ravel()])
    >>> values = np.vstack([m1, m2])
    >>> kernel = stats.gaussian_kde(values)
    >>> Z = np.reshape(kernel(positions).T, X.shape)

    Plot the results:

    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,
    ...           extent=[xmin, xmax, ymin, ymax])
    >>> ax.plot(m1, m2, 'k.', markersize=2)
    >>> ax.set_xlim([xmin, xmax])
    >>> ax.set_ylim([ymin, ymax])
    >>> plt.show()

    """
    def __init__(self, dataset, bw_method=None, weights=None):
        self.dataset = np.atleast_2d(dataset)
        if not self.dataset.size > 1:
            raise ValueError("`dataset` input should have multiple elements.")
        self.d, self.n = self.dataset.shape
            
        if weights is not None:
            self.weights = weights / np.sum(weights)
        else:
            self.weights = np.ones(self.n) / self.n
            
        # Compute the effective sample size 
        # http://surveyanalysis.org/wiki/Design_Effects_and_Effective_Sample_Size#Kish.27s_approximate_formula_for_computing_effective_sample_size
        self.neff = 1.0 / np.sum(self.weights ** 2)

        self.set_bandwidth(bw_method=bw_method)

    def evaluate(self, points):
        """Evaluate the estimated pdf on a set of points.

        Parameters
        ----------
        points : (# of dimensions, # of points)-array
            Alternatively, a (# of dimensions,) vector can be passed in and
            treated as a single point.

        Returns
        -------
        values : (# of points,)-array
            The values at each point.

        Raises
        ------
        ValueError : if the dimensionality of the input points is different than
                     the dimensionality of the KDE.

        """
        points = np.atleast_2d(points)

        d, m = points.shape
        if d != self.d:
            if d == 1 and m == self.d:
                # points was passed in as a row vector
                points = np.reshape(points, (self.d, 1))
                m = 1
            else:
                msg = "points have dimension %s, dataset has dimension %s" % (d,
                    self.d)
                raise ValueError(msg)

        # compute the normalised residuals
        chi2 = cdist(points.T, self.dataset.T, 'mahalanobis', VI=self.inv_cov) ** 2
        # compute the pdf
        result = np.sum(np.exp(-.5 * chi2) * self.weights, axis=1) / self._norm_factor

        return result

    __call__ = evaluate

    def scotts_factor(self):
        return np.power(self.neff, -1./(self.d+4))

    def silverman_factor(self):
        return np.power(self.neff*(self.d+2.0)/4.0, -1./(self.d+4))

    #  Default method to calculate bandwidth, can be overwritten by subclass
    covariance_factor = scotts_factor

    def set_bandwidth(self, bw_method=None):
        """Compute the estimator bandwidth with given method.

        The new bandwidth calculated after a call to `set_bandwidth` is used
        for subsequent evaluations of the estimated density.

        Parameters
        ----------
        bw_method : str, scalar or callable, optional
            The method used to calculate the estimator bandwidth.  This can be
            'scott', 'silverman', a scalar constant or a callable.  If a
            scalar, this will be used directly as `kde.factor`.  If a callable,
            it should take a `gaussian_kde` instance as only parameter and
            return a scalar.  If None (default), nothing happens; the current
            `kde.covariance_factor` method is kept.

        Notes
        -----
        .. versionadded:: 0.11

        Examples
        --------
        >>> x1 = np.array([-7, -5, 1, 4, 5.])
        >>> kde = stats.gaussian_kde(x1)
        >>> xs = np.linspace(-10, 10, num=50)
        >>> y1 = kde(xs)
        >>> kde.set_bandwidth(bw_method='silverman')
        >>> y2 = kde(xs)
        >>> kde.set_bandwidth(bw_method=kde.factor / 3.)
        >>> y3 = kde(xs)

        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111)
        >>> ax.plot(x1, np.ones(x1.shape) / (4. * x1.size), 'bo',
        ...         label='Data points (rescaled)')
        >>> ax.plot(xs, y1, label='Scott (default)')
        >>> ax.plot(xs, y2, label='Silverman')
        >>> ax.plot(xs, y3, label='Const (1/3 * Silverman)')
        >>> ax.legend()
        >>> plt.show()

        """
        if bw_method is None:
            pass
        elif bw_method == 'scott':
            self.covariance_factor = self.scotts_factor
        elif bw_method == 'silverman':
            self.covariance_factor = self.silverman_factor
        elif np.isscalar(bw_method): # and not isinstance(bw_method, string_types):
            self._bw_method = 'use constant'
            self.covariance_factor = lambda: bw_method
        elif callable(bw_method):
            self._bw_method = bw_method
            self.covariance_factor = lambda: self._bw_method(self)
        else:
            msg = "`bw_method` should be 'scott', 'silverman', a scalar " \
                  "or a callable."
            raise ValueError(msg)

        self._compute_covariance()

    def _compute_covariance(self):
        """Computes the covariance matrix for each Gaussian kernel using
        covariance_factor().
        """
        self.factor = self.covariance_factor()
        # Cache covariance and inverse covariance of the data
        if not hasattr(self, '_data_inv_cov'):
            # Compute the mean and residuals
            _mean = np.sum(self.weights * self.dataset, axis=1)
            _residual = (self.dataset - _mean[:, None])
            # Compute the biased covariance
            self._data_covariance = np.atleast_2d(np.dot(_residual * self.weights, _residual.T))
            # Correct for bias (http://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_covariance)
            self._data_covariance /= (1 - np.sum(self.weights ** 2))
            self._data_inv_cov = np.linalg.inv(self._data_covariance)

        self.covariance = self._data_covariance * self.factor**2
        self.inv_cov = self._data_inv_cov / self.factor**2
        self._norm_factor = np.sqrt(np.linalg.det(2*np.pi*self.covariance)) #* self.n

        
        

def lowess(x, y, f=2. / 3., iter=3):
    """lowess(x, y, f=2./3., iter=3) -> yest
    Lowess smoother: Robust locally weighted regression.
    The lowess function fits a nonparametric regression curve to a scatterplot.
    The arrays x and y contain an equal number of elements; each pair
    (x[i], y[i]) defines a data point in the scatterplot. The function returns
    the estimated (smooth) values of y.
    The smoothing span is given by f. A larger value for f will result in a
    smoother curve. The number of robustifying iterations is given by iter. The
    function will run faster with a smaller number of iterations.
    """
    n = len(x)
    r = int(ceil(f * n))
    h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)]
    w = np.clip(np.abs((x[:, None] - x[None, :]) / h), 0.0, 1.0)
    w = (1 - w ** 3) ** 3
    yest = np.zeros(n)
    delta = np.ones(n)
    for iteration in range(iter):
        for i in range(n):
            weights = delta * w[:, i]
            b = np.array([np.sum(weights * y), np.sum(weights * y * x)])
            A = np.array([[np.sum(weights), np.sum(weights * x)],
                          [np.sum(weights * x), np.sum(weights * x * x)]])
            beta = linalg.solve(A, b)
            yest[i] = beta[0] + beta[1] * x[i]

        residuals = y - yest
        s = np.median(np.abs(residuals))
        delta = np.clip(residuals / (6.0 * s), -1, 1)
        delta = (1 - delta ** 2) ** 2

    return yest




# EM ejecta functions:




def calculateRisco(m_bhtemp, Xefftemp):
    # this is prograde orbit
    # see also https://duetosymmetry.com/tool/kerr-isco-calculator/

    # everything in cgs
    c = 2.99792458E10 #[cm s-1] 
    G = 6.67259E-8   
    Msun = 1.99E33 # gr
    Rsun = 6.96E10 # cm     
    
    factorFront =   ((G*m_bhtemp)/c**2) #m_bhtemp #s
    
    Z1 = 1 + (1 - Xefftemp**2)**(1/3) * ((1 + Xefftemp)**(1/3) + (1 - Xefftemp)**(1/3) )
    Z2 = np.sqrt((3* Xefftemp**2 + Z1**2))
    
    Risco = factorFront * (3 + Z2 - np.sqrt((3-Z1)*(3+Z1 +2*Z2)))
    return Risco



def calculateEjectedMassMerger(m_ns, r_ns, m_bh, Xeff ):
 # from 1807.00011, Eq 4 
    # returns M_rem in solar masses 
    # input r and m in solar masses and R sun. Xeff in [0,1] (symmetric) 
    # RNS in km
    
    
    # everything in cgs
    c = 2.99792458E10 #[cm s-1] 
    G = 6.67259E-8   
    Msun = 1.99E33 # gr
    Rsun = 6.96E10 # cm         
    
    
    # convert to cgs
    r_ns  = r_ns*0.1*10**6 #np.asarray([1.E6]* len(m_ns)) # to cm
    m_ns_cgs = Msun * m_ns
    m_bh_cgs = Msun * m_bh
    
    
    alpha, beta, gamma, delta = 0.406, 0.139, 0.255, 1.761
    C_NS = G * m_ns_cgs / (r_ns * c**2)
    
    R_isco = calculateRisco(m_bh_cgs, Xeff)
    
    R_isco_norm  = R_isco / (m_bh_cgs * (G/c**2)) 
    
    Q = m_bh_cgs / m_ns_cgs
    
    eta = Q / (1 + Q)**2
    
    FirstTerm  = alpha*(1 - 2*C_NS) / eta**(1/3)
    SecondTerm = beta* R_isco_norm * C_NS / eta 
    
    A = np.asarray(FirstTerm - SecondTerm + gamma)
    B = np.zeros_like(m_ns_cgs)
    
    Mrem_model = np.maximum(A,B)**(delta)
    
    Mrem_model /= Msun # in solar masses 
    
    # and the true M remnant mass (not normalized and in solar masses =)
    Mrem_solar = Mrem_model * m_ns_cgs  
    return Mrem_solar # in [Msun]






def convert_a_to_P_circular(separation, M1, M2):
    """calculate Period from separation
    separation is separation (needs to be given in astropy units)
    M1 and M2 are masses of the binary
    
    """
    G = const.G # [gr cm s^2]
    

    mu = G*(M1+M2)
    period = 2*np.pi * np.sqrt(separation**3/mu)
    
    
    
    return period        


Arrays_minNSmassEjecta_labels = [r'$(R_{\rm{NS}},\chi_{\rm{BH}})=11.5,0$',\
                                 r'$(R_{\rm{NS}},\chi_{\rm{BH}})=13,0$',\
                                 r'$(R_{\rm{NS}},\chi_{\rm{BH}})=11.5,0.5$', \
                                 r'$(R_{\rm{NS}},\chi_{\rm{BH}})=13,0.5$']







# SFRD options : 
GSMFs = ['Panter et al. (2004) Single', 'Furlong et al. (2015) Single', 'Furlong et al. (2015) Double']
MZs   = [ 'Langer et al. (2006)'      , 'Langer et al. +offset (2006)', 'Ma et al. (2015)']
SFRs  = ['Madau et al. (2014)'         ,'Strolger et al. (2004)',     'Madau et al. (2017)']




# define list with names of the MSSFR variations :-) 
MSSFRnameslist = []
MSSFRnameslist.append('000') # add phenomenological 

for ind_GSMF, GSMF in enumerate(GSMFs):
    ind_y = ind_GSMF + 1
    for ind_MZ, MZ in enumerate(MZs):
        ind_z = ind_MZ +1
        for ind_SFR, SFR in enumerate(SFRs):
            ind_x = ind_SFR+1
            
            
            
            
        

            MSSFRnameslist.append('%s%s%s'%(ind_x, ind_y, ind_z))
# print(modelnameslistA)

DCOTypeList = ['BHBH', 'BHNS', 'NSNS']




# GW stuff


NSNSrate0 = [320-240,320+490] # Gpc-3 yr-1 from: https://arxiv.org/pdf/2001.01761.pdf
BHBHrate0 = [23.9-8.6,23.9+14.9] # Gpc-3 yr-1 from: https://arxiv.org/pdf/1811.12907.pdf
BHNSrate0 = [0,610] # Gpc-3 yr-1 from: https://arxiv.org/pdf/1811.12907.pdf 



NSNSrate0 = [250,2810] # Gpc-3 yr-1 from: https://arxiv.org/pdf/2001.01761.pdf
BHBHrate0 = [9.7,101] # Gpc-3 yr-1 from: https://arxiv.org/pdf/1811.12907.pdf
BHNSrate0 = [0,610] # Gpc-3 yr-1 from: https://arxiv.org/pdf/1811.12907.pdf 


from math import log10, floor
def round_to_1(x):
    """ round to one significant digit"""
    return round(x, -int(floor(log10(abs(x)))))

def round_to_2(x):
    """ round to one significant digit"""
    return round(x, -int(floor(log10(abs(x))))+1)

# from https://stackoverflow.com/questions/21844024/weighted-percentile-using-numpy

def roundAndFormat1(xxx):
    """ changes numbers xxx into string percentages that are nice integer numbers 
    it is a hack to make sure that numbers like 65.241 become 65, whereas numbers like 6.7 become 7
    so its basically rounding to the nearest integer number and then formatting it nicely for legend
    """
    st = '{:0.2}'.format(xxx) # round
    st = (round(float(st),0))
    st = str(st)
    st = ('%f' %float(st)).rstrip('0').rstrip('.') # format
    return str(st)

def roundAndFormat(xxx):
    st = '{:0.2}'.format(xxx) # round
    st = ('%f' %float(st)).rstrip('0').rstrip('.') # format
    return str(st)





def weighted_quantile(values, quantiles, sample_weight=None, 
                      values_sorted=False, old_style=False):
    """ Very close to numpy.percentile, but supports weights.
    NOTE: quantiles should be in [0, 1]!
    :param values: numpy.array with data
    :param quantiles: array-like with many quantiles needed
    :param sample_weight: array-like of the same length as `array`
    :param values_sorted: bool, if True, then will avoid sorting of
        initial array
    :param old_style: if True, will correct output to be consistent
        with numpy.percentile.
    :return: numpy.array with computed quantiles.
    """
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), \
        'quantiles should be in [0, 1]'

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)








# GW DATA 
# array with gravitational wave estimates from LIGO-Virgo public data
#name m1 m1_plus m1_minus m2 m2_plus m2_minus spin spin_plus spin_minus chirp chirp_plus chirp_minus, massratio massratio_plus massratio_minus
# FROM https://www.gw-openscience.org/catalog/GWTC-1-confident/html/
# CATALOG PAPER 
gw150914 = [35.6, 4.8, 3,        30.6, 3, 4.4,       -0.01, 0.12, 0.13,     28.6, 1.7, -1.5,            0,0,0]                     
gw151012 = [23.3, 14, 5.5,       13.6, 4.1, 4.8,      0.04, 0.28, 0.19,     15.2, 2.1, -1.2,            0,0,0]                     
gw151226 = [13.7, 8.8, 3.2,      7.7, 2.2, 2.6,       0.18, 0.2, 0.12,      8.9, 0.3, -0.3,             0,0,0]           
gw170104 = [31, 7.2, 5.6,        20.1, 4.9, 4.5,     -0.04, 0.17, 0.2,      21.4, 2.2, -1.8,            0,0,0]       
gw170608 = [10.9 ,5.3 ,1.7,      7.6, 1.3, 2.1,       0.03, 0.19, 0.07,     7.9, 0.2, -0.2,             0,0,0]       
gw170729 = [50.6, 16.6, 10.2,    34.3, 9.1, 10.1,     0.36, 0.2, 0,         35.4, 6.5, -4.8,            0,0,0]       
gw170809 = [35.2 ,8.3, 6 ,       23.8 ,5.2, 5.1,      0.07 ,0.16 ,0.16,     24.9, 2.1, -1.7,            0,0,0]    
gw170814 = [30.7 ,5.7, 3,        25.3, 2.9, 4.1,      0.07, 0.12, 0.11,     24.1, 1.4, -1.1,            0,0,0]   
gw170817 = [1.46 ,0.12 ,0.1,     1.27 ,0.09 ,0.09,    0 ,   0.02 ,0.01,     1.186, 0.001, -0.001,       0,0,0]    
gw170818 = [35.5 ,7.5 ,4.7,      26.8, 4.3 ,5.2,     -0.09, 0.18, 0,        26.5, 2.1, -1.7,            0,0,0]   
gw170823 = [39.6 ,10 ,6.6,       29.4, 6.3, 7.1,      0.08, 0.2, 0.22,      29.2, 4.6, -3.6,            0,0,0]


#mass ratio GW170817 from https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.119.161101 
qrange_gw170817 = [0.7,1]
Zrange_gw170817 = np.asarray([0.2, 1])*0.0142 #from https://arxiv.org/pdf/1710.05861.pdf

GWdata = [gw150914, gw151012, gw151226, gw170104,gw170608,gw170729 , gw170809, gw170814, gw170817, gw170818, gw170823]







def QinBHspinmodel(separationPreSN2, M1, M2, maskNSBH):
    # returns spins from Qin et al + 2018 model 
    
    # start with all zeseparationDCOFormationarationDCOFormationBH spins
    BHspins = np.zeros_like(separationPreSN2)
    
    # now add spins for NS-BH following Qin et al 2018:
    # this is based on the separation prior to the second SN  
    PeriodPreSN2 = convert_a_to_P_circular(separation=separationPreSN2*u.Rsun, M1=M1*u.Msun, M2=M2*u.Msun)
    PeriodPreSN2 = PeriodPreSN2.to(u.d).value # in days 
    
    # only do non zero spins
    # first mask super tight NSBH that will get spin 1
    maskNSBHChi1 = (np.log10(PeriodPreSN2) < -0.3) & (maskNSBH ==1)
    BHspins[maskNSBHChi1] = np.ones(np.sum(maskNSBHChi1)) # fill with ones
#     print('#total, = ', len(maskNSBHChi1))
#     print('# with Chi = 1, = ', np.sum(maskNSBHChi1))
    
    # now the variable spin
    maskNSBHChi_var = (np.log10(PeriodPreSN2) > -0.3) &  (np.log10(PeriodPreSN2) < 0.3)  &(maskNSBH ==1)
    m_, c_ = -5./3, 0.5 # from Qin + 2018 
    spins_var =  m_ * np.log10(PeriodPreSN2[maskNSBHChi_var])  + c_   
    BHspins[maskNSBHChi_var] = spins_var
#     print('# with Chi var = ', np.sum(maskNSBHChi_var))
    
    return BHspins











def convert_a_to_P_circular(separation, M1, M2):
    """calculate Period from separation
    separation is separation (needs to be given in astropy units)
    M1 and M2 are masses of the binary
    
    """
    G = const.G # [gr cm s^2]
    

    mu = G*(M1+M2)
    period = 2*np.pi * np.sqrt(separation**3/mu)
    
    
    
    return period








    
def getXmomentOfMT(Seeds, maxCounter=10):
    # from Neijssel + 19 
    #this function might become obsolete if we finetune the RLOF output
    #with help from idea Jim Barrett
    #to have a number for x-moment of RLOF

    #make seeds into 1D array and calculate difference, meaning everytime the next line
    #has same seed it will be zero else it will be more, except for the very first line.
    offsetIndices = np.diff(Seeds)
    #I dont care about the difference just that it is nonzero, make it all into 0-1s
    offsetIndices[offsetIndices>=1] = 1

    #Create am empty array to turn into a boolean slice, since the np.diff ommits
    #first line we add one to the length.
    indices       = np.zeros(len(offsetIndices)+1)
    indices[0]    = 1
    #Now an array with 0 and 1s where every one is the first line of a different seed.
    #This effectively is the first moment of mass transfer of the system.
    indices[1:]   = offsetIndices

    
    
    #so nr 1 is first moment,
    counter = 2
    while (0. in indices) and (counter <=maxCounter):
        #get indices
        indexFilled   = np.where(indices != 0)
        #add 1 essentially move one row down
        indexFilledTemp  = indexFilled[0] + 1
        #if not marked alreaydy i.e. in indexFilled 
        notMarked = np.logical_not(np.in1d(indexFilledTemp,indexFilled))
        #and if index not bigger than array
        notTooBig = indexFilledTemp < (len(indices) -1)
        #give me those indices
        indexFilledTemp = indexFilledTemp[notMarked & notTooBig]
        #and fill in the RLOF counter as anotehr moment of RLOF
        indices[np.array(indexFilledTemp,)] = counter
        counter+=1
    return indices







### OLD CODE FOR COLORS 

# DEFINE COLOR LIST 

# colorlist = ['', '', '' , '', '', '', '', '']
# colorlist[7] = 'gray'

# for nrC in range(7):
#     if (nrC>0) & (nrC<4):
#         cm       = plt.get_cmap('viridis_r')
#         indd = nrC +2

#     if (nrC>=4) & (nrC<=5):
#         cm       = plt.get_cmap('plasma_r')
#         indd = nrC
#     if nrC>5 or nrC==0:
#         cm       = plt.get_cmap('plasma_r')
#         if nrC==0:
#             indd=0 
#         else:
#             indd=1
   
        
#     #             cmapCustom = matplotlib.colors.LinearSegmentedColormap.from_list("", [   "white", cm[i]])    
#     mycolors = [cm(x) for x in np.linspace(0,1 , (7))] 
#     colorlist[nrC] = mycolors[indd]


# colorlist = ['', '', '' , '', '', '', '', '']
# colorlist[7] = 'gray'

# for nrC in range(7):
#     if (nrC>=0) & (nrC<=2):
#         cm       = plt.get_cmap('plasma_r')
#         indd = nrC

#         mycolors = [cm(x) for x in np.linspace(0,1 , (6))] 
#         colorlist[nrC] = mycolors[indd] 

#     if nrC==3:
#         colorlist[nrC]='red'


#     if (nrC>=4) & (nrC<=5):
#         cm       = plt.get_cmap('plasma_r')
#         indd = nrC-1
#         mycolors = [cm(x) for x in np.linspace(0,1 , (6))] 
#         colorlist[nrC] = mycolors[indd] 

#     if nrC==6:
#         colorlist[nrC]='green'


# colorlist = ['', '', '' , '', '', '', '', '']
# colorlist[7] = 'gray'

# for nrC in range(7):
#     if (nrC>=0) & (nrC<=3):
#         cm       = plt.get_cmap('plasma')
#         indd = nrC+1

#         mycolors = [cm(x) for x in np.linspace(0,1 , (5))] 
#         colorlist[nrC] = mycolors[indd] 

# #     if nrC==5:
# #         colorlist[nrC]='lightblue'


#     if (nrC>=4) & (nrC<=6):
#         cm       = plt.get_cmap('viridis_r')
#         indd = nrC-3
#         mycolors = [cm(x) for x in np.linspace(0,1 , (5))] 
#         colorlist[nrC] = mycolors[indd] 

#     if nrC==6:
#         colorlist[nrC]='green'
        



    # #             cmapCustom = matplotlib.colors.LinearSegmentedColormap.from_list("", [   "white", cm[i]])    
    # mycolors = [cm(x) for x in np.linspace(0,1 , (7))] 
    # colorlist[nrC] = mycolors[indd]

# colorlist = ['', '', '' , '', '', '', '', '']
# colorlist[7] = 'gray'




# own definitions
# colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 'gold'] # colours of channels 
# colorlist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 'deepskyblue', 'gold','#8c564b', 'gold'] # colours of channels 

# ChannelLabelList = ['channel 1','channel 2','channel 3','channel 4','channel 5','channel 6', 'channel 7' ]  # labels of channels  
# ChannelLabelListShort = ['1','2','3','4','1b','2b', '5' ] # shorter notation of ChannelLabelList




class COspin(object):
    """
    This class calculates the Black Hole (BH) or Neutron Star (NS) spin
    based on a given spin function/model 
    
    """
    
    
    def __init__(self, data_path=None, state='he_depletion'):
    
        self.path                = data_path
        if (self.path is None):
            print("Just to double check you create instance of ClassCOMPAS without path/Data")
        elif not  os.path.isfile(data_path):
            raise ValueError("h5 file not found. Wrong path given?", "path given = %s"%data_path)
        elif os.path.isfile(data_path):
            self.h5file           = h5.File(data_path)
            
            
        self.spin_model = None 
        self.whichweight = None 
        self.state = state 
    
        
    def convert_a_to_P_circular(separation, M1, M2):
        """calculate Period from separation
        separation is separation (needs to be given in astropy units)
        M1 and M2 are masses of the binary

        """

        period = 2*np.pi * np.sqrt(separation**3/(const.G*(M1+M2)))

        return period   
        
        
    def setCOMPASData(self):
        """ reads in some of the COMPAS parameters needed from hdf5 file """
        
        fDCO      = self.h5file['doubleCompactObjects'] # hdf5 file with the DCO information
        fSN       = self.h5file['supernovae']  # hdf5 file with the SN information
        #
        self.M1 = fDCO['M1'][...].squeeze()   # Compact object mass [Msun] of the initially more massive star
        self.M2 = fDCO['M2'][...].squeeze()  # Compact object mass [Msun] of the initially less massive star
        
        self.seedsDCO = fDCO['seed'][...].squeeze()  # get the seeds in the DCO file 
        self.seedsSN = fSN['randomSeed'][...].squeeze()    # get the seeds in the SN file 
        indices = np.sort(np.unique(self.seedsSN[1::2], return_index=True)[1])
        maskSNdco = np.in1d(self.seedsSN,  self.seedsDCO) # mask in the SNe files the SNe that correspond to our DCO
        whichSN = fSN['whichStar'][...].squeeze()[maskSNdco]  # this is 1 if the initially primary star goes SN and 2 if the secondary goes supernova
        whichSN1 = whichSN[::2][indices] # get whichStar for the first SN   (there are 2 SNe for all DCOs)       

        self.separationPreSN2= fSN['separationBefore'][...].squeeze()[maskSNdco][1::2][indices] # the separation just before each SN  in [Rsun], we need only the separation for the second SN to occur, so the [1::2]  
        self.mWR =  fSN['MassStarSN'][...].squeeze()[maskSNdco][1::2][indices]   # obtain the CO core mass before the SNe
        self.MassStarCompanion = fSN['MassStarCompanion'][...].squeeze()[maskSNdco][1::2][indices]  # mass of the companion star (BH) in Msun

        # calculate period using Kepler III law 
        self.PeriodPreSN2 = convert_a_to_P_circular(separation=self.separationPreSN2*u.Rsun, M1=self.mWR*u.Msun, M2=self.MassStarCompanion*u.Msun)  # obtain the Period before the SNe
        self.PeriodPreSN2 = self.PeriodPreSN2.to(u.d).value
        
        self.st1 = fDCO['stellarType1'][...].squeeze()   # obtain the final stellar type of the Primary 
        self.st2 = fDCO['stellarType2'][...].squeeze()   # obtain the final stellar type of the Secondary
        
        self.spinM1 = np.zeros_like(self.M1)  # start by giving all primaries zero spin 
        self.spinM2 = np.zeros_like(self.M2)  # start by giving all secondaries zero spin 

        # did M1 form in the first SN?
        self.M1formedFirst =  (whichSN1==1) # mask that is 1 if the  compact object M1 formed first in the DCO
        # did M2 form in the first SN?
        self.M2formedFirst =  (whichSN1==2)  # mask that is 1 if the compact object M2 formed first in the DCO

        # Supernovae properties 
        # ['MassCOCoreSN',
        #  'MassCoreSN',
        #  'MassStarCompanion', 
        #  'MassStarSN', 
        #  'Survived',
        #  'eccentricityBefore', 
        #  'experiencedRLOF', 
        #  'fallback', 
        #  'previousStellarTypeCompanion',
        #  'previousStellarTypeSN',
        #  'randomSeed', 
        #  'separationBefore', 
        #  'whichStar']







    
    def QinSpin(self):
        """
        Returns spinM1 and spinM2, the spins of the compact objects formed from
        the initial most massive star (M1) and initial least massive star (M2), respectively. 
        
        In this approximation only a BH that is formed second can be tidally spun up, if its 
        pre-SN separation is tight enough. 
        
        see Qin+18, approximation originally given in https://ui.adsabs.harvard.edu/abs/2021MNRAS.504.3682C 
        (and Equation 5 in https://arxiv.org/pdf/2103.02608.pdf)
        
        """
        
        m_, c_ = -5./3, 0.5 # from Qin + 2018 

        # if BH & formed second, calculate spin with Qin+18 approximation
        maskGiveSpin1 = ((self.st1==14) & (self.M1formedFirst==0))
        maskGiveSpin2 = ((self.st2==14) & (self.M2formedFirst==0))
        
        # # first mask super tight NSBH that will get spin 1
        maskSpin1 = (np.log10(self.PeriodPreSN2) < -0.3) & (maskGiveSpin1 ==1)                        
        maskSpin2 = (np.log10(self.PeriodPreSN2) < -0.3) & (maskGiveSpin2 ==1)
        self.spinM1[maskSpin1] = np.ones(np.sum(maskSpin1)) # fill with ones 
        self.spinM2[maskSpin2] = np.ones(np.sum(maskSpin2)) # fill with ones 
  
        
        # now assign the spin for systems that lie in between the 0 and 1 spin using the fitting formulae
        maskChi_var1 = (np.log10(self.PeriodPreSN2) > -0.3) &  (np.log10(self.PeriodPreSN2) < 0.3)  &(maskGiveSpin1==1)
        self.spinM1[maskChi_var1] =  m_ * np.log10(self.PeriodPreSN2[maskChi_var1])  + c_   
             
        maskChi_var2 = (np.log10(self.PeriodPreSN2) > -0.3) &  (np.log10(self.PeriodPreSN2) < 0.3)  &(maskGiveSpin2==1)
        self.spinM2[maskChi_var2] =  m_ * np.log10(self.PeriodPreSN2[maskChi_var2])  + c_   
              
    
        return self.spinM1, self.spinM2

    
    
    def calculate_alpha_beta_Bavera21(self, c1_alpha, c2_alpha, c3_alpha,  c1_beta,  c2_beta,  c3_beta):


        alpha = self.function_f_Bavera21(c1_alpha, c2_alpha, c3_alpha)
        beta  = self.function_f_Bavera21(c1_beta,  c2_beta,  c3_beta)

        return alpha, beta

    def function_f_Bavera21(self, c1, c2, c3):
        """
        m_WR with units using astropy


        """

        top = -c1
        bottom = c2 + np.exp(-c3*self.mWR)

        f = top/bottom


        return f        
        
        
    # def BaveraSpin(self):
    #     """
    #     Returns spinM1 and spinM2, the spins of the compact objects formed from
    #     the initial most massive star (M1) and initial least massive star (M2), respectively. 
        
    #     In this approximation only a BH that is formed second can be tidally spun up, if its 
    #     pre-SN separation is tight enough. 

    #     based on Eq 1 and 2 from https://arxiv.org/pdf/2105.09077.pdf
    
    
    #     """

    #     # numerical coefficients form text below Eq 2
    #     # we use the values at helium depletion, since we later on use the C/O core mass. 
    #     c1_alpha, c2_alpha, c3_alpha =  0.059305, 0.035552, 0.270245
    #     c1_beta,  c2_beta, c3_beta   =  0.026960, 0.011001, 0.420739
        
    #     alpha, beta = self.calculate_alpha_beta_Bavera21(c1_alpha, c2_alpha, c3_alpha,  c1_beta,  c2_beta,  c3_beta)      
        

    #     # if BH & formed second, calculate spin with Qin+18 approximation
    #     maskGiveSpin1 = ((self.st1==14) & (self.M1formedFirst==0))
    #     maskGiveSpin2 = ((self.st2==14) & (self.M2formedFirst==0))
        
    #     # 
    #     # mask shorter than 1 day & a BH formed second 
    #     maskSpin1 = (np.log10(self.PeriodPreSN2) < 1) & (maskGiveSpin1 ==1)                        
    #     maskSpin2 = (np.log10(self.PeriodPreSN2) < 1) & (maskGiveSpin2 ==1)
        
    #     first_term = (alpha* (np.log10(self.PeriodPreSN2)**2)) 
    #     second_term =  ( beta * np.log10(self.PeriodPreSN2))  
    #     self.spinM1[maskSpin1]  =  first_term[maskSpin1]  + second_term[maskSpin1]  
    #     self.spinM2[maskSpin2]  =  first_term[maskSpin2]  + second_term[maskSpin2] 
        
    #     # HAVE TO ADD 
    #     # mask_  = (self.PeriodPreSN2<0.1)
    #     # self.spinM1[self.spinM1<0] = np.zeros(np.sum(mask_))
    #     # self.spinM2[self.spinM2<0] = np.zeros(np.sum(mask_))


    #     mask_ = (self.spinM1<0)
    #     self.spinM1[self.spinM1<0] = np.zeros(np.sum(mask_))
    #     mask_ = (self.spinM2<0)
    #     self.spinM2[self.spinM2<0] = np.zeros(np.sum(mask_))
        
        
    #     return self.spinM1, self.spinM2
    
    def BaveraSpin(self): 
        if self.state == 'c_depletion':
            c1a = 0.051237
            c2a = 0.029928
            c3a = 0.282998
            c1b = 0.027090
            c2b = 0.010905
            c3b = 0.422213
        elif self.state == 'he_depletion':
            c1a = 0.059305
            c2a = 0.035552
            c3a = 0.270245
            c1b = 0.026960
            c2b = 0.011001
            c3b = 0.420739
        else:
            raise ValueError('state not supported!')
        
        # a_BH2(p >= 1) = 0 
        a_BH2 = np.zeros(len(self.PeriodPreSN2)) # spin 
        
        def constant(m_WR, c1, c2, c3):
            return -c1/(c2+np.exp(-c3*m_WR))
        
        alpha = constant(self.mWR[self.PeriodPreSN2<1.], c1a, c2a, c3a)
        beta = constant(self.mWR[self.PeriodPreSN2<1.], c1b, c2b, c3b)



        a_BH2[self.PeriodPreSN2<1.] = alpha*np.log10(self.PeriodPreSN2[self.PeriodPreSN2<1.])**2+beta*np.log10(self.PeriodPreSN2[self.PeriodPreSN2<1.])
        

        # if BH & formed second, calculate spin with Qin+18 approximation
        maskGiveSpin1 = ((self.st1==14) & (self.M1formedFirst==0))
        maskGiveSpin2 = ((self.st2==14) & (self.M2formedFirst==0))

        self.spinM1[maskGiveSpin1]  =  a_BH2[maskGiveSpin1]
        self.spinM2[maskGiveSpin2]  =  a_BH2[maskGiveSpin2]

        # boundary conditions,if period < 0.09, make spin 1 
        # self.spinM1[self.PeriodPreSN2<0.09] = np.ones_like(self.PeriodPreSN2[self.PeriodPreSN2<0.09]) # fill with ones 
        # self.spinM2[self.PeriodPreSN2<0.09] = np.ones_like(self.PeriodPreSN2[self.PeriodPreSN2<0.09]) # fill with ones 
        # print(len(self.PeriodPreSN2[self.PeriodPreSN2<0.09]), ' out of boundary condition Period')

        # boundary conditions if M_WR < 8Msun make spin 0
        # self.spinM1[self.mWR<8] = np.zeros_like(self.PeriodPreSN2[self.mWR<8]) # fill with ones 
        # self.spinM2[self.mWR<8] = np.zeros_like(self.PeriodPreSN2[self.mWR<8]) # fill with ones 
        # print(len(self.mWR[self.mWR<8]), ' out of boundary condition Wolf Rayet Mass')

        print(len(self.spinM1[self.spinM1<0]), ' systems had negative spin because they are outside of the boundary conditions; we set these to 0 ')
        self.spinM1[self.spinM1<0] = np.zeros_like(self.spinM1[self.spinM1<0])
        self.spinM2[self.spinM2<0] = np.zeros_like(self.spinM2[self.spinM2<0])



        return self.spinM1, self.spinM2

    
    




MSSFRnameslist = []
MSSFRnameslist.append('000') # add phenomenological 

for ind_SFR, SFR in enumerate(SFRs):
    ind_x = ind_SFR+1
    for ind_GSMF, GSMF in enumerate(GSMFs):
        ind_y = ind_GSMF + 1
        for ind_MZ, MZ in enumerate(MZs):
            ind_z = ind_MZ +1

            MSSFRnameslist.append('%s%s%s'%(ind_x, ind_y, ind_z))
            
           


MSSFRnameslistCSV = ['.0.0.0', '.1.1.1', '.1.1.2', '.1.1.3', '.1.2.1', '.1.2.2', '.1.2.3', '.1.3.1', '.1.3.2', '.1.3.3', '.2.1.1', '.2.1.2', '.2.1.3', '.2.2.1', '.2.2.2', '.2.2.3', '.2.3.1', '.2.3.2', '.2.3.3', '.3.1.1', '.3.1.2', '.3.1.3', '.3.2.1', '.3.2.2', '.3.2.3', '.3.3.1', '.3.3.2', '.3.3.3']
        
MSSFRheaderDict =  {'000':'.0.0.0', '111':'.1.1.1', '112':'.1.1.2', '113':'.1.1.3', '121':'.1.2.1', '122':'.1.2.2', '123':'.1.2.3', '131':'.1.3.1', '132':'.1.3.2', '133':'.1.3.3', '211':'.2.1.1',\
                    '212':'.2.1.2', '213':'.2.1.3', '221':'.2.2.1', '222':'.2.2.2', '223':'.2.2.3', '231':'.2.3.1', '232':'.2.3.2', '233':'.2.3.3', '311':'.3.1.1', '312':'.3.1.2', '313':'.3.1.3', '321':'.3.2.1', \
                    '322':'.3.2.2', '323':'.3.2.3', '331':'.3.3.1', '332':'.3.3.2', '333':'.3.3.3'}    





def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
# colors = ['#1f77b4', '#ff7f0e']
# colors_lighter = [adjust_lightness(color=colors[0], amount=2.2),adjust_lightness(color=colors[1], amount=1.7)]




# Functions for metallicity yields 
solar=0.0142
metallicity_vlines_values_list = [np.log10(solar), np.log10(0.5*solar),np.log10(0.2*solar), np.log10(0.1*solar), np.log10(0.001)]#, np.log10(0.0105)]
metallicity_vlines_text_list = [r'$Z_{\rm{i}}=Z_{\odot}$', r'$Z_{\rm{i}}=Z_{\odot}/2$', \
             r'$Z_{\rm{i}}=Z_{\odot}/5$',  r'$Z_{\rm{i}}=Z_{\odot}/10$',\
             r'$Z_{\rm{i}}=0.001$'] #, r'$Z_{\rm{i}}=0.0105$']  
metallicities_list = [0.0001, 0.00011, 0.00012, 0.00014, 0.00016, 0.00017,\
   0.00019, 0.00022, 0.00024, 0.00027, 0.0003, 0.00034, \
   0.00037, 0.00042, 0.00047, 0.00052, 0.00058, 0.00065,\
   0.00073, 0.00081, 0.0009, 0.00101, 0.00113, 0.00126,\
   0.0014, 0.00157, 0.00175, 0.00195, 0.00218, 0.00243, \
   0.00272, 0.00303, 0.00339, 0.00378, 0.00422, 0.00471, \
   0.00526, 0.00587, 0.00655, 0.00732, 0.00817, 0.00912, \
   0.01018, 0.01137, 0.01269, 0.01416, 0.01581, 0.01765, 0.01971, 0.022, 0.0244, 0.02705, 0.03]






