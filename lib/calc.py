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

def calculate(reader_file):

	# create file to write output csv file data
	writer_file = io.StringIO()
	writer = csv.writer(writer_file,delimiter=',')

	labels = []
	assays = []
	for line in csv.reader(reader_file, delimiter=','):
		if ('Label' in line[0]): # edit/write header line, then skip
			line += ['mode (rIU/mL)','68%CR-LB (rIU/mL)', '68%CR-UB (rIU/mL)', '95%CR-LB (rIU/mL)', '95%CR-UB (rIU/mL)', 'RM (TCID50/mL)', 'SK (TCID50/mL)']
			writer.writerow(line)
			continue
		elif ('#' in line[0]): # write/skip comment line
			writer.writerow(line)
			continue
		# read input csv file and run data through calculator
		Vinoc,dilmin,dilfac = (float(a) for a in line[1:1+3])
		icut = line[4:].index('#') + 4
		ntot = [int(a) for a in line[4:icut]]
		icut2 = line[icut+1:].index('#') + icut + 1
		ninf = [int(a) for a in line[icut+1:icut2]]
		assert len(ntot)==len(ninf)
		labels.append( line[0] )
		assays.append( midsin.Assay(Vinoc, dilmin, dilfac, ninf, ntot=ntot) )
		pack = assays[-1].payload()

		# write results to file for output csv file
		line += [ pack['mode'] ] + pack['bounds']
		line += [ pack['RM'] , pack['SK'] ]
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
