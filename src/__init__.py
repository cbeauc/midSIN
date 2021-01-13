# Copyright (C) 2020-2021 Catherine Beauchemin
# Copyright (C) 2019-2020 Christian Quirouette
# Copyright (C) 2016-2019 Daniel Cresta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# =============================================================================

import numpy
import scipy.interpolate
import scipy.optimize
import scipy.stats


# Columns of csv input file
incols = ['name','Vinoc','dilmin','dilfac','ntot','ninf','comments']

# Columns added to csv output file
outcols = ['mode','68lb','68ub','95lb','95ub','RM','SK']

# label/header for assay parameters
label = {
	# input
	'Vinoc': "Well volume (in mL)",
	'dilmin': "Starting dilution",
	'dilfac': "Dilution factor",
	'ndils': "# dilutions",
	'nreps': "# repeats/dilution",
	'name': "Label",
	'ninf': "# wells infected",
	'ntot': "# wells total",
	'comments': "Comment (optional)",
	# output
	'mode': 'mode log10(SIN/mL)',
	'68lb': '68%CI-lo log10(SIN/mL)',
	'68ub': '68%CI-hi log10(SIN/mL)',
	'95lb': '95%CI-lo log10(SIN/mL)',
	'95ub': '95%CI-hi log10(SIN/mL)',
	'RM': 'RM log10(TCID50/mL)',
	'SK': 'SK log10(TCID50/mL)',
}

# help_text associated with assay parameters
info = {
	'Vinoc': "Typical value for 96-well plate is 0.1 mL.",
	'dilmin': "Must be &le; 1 (e.g. 10-fold as 0.1, 4-fold as 0.25).",
	'dilfac': "Must be &lt; 1 (e.g. 10-fold as 0.1, 4-fold as 0.25).",
	'ndils': "Typically 7 or 8 or 11 or 12.",
	'nreps': "Typically 4 or 6 or 8.",
	'name': "An identifying label like StrainA-24h-exp1.",
	'ninf': "A list separated by [,] [.] or [tab].",
	'ntot': "A list separated by [,] [.] or [tab].",
	'comments': "Can be anything you want (e.g. 24h).",
}

# parameter values for the example assay
example = {
	'Vinoc': 0.1,
	'dilmin': 0.01,
	'dilfac': 0.1,
	'ndils': 11,
	'nreps': 8,
	'name': "example",
	'ninf': [8,8,8,8,8,7,7,5,2,0,0],
	'ntot': [8,8,8,8,8,8,8,8,8,8,8],
	'comments': '',
}


def RMSK(dilut,Npos,Ntot):
	# if only one well
	if len(Npos) < 2:
		return (numpy.nan,numpy.nan)
	# if no infected well
	elif numpy.sum(Npos) == 0.0:
		return (numpy.nan,numpy.nan)
	# if all wells infected
	elif numpy.sum(Ntot-Npos) == 0.0:
		return (numpy.nan,numpy.nan)
	df = abs( numpy.diff(dilut)[0] )
	frac = 1.0*numpy.cumsum(Npos[::-1])[::-1]
	frac = frac/(frac+numpy.cumsum(Ntot-Npos))
	# Reed-Muench
	idx = numpy.argmax(frac < 0.5)-1
	propdist = (frac[idx]-0.5)/(frac[idx]-frac[idx+1])
	RM = df*propdist - dilut[idx]
	# Spearman-Kaerber
	frac = 1.0*Npos/Ntot # comment out this line to use RM-like smoothing
	idx = numpy.argmin( frac < 1.0 )
	if idx == 0: # if frac<1 in lowest dilution column
		frac = numpy.hstack((1.0,frac))
		dilut = numpy.hstack((dilut[0]+df,dilut))
	SK = df*numpy.trapz(frac[idx:]) - dilut[idx]
	return (RM,SK)


