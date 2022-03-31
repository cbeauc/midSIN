# Copyright (C) 2020-2022 Catherine Beauchemin
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

"""
This module contains the plotting routines that produce a visual
representation of the experimental setup and the estimated
relative infectious virus concentration.

This file is part of the midsin module.
"""

import numpy
import matplotlib
params = {
	'xtick.labelsize': 14.0,
	'xtick.direction': 'in',
	'xtick.top': True,
	'ytick.labelsize': 14.0,
	'ytick.direction': 'in',
	'ytick.right': True,
	'axes.titlesize': 'medium',
	'axes.labelsize': 'medium',
	'legend.fontsize': 'medium',
	'font.family': 'serif',
	'font.size': 14.0,
	'text.usetex': True
}
matplotlib.rcParams.update(params)
import matplotlib.figure
from matplotlib.backends.backend_agg import FigureCanvas
import matplotlib.ticker


class grid_plot(object):
	def __init__(self, ghgw, hspace=0.44, wspace=0.32, rwidth=3.8, rheight=3.6):
		self.gh = ghgw[0]
		self.gw = ghgw[1]
		# Setup the figure looking nice
		self.fig = matplotlib.figure.Figure(figsize=(rwidth*self.gw,rheight*self.gh),subplotpars=matplotlib.figure.SubplotParams(hspace=hspace,wspace=wspace))
		self.canvas = FigureCanvas(self.fig)

	def subaxes(self, idx, *args, **kwargs):
		return self.fig.add_subplot(self.gh,self.gw,idx+1)



def lC_post(idassay, ax):
	xlab = r'$\log_{10}(\mathrm{specific\ infection, \mathrm{SIN/mL}})$'
	if idassay.isempty or idassay.isfull:
		ax.plot(idassay.pack['lCvec'],idassay.pack['pdf'],'k-')
		ax.fill_between(idassay.pack['lCvec'],idassay.pack['pdf'],color=(0.5,0.5,0.5))
		ax.set_title(r'Limit of detection')
		ax.set_xlabel(xlab)
		ax.set_ylabel(r'Un-normalizable likelihood')
		return True
	# Truncate the plot's range and dist to 1e-3 its max
	pmax = 10.**(round(numpy.log10(idassay.pack['pdf'].max())-0.5))
	bound = idassay.pack['bounds']
	# Outer dist
	oidx = (idassay.pack['pdf'] > idassay.pack['pdf'].max()/1.0e3)
	ax.fill_between(idassay.pack['lCvec'][oidx],idassay.pack['pdf'][oidx]/pmax,color=(0.5,0.5,0.5))
	# 95% CR dist
	idx = (bound[2] < idassay.pack['lCvec']) * (idassay.pack['lCvec'] < bound[3])
	ax.fill_between(idassay.pack['lCvec'][idx],idassay.pack['pdf'][idx]/pmax,color=(0.75,0.75,0.75))
	# 68% CR dist
	idx = (bound[0] < idassay.pack['lCvec']) * (idassay.pack['lCvec'] < bound[1])
	ax.fill_between(idassay.pack['lCvec'][idx],idassay.pack['pdf'][idx]/pmax,color='white')
	# The PDF outline
	ax.plot(idassay.pack['lCvec'][oidx],idassay.pack['pdf'][oidx]/pmax,'k-')
	# Indicated mode
	ax.axvline(idassay.pack['mode'], color='tab:blue')
	xlim = ax.get_xlim()
	cor = numpy.log10(numpy.exp(-0.5772156649)) # from Wulff
	ax.axvline(idassay.pack['RM']+cor,color='tab:orange',linewidth=1.5,linestyle='-')
	ax.axvline(idassay.pack['SK']+cor,color='tab:green',linewidth=1.5,linestyle='--')
	# Now annotate
	val = tuple([idassay.pack['mode']]+[a-idassay.pack['mode'] for a in bound])
	ax.set_title(r'${%.3f\,}_{%+.2f}^{%+.2f}\left[{}_{%+.2f}^{%+.2f}\right]$'%val)
	ax.set_xlabel(xlab)
	ax.set_ylabel(r'$\propto$ Likelihood\ $(\times10^{%g})$'% numpy.log10(pmax))
	ax.set_xlim(xlim)



def observed_wells(idassay, ax):
	# Compute theoretical DR curve
	diff = numpy.log10(idassay.pack['dilfac'])/2.0
	DR = [numpy.linspace(idassay.pack['dilutions'][-1]+diff,idassay.pack['dilutions'][0]-diff,200)]
	pb = numpy.exp(-10.**DR[0]*idassay.pack['Vinoc'])
	nmax = max(idassay.pack['ntot'])
	# Theoretical line
	for val in [idassay.pack['mode']]+idassay.pack['bounds']:
		DR.append( nmax*(1.-pb**(10.**val)) )
	DR = numpy.vstack(DR)
	# Vertical line showing TCID50 by others
	cor = numpy.log10(idassay.pack['Vinoc']) # as fct of well dilution, not /mL
	ax.axvline(idassay.pack['RM']+cor,color='tab:orange',linewidth=1.5,linestyle='-')
	ax.axvline(idassay.pack['SK']+cor,color='tab:green',linewidth=1.5,linestyle='--')
	# Plot theoretical curve based on mode of the Cvir distribution
	ax.fill_between(-DR[0],DR[4],DR[5],color=(0.75,0.75,0.75))
	ax.fill_between(-DR[0],DR[2],DR[3],color='white')
	ax.plot(-DR[0],DR[1],'tab:blue',linewidth=1.5)
	# Plot # wells infected vs dilution
	ax.axhline(idassay.pack['ntot'].max()*0.5,ls=':',color='grey')
	# Need to account for spoiled wells e.g. 7 rather than 8 repeats
	ninfcorr = (1.0*idassay.pack['ninf']/idassay.pack['ntot'])*numpy.round(idassay.pack['ntot'].mean())
	ax.plot(-idassay.pack['dilutions'],ninfcorr,'ko')
	# Now annotate
	ax.set_xticks(numpy.round(-idassay.pack['dilutions'][::2],1))
	ax.set_xticklabels(['%.1f'%s for s in ax.get_xticks()])
	ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True,min_n_ticks=min(6,idassay.pack['ntot'].max()),steps=[1, 2, 3, 4, 5, 10]))
	ax.set_xlim(-DR[0][-1],-DR[0][0])
	ax.set_ylim(-0.5,idassay.pack['ntot'].max()+0.5)
	ax.set_xlabel(r'Sample dilution,\ $10^{-x}$')
	ax.set_ylabel('Number of infected wells')
	ax.legend(['RM','SK'],bbox_to_anchor=(0.,1.02, 1.,.102), loc=3, ncol=2, borderaxespad=0., handlelength=1.7, handletextpad=0.3, frameon=False, borderpad=0.)
