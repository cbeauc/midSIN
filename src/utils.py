# Copyright (C) 2020-2021 Catherine Beauchemin
# Copyright (C) 2020 Christian Quirouette
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

import argparse
import csv
import midsin
import midsin.plot
import io



def dict_to_output(pdic):
	"""Parses input dictionary into a midsin.Assay and returns the analysis
		a figure and csv StringIO.

	Args:
		pdic: The dictionary of input parameters.
		header: Boolean whether or not the header line should be included.

	Returns:
		gridfig: matplotlib figure grid which can be saved via method
			gridfig.fig.savefig.
		writer_file: io.StingIO of the input+output written using csv.writer

	"""
	return csv_to_output(dict_to_csv(pdic))



def dict_to_csv(pdic,header=True):
	"""Parses input dictionary into a csv.writer-formatted list of lines
		suitable for use with .dict_to_output(lines).

	Args:
		pdic: The dictionary of input parameters.
		header: Boolean whether or not the header line should be included.

	Returns:
		lines: csv.writer-formatted list of lines.

	"""
	lines = []
	if header:
		lines.append(['%s'%midsin.label[key] for key in midsin.incols])
	# Check whether pdic contains one or more realizations
	try:
		nres = len(pdic['Vinoc'])
	except TypeError:
		nres = 1
	for n in range(nres):
		lines.append([])
		for key in midsin.incols:
			if key not in ('ntot','ninf'):
				lines[-1].append( pdic[key] )
			else:
				lines[-1] += list(pdic[key]) + ['#']
	# Offset header to accommodate the ndils columns of ntot and ninf
	for i in range(pdic['ndils']):
		lines[0].insert(lines[0].index(midsin.label['ntot'])+1,'')
		lines[0].insert(lines[0].index(midsin.label['ninf'])+1,'')
	return lines



def csv_to_output(csv_input_lines):
	"""Parses a list or iterator of csv.reader parsed input lines into a
		midsin.Assay and returns the analysis as a figure and csv StringIO.

	Args:
		csv_input_lines: csv.reader-style interator or list of lines.

	Returns:
		gridfig: matplotlib figure grid which can be saved via method
			gridfig.fig.savefig.
		writer_file: io.StingIO of the input+output written using csv.writer

	"""

	# create file to write output csv file data
	writer_file = io.StringIO()
	writer = csv.writer(writer_file,delimiter=',')

	labels = []
	assays = []
	for line in csv_input_lines:
		# Check if this is the header line
		if midsin.label['Vinoc'] in line:
			line += [midsin.label[key] for key in midsin.outcols]
			writer.writerow(line)
			continue
		# Check if line is commented-out (using #)
		elif line[0] == '#':
			writer.writerow(line)
			continue
		# Otherwise, parse input csv file line and input data into Assay
		Vinoc,dilmin,dilfac = (float(a) for a in line[1:1+3])
		icut = line[4:].index('#') + 4
		ntot = [int(a) for a in line[4:icut]]
		icut2 = line[icut+1:].index('#') + icut + 1
		ninf = [int(a) for a in line[icut+1:icut2]]
		assert len(ntot)==len(ninf)
		labels.append( line[0] )
		assays.append( midsin.Assay(Vinoc, dilmin, dilfac, ninf, ntot=ntot) )

		# write results to file for output csv file
		line += [ assays[-1].pack['mode'] ] + assays[-1].pack['bounds']
		line += [ assays[-1].pack['RM'] , assays[-1].pack['SK'] ]
		writer.writerow(line)

	# plot results 
	gridfig = midsin.plot.grid_plot((len(assays)+1,4))
	pid = -1;
	for idassay,label in zip(assays,labels):
		pid += 1; ax = gridfig.subaxes(pid); 
		midsin.plot.lC_post(idassay, ax)
		ax.text(0.03,0.95,label,va='top',ha='left',transform=ax.transAxes) 
		pid += 1; ax = gridfig.subaxes(pid)
		midsin.plot.observed_wells(idassay, ax)

	return gridfig, writer_file
