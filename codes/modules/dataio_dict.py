##################################################################################################
# Author: Aditya Rotti, Jodrell Bank Center for Astrophysics, University of Manchester
# Date created: 25 March 2020
# Date modified: 27 March 2020
##################################################################################################

import os
import collections
from . import project_path

cmb_prefix="_CMB_NILC_BB"
noise_prefix="_CMB_NILC_noise"
suffix="res40acm.fits"

mom_lbl={}
mom_lbl["cmb"]=r"$f_{\rm CMB}$"
mom_lbl["f_sync"]=r"$f_{\rm sync}$"
mom_lbl["df_sync/dbeta"]=r"$\frac{d f_{\rm sync}}{d \beta}$"
mom_lbl["d2f_sync/dbeta2"]=r"$\frac{d^2 f_{\rm sync}}{d^2 \beta}$"
mom_lbl["f_dust"]=r"$I_{\rm dust}$"
mom_lbl["df_dust/dbeta"]=r"$\frac{d f_{\rm dust}}{d \beta}$"
mom_lbl["df_dust/dT"]=r"$\frac{d f_{\rm dust}}{d T}$"
mom_lbl["d2f_dust/dbeta2"]=r"$\frac{d^2 f_{\rm dust}}{d^2 \beta}$"
mom_lbl["d2f_dust/dbetadT"]=r"$\frac{d^2 f_{\rm dust}}{d \beta d T}$"
mom_lbl["d2f_dust/dT2"]=r"$\frac{d^2 f_{\rm dust}}{d^2 T}$"


# PICO --------------------------------------------------------------
PICO=collections.OrderedDict()
PICO["indatapath"]="/scratch/nas_vulture/scratch/mremazei/PICO/90.91/"
PICO["outdatapath"]= project_path + "/dataout/pico/"
PICO["simname"]="PICO"
PICO["datadef"] = {
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

PICO["fnames"]={}
PICO["cmb_fname"]="smoothed_input_cmb_bmode_map_v2.fits"
for key in range(len(PICO["datadef"].keys())):
    adr="cMILC" + str(key).zfill(2)
    PICO["fnames"][adr]={}
    PICO["fnames"][adr]["cmb"]=PICO["simname"] + cmb_prefix
    PICO["fnames"][adr]["cmb"]=PICO["fnames"][adr]["cmb"]+PICO["datadef"][adr]["midfix"] + suffix
    PICO["fnames"][adr]["noise"]=PICO["simname"] + noise_prefix
    PICO["fnames"][adr]["noise"]=PICO["fnames"][adr]["noise"]+PICO["datadef"][adr]["midfix"] + suffix

PICO["mask_path"]="/scratch/nas_vulture/scratch/mremazei/LiteBIRD/outputs2/"
PICO["mask_fname"]="apodized_masks_v2.sav"
PICO["cl_path"]="/raid/scratch/mremazei/WORK/GNILC_CMB/litebird/cosmo/PICO/"
PICO["cl_fname"]="ffp10_lensedCls.dat"

PICO["lbl"]={}
PICO["npar"]={}
for idx in range(len(PICO["datadef"].keys())):
	adr="cMILC" + str(idx).zfill(2)
	PICO["npar"][adr]=len(PICO["datadef"][adr]["moments"])
	PICO["lbl"][adr]=adr+" : "
	for imom,mom in  enumerate(PICO["datadef"][adr]["moments"]):
		if imom>0:
			PICO["lbl"][adr]=PICO["lbl"][adr] + " ; " +  mom_lbl[mom]
		else:
			PICO["lbl"][adr]=PICO["lbl"][adr] + mom_lbl[mom]
	if PICO["datadef"][adr]["comment"]=="Hybrid":
		PICO["lbl"][adr]=PICO["lbl"][adr] + " (H)"


# LITEBIRD --------------------------------------------------------------
LITEBIRD=collections.OrderedDict()
LITEBIRD["indatapath"]="/scratch/nas_vulture/scratch/mremazei/LiteBIRD/outputs22/"
LITEBIRD["outdatapath"]= project_path +  "/dataout/litebird/"
LITEBIRD["simname"]="LITEBIRD"
LITEBIRD["datadef"] = {
"cMILC00" : {"midfix" : "_" , "moments": ["cmb"], "comment" : None},
"cMILC01" : {"midfix" : "0m_" , "moments":["cmb","f_sync"], "comment" : None},
"cMILC02" : {"midfix" : "1m_" , "moments":["cmb","f_dust"], "comment" : None},
"cMILC03" : {"midfix" : "2m_" , "moments":["cmb","f_sync","f_dust"], "comment" : None},
"cMILC04" : {"midfix" : "2m1_" , "moments":["cmb","f_dust", "df_dust/dbeta"], "comment" : None},
"cMILC05" : {"midfix" : "3m0_" , "moments":["cmb","f_sync","f_dust", "df_sync/dbeta"], "comment" : None},
"cMILC06" : {"midfix" : "3m0h_" , "moments":["cmb","f_sync","f_dust", "df_sync/dbeta"], "comment" : "Hybrid"},
"cMILC07" : {"midfix" : "3m1_" , "moments":["cmb","f_sync","f_dust", "df_dust/dbeta"], "comment" : None},
"cMILC08" : {"midfix" : "3m1h_" , "moments":["cmb","f_sync","f_dust", "df_dust/dbeta"], "comment" : "Hybrid"},
"cMILC09" : {"midfix" : "2m2m_", "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta","df_dust/dbeta"], "comment" : None},
"cMILC10" : {"midfix" : "2m3m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT"], "comment" : None},
"cMILC11" : {"midfix" : "2m2m1m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta","df_dust/dbeta", "df_dust/dT", "d2f_sync/dbeta2"], "comment" : None},
"cMILC12" : {"midfix" : "2m2m2m_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT", "d2f_sync/dbeta2", "d2f_dust/dT2"], "comment" : None},
"cMILC13" : {"midfix" : "1_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta", "df_dust/dbeta", "df_dust/dT","d2f_sync/dbeta2", "d2f_dust/dT2", "d2f_dust/dbetadT"], "comment" : None},
"cMILC14" : {"midfix" : "2_" , "moments" : ["cmb","f_sync", "f_dust", "df_sync/dbeta","df_dust/dbeta", "df_dust/dT","d2f_sync/dbeta2", "d2f_dust/dT2","d2f_dust/dbetadT", "d2f_dust/dbeta2"], "comment" : None},
}

