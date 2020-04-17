##################################################################################################
# Author: Aditya Rotti, Jodrell Bank Center for Astrophysics, University of Manchester
# Date created: 25 March 2020
# Date modified: 27 March 2020
##################################################################################################

import sys,os
import numpy as np
import healpy as h
import collections
import pandas as pd
import get_data as gd
from scipy.io.idl import readsav
from master import binned_master as bm
from scipy.interpolate import interp1d
from scipy.integrate import quad
from . import project_path


class setup_r_forecasts(object):
	def __init__(self,instrument="LITEBIRD",Alens_vals=[0.0,0.3,0.6,0.9],rprop=[1e-4,1e-1,1000],data_outpath=[],verbose=False,only_return_dict=True):
		self.data_outpath=data_outpath
		self.instrument=instrument
		self.Alens_vals=Alens_vals
		self.verbose=verbose
		self.only_return_dict=only_return_dict

#		if self.instrument=="LITEBIRD":
#			self.dd=gd.get_litebird_data(only_return_dict=False,outpath=self.data_outpath,verbose=self.verbose)
#		elif self.instrument=="PICO":
#			self.dd=gd.get_pico_data(only_return_dict=False,outpath=self.data_outpath,verbose=self.verbose)
		self.dd=gd.get_data(exprmnt=self.instrument,only_return_dict=self.only_return_dict,outpath=self.data_outpath,verbose=self.verbose)

		# You can update these when you run tabulate_rstat
		self.rprop=rprop
		self.rvalues=np.logspace(np.log10(rprop[0]),np.log10(rprop[1]),rprop[2])

	def setup_master(self,lmin=2,lmax=450,dell=8,fwhm=40.,mask=[]):
		self.fwhm=fwhm
		self.lmin=lmin
		self.lmax=lmax
		self.dell=dell
		
		# Get the analysis mask
		if mask==[]:
			vv=readsav(self.dd["outdatapath"] + self.dd["mask_fname"])
			self.mask=vv.apomask1m
		else:
			self.mask=mask
	
		self.fsky=np.sum(self.mask)/np.size(self.mask)
		self.nside=h.get_nside(self.mask)
		self.masklmax=2*self.nside
		
		# Setup Master
		beam=h.gauss_beam(fwhm=(self.fwhm/60.)*np.pi/180.,lmax=self.lmax)*h.pixwin(self.nside)[:self.lmax+1]
		self.master=bm.binned_master(self.mask,self.lmin,self.lmax,self.masklmax,beam=beam,deltaell=self.dell)

	def run_spectral_analysis(self,):
		self.clbin={}
		
		# Get the theory lensed Cls
#		data=np.loadtxt(project_path + "/dataout/pico/ffp10_lensedCls.dat")
		data=np.loadtxt(self.dd["outdatapath"] + "ffp10_lensedCls.dat")
		ell=data[:self.lmax-1,0] ; cldata=data[:self.lmax-1,3]
		cldata=cldata*2.*np.pi/(ell*(ell+1))
		ell=np.append([0.,1.],ell)
		cldata=np.append([0.,0.],cldata)
		self.lbin,self.clbin["lens"]=self.master.return_binned_spectra(cldata)

		# Get the theory BB Cls @ r=1
		data=np.loadtxt(project_path + "/dataout/test_tensCls.dat")
		ell=data[:self.lmax-1,0] ; cldata=data[:self.lmax-1,3]
		cldata=cldata*2.*np.pi/(ell*(ell+1))
		ell=np.append([0.,1.],ell)
		cldata=np.append([0.,0.],cldata)
		self.lbin,self.clbin["bb"]=self.master.return_binned_spectra(cldata)

		# Get the master corrected CMB map spectrum
		cmb=h.read_map(self.dd["outdatapath"] + self.dd["cmb_fname"],verbose=False)
		cldata=h.alm2cl(h.map2alm(cmb*self.mask,lmax=self.lmax))
		self.lbin,self.clbin["cmb"]=self.master.return_bmcs(cldata)

		self.clbin["frg"]={}
		self.clbin["frg1"]={}
		self.clbin["obs"]={}
		self.clbin["noise"]={}
		self.adr_list=sorted(self.dd["fnames"].keys())

		for adr in self.adr_list:
			# Obs.
			obs=h.read_map(self.dd["outdatapath"] + self.dd["fnames"][adr]["cmb"],verbose=False)
			cldata=h.alm2cl(h.map2alm(obs*self.mask,lmax=self.lmax))
			self.lbin,self.clbin["obs"][adr]=self.master.return_bmcs(cldata)
			# Noise.
			noise=h.read_map(self.dd["outdatapath"] + self.dd["fnames"][adr]["noise"],verbose=False)
			cldata=h.alm2cl(h.map2alm(noise*self.mask,lmax=self.lmax))
			self.lbin,self.clbin["noise"][adr]=self.master.return_bmcs(cldata)
			# Frg. - estimated from obs, cmb and noise
			data=obs-cmb-noise
			cldata=h.alm2cl(h.map2alm(data*self.mask,lmax=self.lmax))
			self.lbin,self.clbin["frg"][adr]=self.master.return_bmcs(cldata)
			# Frg - directly estimated in component separation
			data=h.read_map(self.dd["outdatapath"] + self.dd["fnames"][adr]["frg"],verbose=False)
			cldata=h.alm2cl(h.map2alm(data*self.mask,lmax=self.lmax))
			self.lbin,self.clbin["frg1"][adr]=self.master.return_bmcs(cldata)

	def tabulate_rlike(self,Alens_vals=[0.0,0.3,0.6,0.9],rprop=[1e-4,1e-1,1000],compute_map=False,rvar=1):
		self.Alens_vals=Alens_vals
		self.rprop=rprop
		self.rvalues=np.logspace(np.log10(rprop[0]),np.log10(rprop[1]),rprop[2])
		
		self.rlike_dict=collections.OrderedDict()
		self.rlike_map_dict=collections.OrderedDict()
		for adr in self.adr_list:
			self.rlike_dict[adr]=collections.OrderedDict()
			self.rlike_map_dict[adr]=collections.OrderedDict()
			for Alens in self.Alens_vals:
				self.rlike_dict[adr][Alens]=self.return_r_likelihood(adr,Alens,rvar)
				if compute_map:
					self.rlike_map_dict[adr][Alens]=self.return_r_likelihood_map(adr,Alens)

