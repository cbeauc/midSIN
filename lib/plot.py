# Copyright (C) 2020 Catherine Beauchemin
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

class grid_plot(object):
	def __init__(self, ghgw, hspace=0.44, wspace=0.32, rwidth=3.8, rheight=3.6):
		self.gh = ghgw[0]
		self.gw = ghgw[1]
		# Setup the figure looking nice
		self.fig = matplotlib.figure.Figure(figsize=(rwidth*self.gw,rheight*self.gh),subplotpars=matplotlib.figure.SubplotParams(hspace=hspace,wspace=wspace))
		self.canvas = FigureCanvas(self.fig)

	def subaxes(self, idx, *args, **kwargs):
		return self.fig.add_subplot(self.gh,self.gw,idx+1)
