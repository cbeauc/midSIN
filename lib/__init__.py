# Copyright (C) 2020 Catherine Beauchemin
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

import math
import numpy
import scipy.interpolate
import scipy.optimize
import scipy.stats


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

	def plot_ppld(self,ax):
		xlab = r'$\log_{10}(\mathrm{specific\ infection, \mathrm{SIN/mL}})$'
		if self.isempty or self.isfull:
			ax.plot(self.pack['lCvec'],self.pack['pdf'],'k-')
			ax.fill_between(self.pack['lCvec'],self.pack['pdf'],color=(0.5,0.5,0.5))
			ax.set_title(r'Limit of detection')
			ax.set_xlabel(xlab)
			ax.set_ylabel(r'Un-normalizable likelihood')
			return True
		# Truncate the plot's range and dist to 1e-3 its max
		pmax = 10.**(round(numpy.log10(self.pack['pdf'].max())-0.5))
		bound = self.pack['bounds']
		# Outer dist
		oidx = (self.pack['pdf'] > self.pack['pdf'].max()/1.0e3)
		ax.fill_between(self.pack['lCvec'][oidx],self.pack['pdf'][oidx]/pmax,color=(0.5,0.5,0.5))
		# 95% CR dist
		idx = (bound[2] < self.pack['lCvec']) * (self.pack['lCvec'] < bound[3])
		ax.fill_between(self.pack['lCvec'][idx],self.pack['pdf'][idx]/pmax,color=(0.75,0.75,0.75))
		# 68% CR dist
		idx = (bound[0] < self.pack['lCvec']) * (self.pack['lCvec'] < bound[1])
		ax.fill_between(self.pack['lCvec'][idx],self.pack['pdf'][idx]/pmax,color='white')
		# The PDF outline
		ax.plot(self.pack['lCvec'][oidx],self.pack['pdf'][oidx]/pmax,'k-')
		# Indicated mode
		ax.axvline(self.pack['mode'], color='tab:blue')
		xlim = ax.get_xlim()
		cor = numpy.log10(numpy.exp(-0.5772156649)) # from Wulff
		ax.axvline(self.pack['RM']+cor,color='tab:orange',linewidth=1.5,linestyle='-')
		ax.axvline(self.pack['SK']+cor,color='tab:green',linewidth=1.5,linestyle='--')
		# Now annotate
		val = tuple([self.pack['mode']]+[a-self.pack['mode'] for a in bound])
		ax.set_title(r'${%.3f\,}_{%+.2f}^{%+.2f}\left[{}_{%+.2f}^{%+.2f}\right]$'%val)
		ax.set_xlabel(xlab)
		ax.set_ylabel(r'$\propto$ Likelihood\ $(\times10^{%g})$'% numpy.log10(pmax))
		ax.set_xlim(xlim)

	def plot_DRassay(self,ax):
		# Compute theoretical DR curve
		diff = numpy.log10(self.pack['dilfac'])/2.0
		DR = [numpy.linspace(self.pack['dilutions'][-1]+diff,self.pack['dilutions'][0]-diff,200)]
		pb = numpy.exp(-10.**DR[0]*self.pack['Vinoc'])
		nmax = max(self.pack['ntot'])
		# Theoretical line
		for val in [self.pack['mode']]+self.pack['bounds']:
			DR.append( nmax*(1.-pb**(10.**val)) )
		DR = numpy.vstack(DR)
		# Vertical line showing TCID50 by others
		cor = numpy.log10(self.pack['Vinoc']) # as fct of well dilution, not /mL
		ax.axvline(self.pack['RM']+cor,color='tab:orange',linewidth=1.5,linestyle='-')
		ax.axvline(self.pack['SK']+cor,color='tab:green',linewidth=1.5,linestyle='--')
		# Plot theoretical curve based on mode of the Cvir distribution
		ax.fill_between(-DR[0],DR[4],DR[5],color=(0.75,0.75,0.75))
		ax.fill_between(-DR[0],DR[2],DR[3],color='white')
		ax.plot(-DR[0],DR[1],'tab:blue',linewidth=1.5)
		# Plot # wells infected vs dilution
		ax.axhline(self.pack['ntot'].max()*0.5,ls=':',color='grey')
		ax.plot(-self.pack['dilutions'],self.pack['ninf'],'ko')
		# Now annotate
		ax.set_xticks(numpy.round(-self.pack['dilutions'][::2],1))
		ax.set_xticklabels(['%.1f'%s for s in ax.get_xticks()])
		ax.set_yticks(range(0,max(self.pack['ntot'])+1))
		ax.set_xlim(-DR[0][-1],-DR[0][0])
		ax.set_ylim(-0.5,self.pack['ntot'].max()+0.5)
		ax.set_xlabel(r'Sample dilution,\ $10^{-x}$')
		ax.set_ylabel('Number of infected wells')
		ax.legend(['RM','SK'],bbox_to_anchor=(0.,1.02, 1.,.102), loc=3, ncol=2, borderaxespad=0., handlelength=1.7, handletextpad=0.3, frameon=False, borderpad=0.)
