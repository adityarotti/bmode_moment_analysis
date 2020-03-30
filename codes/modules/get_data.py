##################################################################################################
# Author: Aditya Rotti, Jodrell Bank Center for Astrophysics, University of Manchester
# Date created: 25 March 2020
# Date modified: 27 March 2020
##################################################################################################

import os
import dataio_dict as dd

base_cmd="scp arotti@vulture:"

def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)

def get_pico_data(outpath=[],only_return_dict=True,verbose=False):
	if outpath==[]:
		outpath=dd.PICO["outdatapath"]
	ensure_dir(outpath)

	dd.PICO["outdatapath"]=outpath

	# Mask
	cmd = base_cmd + dd.PICO["mask_path"] + "/" + dd.PICO["mask_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.PICO["mask_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				if verbose:
					print "Getting : ", filename
				os.system(cmd)
		except:
			print "Failed to execute command"

	# Power spectrum
	cmd = base_cmd + dd.PICO["cl_path"] + "/" + dd.PICO["cl_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.PICO["cl_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				print "Getting : ", filename
				if verbose:
					os.system(cmd)
		except:
			print "Failed to execute command"

	# True CMB
	cmd = base_cmd + dd.PICO["indatapath"] + "/" + dd.PICO["cmb_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.PICO["cmb_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				if verbose:
					print "Getting : ", filename
				os.system(cmd)
		except:
			print "Failed to execute command"

	# True CMB
	for idx in range(len(dd.PICO["datadef"].keys())):
		adr="cMILC" +str(idx).zfill(2)
		cmd = base_cmd + dd.PICO["indatapath"] + "/" + dd.PICO["fnames"][adr]["cmb"] + " " + outpath + "/"
		filename=outpath + "/" + dd.PICO["fnames"][adr]["cmb"]
		if verbose:
			print cmd
		if not(only_return_dict):
			try:
				if os.path.isfile(filename):
					if verbose:
						print filename + " exists"
				else:
					if verbose:
						print "Getting : ", filename
					os.system(cmd)
			except:
				print "Failed to execute command"

		cmd = base_cmd + dd.PICO["indatapath"] + "/" + dd.PICO["fnames"][adr]["noise"] + " " + outpath + "/"
		filename=outpath + "/" + dd.PICO["fnames"][adr]["noise"]
		if verbose:
			print cmd
		if not(only_return_dict):
			try:
				if os.path.isfile(filename):
					if verbose:
						print filename + " exists"
				else:
					if verbose:
						print "Getting : ", filename
					os.system(cmd)
			except:
				print "Failed to execute command"
	return dd.PICO

def get_litebird_data(outpath=[],only_return_dict=True,verbose=False):
	if outpath==[]:
		outpath=dd.LITEBIRD["outdatapath"]
	ensure_dir(outpath)

	dd.LITEBIRD["outdatapath"]=outpath

	# Mask
	cmd = base_cmd + dd.LITEBIRD["mask_path"] + "/" + dd.LITEBIRD["mask_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.LITEBIRD["mask_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				if verbose:
					print "Getting : ", filename
				os.system(cmd)
		except:
			print "Failed to execute command"

	# Power spectrum
	cmd = base_cmd + dd.LITEBIRD["cl_path"] + "/" + dd.LITEBIRD["cl_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.LITEBIRD["cl_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				if verbose:
					print "Getting : ", filename
				os.system(cmd)
		except:
			print "Failed to execute command"

	# True CMB
	cmd = base_cmd + dd.LITEBIRD["indatapath"] + "/" + dd.LITEBIRD["cmb_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.LITEBIRD["cmb_fname"]
	if verbose:
		print cmd
	if not(only_return_dict):
		try:
			if os.path.isfile(filename):
				if verbose:
					print filename + " exists"
			else:
				if verbose:
					print "Getting : ", filename
				os.system(cmd)
		except:
			print "Failed to execute command"

	# True CMB
	for idx in range(len(dd.LITEBIRD["datadef"].keys())):
		adr="cMILC" +str(idx).zfill(2)
		cmd = base_cmd + dd.LITEBIRD["indatapath"] + "/" + dd.LITEBIRD["fnames"][adr]["cmb"] + " " + outpath + "/"
		filename=outpath + "/" + dd.LITEBIRD["fnames"][adr]["cmb"]
		if verbose:
			print cmd
		if not(only_return_dict):
			try:
				if os.path.isfile(filename):
					if verbose:
						print filename + " exists"
				else:
					if verbose:
						print "Getting : ", filename
					os.system(cmd)
			except:
				print "Failed to execute command"

		cmd = base_cmd + dd.LITEBIRD["indatapath"] + "/" + dd.LITEBIRD["fnames"][adr]["noise"] + " " + outpath + "/"
		filename=outpath + "/" + dd.LITEBIRD["fnames"][adr]["noise"]
		if verbose:
			print cmd
		if not(only_return_dict):
			try:
				if os.path.isfile(filename):
					if verbose:
						print filename + " exists"
				else:
					if verbose:
						print "Getting : ", filename
					os.system(cmd)
			except:
				print "Failed to execute command"
	return dd.LITEBIRD