LITEBIRD["fnames"]={}
LITEBIRD["cmb_fname"]="smoothed_input_cmb_bmode_map_v2.fits"
for key in range(len(LITEBIRD["datadef"].keys())):
    adr="cMILC" + str(key).zfill(2)
    LITEBIRD["fnames"][adr]={}
    LITEBIRD["fnames"][adr]["cmb"]=LITEBIRD["simname"] + cmb_prefix
    LITEBIRD["fnames"][adr]["cmb"]=LITEBIRD["fnames"][adr]["cmb"]+LITEBIRD["datadef"][adr]["midfix"] + suffix
    LITEBIRD["fnames"][adr]["noise"]=LITEBIRD["simname"] + noise_prefix
    LITEBIRD["fnames"][adr]["noise"]=LITEBIRD["fnames"][adr]["noise"]+LITEBIRD["datadef"][adr]["midfix"] + suffix

LITEBIRD["mask_path"]="/scratch/nas_vulture/scratch/mremazei/LiteBIRD/outputs2/"
LITEBIRD["mask_fname"]="apodized_masks_v2.sav"
LITEBIRD["cl_path"]="/raid/scratch/mremazei/WORK/GNILC_CMB/litebird/cosmo/LITEBIRD/"
LITEBIRD["cl_fname"]="Cls_Planck2018_lensed_scalar.fits"

LITEBIRD["lbl"]={}
LITEBIRD["npar"]={}
for idx in range(len(LITEBIRD["datadef"].keys())):
	adr="cMILC" + str(idx).zfill(2)
	LITEBIRD["npar"][adr]=len(LITEBIRD["datadef"][adr]["moments"])
	LITEBIRD["lbl"][adr]=adr+" : "
	for imom,mom in  enumerate(LITEBIRD["datadef"][adr]["moments"]):
		if imom>0:
			LITEBIRD["lbl"][adr]=LITEBIRD["lbl"][adr] + " ; " +  mom_lbl[mom]
		else:
			LITEBIRD["lbl"][adr]=LITEBIRD["lbl"][adr] + mom_lbl[mom]
	if LITEBIRD["datadef"][adr]["comment"]=="Hybrid":
		LITEBIRD["lbl"][adr]=LITEBIRD["lbl"][adr] + " (H)"