class Assay(object):
	def __init__(self, Vinoc, dilmin, dilfac, ninf, ntot):
		# Save user input
		self.pack = {'Vinoc':Vinoc, 'dilmin':dilmin, 'dilfac':dilfac}
		# computer n (# of unspoiled wells)
		self.pack['ntot'] = numpy.array(ntot)
		# Compute k (# of wells infected)
		self.pack['ninf'] = numpy.array(ninf)
		# Compute n-k (# of wells uninfected)
		self.nmks = self.pack['ntot']-self.pack['ninf']
		# Raise flag if no well was infected (lower limit of detection)
		if sum(self.pack['ninf']) == 0.0:
			self.isempty = True
		else:
			self.isempty = False
		# Raise flag if all wells were infected (upper limit of detection)
		if sum(self.nmks) == 0.0:
			self.isfull = True
		else:
			self.isfull = False
		# Compute arg of lnqbase = exp[ - Vinoc * dilmin * dilfac^pow ]
		self.VDs = Vinoc * dilmin * dilfac**numpy.arange(len(self.nmks))
		# Compute the remainder of the assay payload
		self.payload()

	def lCmode(self):
		""" Computes the mode of the posterior PDF for lCvir, and the TCID50 via the Reed-Munch and Spearmann-Kaerber estimation methods. """
		if 'mode' in self.pack.keys():
			return self.pack['mode']
		# If no infected well: give lC upper bound
		if self.isempty or self.isfull:
			self.pack['mode'] = numpy.nan
			return self.pack['mode']
		# Estimate most likely lCvir value (mode of dist)
		res = scipy.optimize.minimize_scalar(lambda x: -self.lCcalc(x))
		assert res.success, 'Could not find lC mode'
		self.pack['mode'] = res.x
		return self.pack['mode']

	def lCcalc(self, lCvec):
		""" Compute posterior likelihood distribution, i.e. value of exp(lnProb), for all elements in vector lCvec, and returns it as a vector of the same size as lCvec, suitable for plotting. """
		# OLD WAY OF COMPUTING
		#lnP = numpy.zeros_like(lCvec)
		# for each column...
		#for VD,k,nmk in zip(-self.VDs,self.pack['ninf'],self.nmks):
		#	CVD = 10.0**lCvec * VD
		#	lnP += nmk*CVD
		#	lnP += k*numpy.log1p(-numpy.exp(CVD))
		#return numpy.exp(lnP)
		# NEW WAY OF COMPUTING
		P = numpy.ones_like(lCvec)
		for VD,n,k in zip(-self.VDs,self.pack['ntot'],self.pack['ninf']):
			pinfvec = -numpy.expm1(10.0**lCvec*VD)
			P *= scipy.stats.binom.pmf(k,n,pinfvec)
		return P

	def lCdist(self, lCvec=None):
		""" Creates (if not provided) and stores the lCvir vector, stores the posterior PDF vector computed by lCcalc for the values in lCvir, and computes and stores the CDF vector corresponding to the PDF for the values in lCvir. """
		if lCvec is None:
			if self.isempty or self.isfull:
				a = -numpy.log10(self.VDs[0])-10.0
				b = -numpy.log10(self.VDs[-1])+10.0
				lb = scipy.optimize.brentq(lambda x: self.lCcalc(x)-0.0001,a,b)
				ub = scipy.optimize.brentq(lambda x: self.lCcalc(x)-0.9999,a,b)
				lCvec = numpy.linspace(lb,ub,500)
			else:
				lCvec = numpy.arange(0.0,1.0,0.01)
				lCvec = numpy.hstack((lCvec-2,numpy.arange(-1.0,1.0,0.002),lCvec+1))
				lCvec += self.lCmode()
		self.pack['lCvec'] = lCvec
		# Compute posterior likelihood distribution (pdf) for lVec
		self.pack['pdf'] = self.lCcalc(lCvec)
		# Compute CDF from posterior likelihood dist
		self.pack['cdf'] = numpy.cumsum(self.pack['pdf'][1:]*numpy.diff(self.pack['lCvec']))
		# Re-normalize so that CDF is 1 at Cvir= max in lCvec
		self.pack['cdf'] = numpy.hstack((0.0,self.pack['cdf']))/self.pack['cdf'].max()

	def lCbounds(self):
		""" Computes and stores the 68% and 95% bounds of lCvir likelihood as a 4-element list: [68-lower,68-upper,95-lower, 95-upper]. """
		if 'cdf' not in self.pack.keys():
			self.lCdist()
		if self.isempty or self.isfull:
			return [numpy.nan]*4
		ppf = scipy.interpolate.interp1d( self.pack['cdf'], self.pack['lCvec'], bounds_error=False, fill_value=0.0 )
		subbounds = []
		for frac in (0.68,0.95):
			res = scipy.optimize.minimize_scalar(lambda x: ppf(x+frac)-ppf(x),bounds=(0.0,1.0-frac),method='bounded')
			assert res.success, 'Could not find credible region.'
			subbounds += list( ppf([res.x,res.x+frac]) )
		return subbounds

	def payload(self):
		# Compute Reed-Muench and Spearman-Kaerber
		for key,val in zip(('RM','SK'),RMSK(numpy.log10(self.VDs),self.pack['ninf'],self.pack['ntot'])):
			self.pack[key] = val
		self.pack['bounds'] = self.lCbounds()
		self.pack['dilutions'] = numpy.log10(self.VDs/self.pack['Vinoc'])
		self.pack['mode'] = self.lCmode()
		self.pack['mean'] = numpy.sum(self.pack['lCvec']*self.pack['pdf'])
		self.pack['mean'] /= self.pack['pdf'].sum()
		return self.pack
