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

from django.shortcuts import render
from django.http import HttpResponse
import midsin.web.forms as sinforms
import midsin.utils
import io
import csv
import zipfile



def home(request):
	if request.method == "GET":
		return render(request, "templates/home.html")



def csv_template(request):
	""" Constructs the csv_template for batch processing of multiple sample
		outcomes.

	"""
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="midsin_batch.csv"'
	writer = csv.writer(response)
	writer.writerows(midsin.utils.dict_to_csv(midsin.example))
	return response



def parse_ninf_ntot( pdic ):
	for key in ('ninf','ntot'):
		pdic[key] = [int(a) for a in pdic[key].replace(',',' ').split()]
	assert len(pdic['ninf']) == len(pdic['ntot']), "Length of ninf != ntot."
	assert len(pdic['ninf']) == pdic['ndils'], "Length of ninf != ndils."
	return pdic



def onesample(request):
	if request.method == "GET":
		form = sinforms.plate_layout(request.GET)

		# If layout hasn't even been set yet
		if not form.is_valid():
			form = sinforms.plate_layout()
			return render(request, "templates/onesample.html",{'form':form, 'status':'set_layout'})

		# If plate layout is valid: add the sample outcome (sninf, sntot)
		if 'ntot' not in request.GET:
			dils = form.add_outcome()
			return render(request,"templates/onesample.html",{'form':form, 'dils':dils, 'status':'set_outcome'})

		# If the sample outcome has been submitted and is valid
		data = parse_ninf_ntot( form.cleaned_data.copy() )
		gridfig,csvout = midsin.utils.dict_to_output(data)
		# Save figure file
		figfile = io.StringIO()
		gridfig.fig.savefig(figfile,format='svg',bbox_inches='tight')
		return render(request,"templates/onesample.html",{'status':'results', 'params':data, 'image':figfile.getvalue(), 'template':csvout.getvalue()})



def batch(request):
	if request.method == "GET":
		return render(request, "templates/batch.html")

	# POST method, i.e. user sends input csv file to server

	# prepare input csv file to read
	lines = request.FILES['file'].read().decode('UTF-8')
	lines = csv.reader(io.StringIO(lines),delimiter=',',quotechar="|")
	# compute results using midsin
	gridfig, writer_file = midsin.utils.csv_to_output(lines)
	# save graph for web display
	figtext = io.StringIO()
	gridfig.fig.savefig(figtext,format='svg',bbox_inches='tight')
	# Pack-up zip of [image as pdf] + [results as csv]
	image_file = io.BytesIO()
	gridfig.fig.savefig(image_file,format='pdf',bbox_inches='tight')
	zipbuffer = io.BytesIO()
	with zipfile.ZipFile(zipbuffer,'w') as zf:
		zf.writestr('output.pdf',image_file.getvalue())
		zf.writestr('output.csv',writer_file.getvalue())
	# return figfile and writerfile
	return render(request,'templates/batch.html',{'image':figtext.getvalue(), 'writer_file':writer_file.getvalue(),'zipbuffer':zipbuffer.getvalue().hex()})



def download_batchres(request):
	# grab the file via the request
	zipbuffer = bytes.fromhex(request.POST.get('zipbuffer'))
	#return zip-file as attachment
	response = HttpResponse(zipbuffer, content_type="application/x-zip-compressed")
	response['Content-Disposition'] = 'attachment; filename=output.zip'
	return response