#	def return_r_likelihood(self,adr,Alens):
#		var=(Alens*self.clbin["cmb"])**2. + self.clbin["noise"][adr]**2. + self.clbin["frg"][adr]**2.
##		var=(self.clbin["obs"][adr] - (1.-Alens)*self.clbin["cmb"])**2.
#		var=var*(2./((2.*self.lbin+1)*self.dell*self.fsky))
#		fn_like = np.vectorize(lambda x : np.sum((self.clbin["frg"][adr] - x*self.clbin["bb"])**2./var))
#		data=fn_like(self.rvalues) ; data=data-min(data)
#		return np.exp(-data/2.)

	def return_r_likelihood(self,adr,Alens,rvar=1.):
#		var_other=(Alens*self.clbin["cmb"])**2. + self.clbin["noise"][adr]**2. + self.clbin["frg"][adr]**2.
		var_other=(self.clbin["obs"][adr] - (1.-Alens)*self.clbin["cmb"])**2.
		data=np.zeros_like(self.rvalues)
		for ir,r in enumerate(self.rvalues):
			var=(var_other + rvar*(r*self.clbin["bb"])**2.)*(2./((2.*self.lbin+1)*self.dell*self.fsky))
			data[ir] = np.sum((self.clbin["frg"][adr] - r*self.clbin["bb"])**2./var)
		data=data-min(data)
		return np.exp(-data/2.)

	def return_r_likelihood_map(self,adr,Alens):
		like_map=np.zeros((len(self.rvalues),len(self.lbin)),dtype=np.float64)
#		var=(Alens*self.clbin["cmb"])**2. + self.clbin["noise"][adr]**2. + self.clbin["frg"][adr]**2.
		var=(self.clbin["obs"][adr] - (1.-Alens)*self.clbin["cmb"])**2.
		var=var*(2./((2.*self.lbin+1)*self.dell*self.fsky))
		for il, ell in enumerate(self.lbin):
			fn_like = np.vectorize(lambda x : np.exp(-np.sum((self.clbin["frg"][adr][il] - x*self.clbin["bb"][il])**2./var[il])/2.))
			like_map[:,il]=fn_like(self.rvalues)
		return like_map

	def tabulate_rstat(self,sigma=0.66,ul=0.95,tol=1e-2):
		self.rstat=collections.OrderedDict()
		for adr in self.adr_list:
			self.rstat[adr]=collections.OrderedDict()
			for Alens in self.Alens_vals:
				try:
					self.rstat[adr][Alens]=return_pdf_char(self.rvalues,self.rlike_dict[adr][Alens],tol=tol,sigma=sigma,ul=ul)
				except:
					print "Failed at",adr,Alens

