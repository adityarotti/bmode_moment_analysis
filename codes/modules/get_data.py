##################################################################################################
# Author: Aditya Rotti, Jodrell Bank Center for Astrophysics, University of Manchester
# Date created: 31 March 2020
# Date modified: 31 March 2020
##################################################################################################
import os

base_cmd="scp arotti@vulture:"

def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)

def get_data(exprmnt,outpath=[],only_return_dict=True,verbose=False):
	if exprmnt=="PICO":
		import pico_dataio_dict as dd
	elif exprmnt=="DPICO":
		import dpico_dataio_dict as dd
	elif exprmnt=="LITEBIRD":
		import litebird_dataio_dict as dd

	if outpath==[]:
		outpath=dd.exprmnt["outdatapath"]
	ensure_dir(outpath)

	dd.exprmnt["outdatapath"]=outpath

	# Mask
	cmd = base_cmd + dd.exprmnt["mask_path"] + "/" + dd.exprmnt["mask_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.exprmnt["mask_fname"]
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
	cmd = base_cmd + dd.exprmnt["cl_path"] + "/" + dd.exprmnt["cl_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.exprmnt["cl_fname"]
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
	cmd = base_cmd + dd.exprmnt["indatapath"] + "/" + dd.exprmnt["cmb_fname"] + " " + outpath + "/"
	filename=outpath + "/" + dd.exprmnt["cmb_fname"]
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
	for idx in range(len(dd.exprmnt["datadef"].keys())):
		adr="cMILC" +str(idx).zfill(2)
		cmd = base_cmd + dd.exprmnt["indatapath"] + "/" + dd.exprmnt["fnames"][adr]["cmb"] + " " + outpath + "/"
		filename=outpath + "/" + dd.exprmnt["fnames"][adr]["cmb"]
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

		cmd = base_cmd + dd.exprmnt["indatapath"] + "/" + dd.exprmnt["fnames"][adr]["noise"] + " " + outpath + "/"
		filename=outpath + "/" + dd.exprmnt["fnames"][adr]["noise"]
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
	return dd.exprmnt
