##################################################################################################
# Author: Aditya Rotti, Jodrell Bank Center for Astrophysics, University of Manchester
# Date created: 31 March 2020
# Date modified: 31 March 2020
##################################################################################################

import os
import collections
from . import project_path

cmb_prefix="_CMB_NILC_BB"
noise_prefix="_CMB_NILC_noise"
suffix="res40acm.fits"

mom_lbl={}
mom_lbl["cmb"]=r"$I_{\rm CMB}$"
mom_lbl["f_sync"]=r"$I_{\rm sync}$"
mom_lbl["df_sync/dbeta"]=r"$\frac{d I_{\rm sync}}{d \beta}$"
mom_lbl["d2f_sync/dbeta2"]=r"$\frac{d^2 I_{\rm sync}}{d^2 \beta}$"
mom_lbl["f_dust"]=r"$I_{\rm dust}$"
mom_lbl["df_dust/dbeta"]=r"$\frac{d I_{\rm dust}}{d \beta}$"
mom_lbl["df_dust/dT"]=r"$\frac{d I_{\rm dust}}{d T}$"
mom_lbl["d2f_dust/dbeta2"]=r"$\frac{d^2 I_{\rm dust}}{d^2 \beta}$"
mom_lbl["d2f_dust/dbetadT"]=r"$\frac{d^2 I_{\rm dust}}{d \beta d T}$"
mom_lbl["d2f_dust/dT2"]=r"$\frac{d^2 I_{\rm dust}}{d^2 T}$"


# PICO --------------------------------------------------------------
exprmnt=collections.OrderedDict()
## These are the original files where analysis is done with regularization noise
#exprmnt["indatapath"]="/scratch/nas_vulture/scratch/mremazei/PICO/90.91/"
#exprmnt["outdatapath"]= project_path + "/dataout/pico/"
## No regularization noise here. Double precision solved the problem.
#exprmnt["indatapath"]="/scratch/nas_vulture/scratch/mremazei/PICO/90.91DOUBLE/"
#exprmnt["outdatapath"]= project_path + "/dataout/pico_double/"
## No regularization noise here. Double precision solved the problem + dust (1/T) derivatives
#exprmnt["indatapath"]="/scratch/nas_vulture/scratch/mremazei/PICO/90.91DOUBLE2/"
#exprmnt["outdatapath"]= project_path + "/dataout/pico_1bT/"
#No regularization noise here. Double precision solved the problem + more low ell needlets
exprmnt["indatapath"]="/scratch/nas_vulture/scratch/mremazei/PICO/90.91NEED/"
exprmnt["outdatapath"]= project_path + "/dataout/pico_low_needlets/"

exprmnt["simname"]="PICO"
exprmnt["datadef"] = {
"cMILC00" : {"midfix" : "_" , "moments": ["cmb"], "comment" : None},
"cMILC01" : {"midfix" : "0m_" , "moments":["cmb","f_sync"], "comment" : None},
"cMILC02" : {"midfix" : "1m_" , "moments":["cmb","f_dust"], "comment" : None},
"cMILC03" : {"midfix" : "2m_" , "moments":["cmb","f_sync","f_dust"], "comment" : None},
"cMILC04" : {"midfix" : "2m1_" , "moments":["cmb","f_dust", "df_dust/dbeta"], "comment" : None},
"cMILC05" : {"midfix" : "3m1_" , "moments":["cmb","f_sync","f_dust", "df_dust/dbeta"], "comment" : None},
"cMILC06" : {"midfix" : "2m2m_", "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta","df_dust/dbeta"], "comment" : "Hybrid"},
"cMILC07" : {"midfix" : "2m3m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT"], "comment" : None},
"cMILC08" : {"midfix" : "2m2m1m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta","df_dust/dT", "d2f_dust/dT2"], "comment" : None},
"cMILC09" : {"midfix" : "2m2m1mh_", "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta","df_dust/dT", "d2f_dust/dT2"], "comment" : "Hybrid"},
"cMILC10" : {"midfix" : "2m2m2m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT", "d2f_sync/dbeta2", "d2f_dust/dT2"], "comment" : None},
"cMILC11" : {"midfix" : "2m2m2mh_", "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT", "d2f_sync/dbeta2", "d2f_dust/dT2"], "comment" : "Hybrid"},
"cMILC12" : {"midfix" :"1_","moments":["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT","d2f_sync/dbeta2", "d2f_dust/dT2","d2f_dust/dbetadT"], "comment" : None},
"cMILC13" : {"midfix" : "1h_","moments" : ["cmb","f_sync","f_dust","df_sync/dbeta","df_dust/dbeta","df_dust/dT","d2f_sync/dbeta2","d2f_dust/dT2","d2f_dust/dbetadT"], "comment" : "Hybrid"},
"cMILC14" : {"midfix" : "2_" , "moments" : ["cmb", "f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT", "d2f_sync/dbeta2", "d2f_dust/dT2", "d2f_dust/dbetadT", "d2f_dust/dbeta2"], "comment" : None},
}

exprmnt["fnames"]={}
exprmnt["cmb_fname"]="smoothed_input_cmb_bmode_map_v2.fits"
for key in range(len(exprmnt["datadef"].keys())):
    adr="cMILC" + str(key).zfill(2)
    exprmnt["fnames"][adr]={}
    exprmnt["fnames"][adr]["cmb"]=exprmnt["simname"] + cmb_prefix
    exprmnt["fnames"][adr]["cmb"]=exprmnt["fnames"][adr]["cmb"]+exprmnt["datadef"][adr]["midfix"] + suffix
    exprmnt["fnames"][adr]["noise"]=exprmnt["simname"] + noise_prefix
    exprmnt["fnames"][adr]["noise"]=exprmnt["fnames"][adr]["noise"]+exprmnt["datadef"][adr]["midfix"] + suffix

exprmnt["mask_path"]="/scratch/nas_vulture/scratch/mremazei/LiteBIRD/outputs2/"
exprmnt["mask_fname"]="apodized_masks_v2.sav"
exprmnt["cl_path"]="/raid/scratch/mremazei/WORK/GNILC_CMB/litebird/cosmo/PICO/"
exprmnt["cl_fname"]="ffp10_lensedCls.dat"

exprmnt["lbl"]={}
exprmnt["npar"]={}
for idx in range(len(exprmnt["datadef"].keys())):
	adr="cMILC" + str(idx).zfill(2)
	exprmnt["npar"][adr]=len(exprmnt["datadef"][adr]["moments"])
	exprmnt["lbl"][adr]=adr+" : "
	for imom,mom in  enumerate(exprmnt["datadef"][adr]["moments"]):
		if imom>0:
			exprmnt["lbl"][adr]=exprmnt["lbl"][adr] + " ; " +  mom_lbl[mom]
		else:
			exprmnt["lbl"][adr]=exprmnt["lbl"][adr] + mom_lbl[mom]
	if exprmnt["datadef"][adr]["comment"]=="Hybrid":
		exprmnt["lbl"][adr]=exprmnt["lbl"][adr] + " (H)"