def return_pdf_char(x,pdf,tol=1e-2,sigma=0.682,ul=0.95,ul_snr=2.):
	stat={}
	mask=np.ones_like(pdf) ; mask[pdf<tol/10.]=0
	x=x[mask==True] ; pdf=pdf[mask==True]
	mp_idx=np.where(pdf==max(pdf))[0][0]
	stat["mp"]=x[mp_idx]

	stat["comment_l"]="Compact"
	if pdf[0]>tol:
		stat["comment_l"]="Not compact"

	stat["comment_h"]="Compact"
	if pdf[-1]>tol:
		stat["comment_h"]="Not compact"

	stat["sigma"]=np.NAN ; stat["ul"]=np.NAN ; stat["snr"]=np.NAN
	# Lower error needs to be computed before upper error.
	# If high r posterior is terminated and low end is not compact full result wont be returned.
	if stat["comment_l"]=="Compact":
		fn=interp1d(x[:mp_idx+1],pdf[:mp_idx+1],kind="cubic",assume_sorted=False)
		norm=quad(fn,stat["mp"],min(x[:mp_idx+1]))[0]
		# Normalizing the PDF
		fn=interp1d(x[:mp_idx+1],pdf[:mp_idx+1]/norm,kind="cubic",assume_sorted=False)
		tempx=np.linspace(stat["mp"],min(x[:mp_idx+1]),len(x[:mp_idx+1]))
		cpdf=np.zeros_like(tempx)
		for ix,xp in enumerate(tempx):
			cpdf[ix]=quad(fn,stat["mp"],xp)[0]
		fn_cpdf=interp1d(cpdf,tempx,kind="cubic",assume_sorted=False,fill_value=max(tempx))
		stat["sigma"]=stat["mp"]-fn_cpdf(sigma)
		stat["snr"]=stat["mp"]/stat["sigma"]
	elif stat["comment_h"]=="Compact":
		fn=interp1d(x[mp_idx:],pdf[mp_idx:],kind="cubic",assume_sorted=False)
		norm=quad(fn,stat["mp"],max(x[mp_idx:]))[0]
		# Normalizing the PDF
		fn=interp1d(x[mp_idx:],pdf[mp_idx:]/norm,kind="cubic",assume_sorted=False)
		tempx=np.linspace(stat["mp"],max(x[mp_idx:]),len(x[mp_idx:]))
		cpdf=np.zeros_like(tempx)
		for ix,xp in enumerate(tempx):
			cpdf[ix]=quad(fn,stat["mp"],xp)[0]
		fn_cpdf=interp1d(cpdf,tempx,kind="cubic",assume_sorted=False,fill_value=max(tempx))
		stat["sigma"]=fn_cpdf(sigma)-stat["mp"]
		stat["snr"]=stat["mp"]/stat["sigma"]
		if stat["snr"]<=ul_snr:
			stat["ul"]=fn_cpdf(ul)

	return stat

def return_pdf_char_old(x,pdf,tol=1e-2,sigma=0.66,ul=.95):
	stat={}
	mask=np.ones_like(pdf) ; mask[pdf<tol/10.]=0
	x=x[mask==True] ; pdf=pdf[mask==True]
	mp_idx=np.where(pdf==max(pdf))[0][0]
	stat["mp"]=x[mp_idx]

	stat["comment_l"]="Compact"
	if pdf[0]>tol:
		stat["comment_l"]="Not compact"

	stat["comment_h"]="Compact"
	if pdf[-1]>tol:
		stat["comment_h"]="Not compact"

	stat["sigma_l"]=np.float64(x[0])
	if stat["comment_l"]=="Compact":
		fn=interp1d(x[:mp_idx+1],pdf[:mp_idx+1],kind="cubic",assume_sorted=False)
		norm=quad(fn,stat["mp"],min(x[:mp_idx+1]))[0]
		# Normalizing the PDF
		fn=interp1d(x[:mp_idx+1],pdf[:mp_idx+1]/norm,kind="cubic",assume_sorted=False)
		tempx=np.linspace(stat["mp"],min(x[:mp_idx+1]),len(x[:mp_idx+1]))
		cpdf=np.zeros_like(tempx)
		for ix,xp in enumerate(tempx):
			cpdf[ix]=quad(fn,stat["mp"],xp)[0]
		fn_cpdf=interp1d(cpdf,tempx,kind="cubic",assume_sorted=False,fill_value=max(tempx))
		stat["sigma_l"]=stat["mp"]-fn_cpdf(sigma)

	stat["sigma_h"]=np.float64(x[-1])
	stat["ul"]=np.float64(x[-1])
	if stat["comment_h"]=="Compact":
		fn=interp1d(x[mp_idx:],pdf[mp_idx:],kind="cubic",assume_sorted=False)
		norm=quad(fn,stat["mp"],max(x[mp_idx:]))[0]
		# Normalizing the PDF
		fn=interp1d(x[mp_idx:],pdf[mp_idx:]/norm,kind="cubic",assume_sorted=False)
		tempx=np.linspace(stat["mp"],max(x[mp_idx:]),len(x[mp_idx:]))
		cpdf=np.zeros_like(tempx)
		for ix,xp in enumerate(tempx):
			cpdf[ix]=quad(fn,stat["mp"],xp)[0]
		fn_cpdf=interp1d(cpdf,tempx,kind="cubic",assume_sorted=False,fill_value=max(tempx))
		stat["sigma_h"]=fn_cpdf(sigma)-stat["mp"]

		fn=interp1d(x,pdf,kind="cubic",assume_sorted=False)
		norm=quad(fn,x[0],x[-1])[0]
		# Normalizing the PDF
		fn=interp1d(x,pdf/norm,kind="cubic",assume_sorted=False)
		cpdf=np.zeros_like(x)
		for ix,xp in enumerate(x):
			cpdf[ix]=quad(fn,x[0],xp)[0]
		fn_cpdf=interp1d(cpdf,x,kind="cubic",assume_sorted=False,fill_value=max(tempx))
		stat["ul"]=fn_cpdf(ul)*1
	return stat
