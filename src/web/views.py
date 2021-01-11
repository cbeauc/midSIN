from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import midsin.web.forms as sinforms


def index(request):
	if request.method == "GET":
		return render(request, "templates/home.html")


def parse_plate_outcome( pdic ):
	for key in ('ninf','ntot'):
		pdic[key] = [int(a) for a in pdic[key].replace(',',' ').split()]
	assert len(pdic['ninf']) == len(pdic['ntot']), "Length of ninf != ntot."
	assert len(pdic['ninf']) == pdic['ndils'], "Length of ninf != ndils."
	return pdic


def oneplate(request):
	if request.method == "GET":
		form = sinforms.plate_layout(request.GET)

		# If layout hasn't even been set yet
		if not form.is_valid():
			form = sinforms.plate_layout()
			return render(request, "templates/oneplate.html",{'form':form, 'status':'set_layout'})

		# If plate layout is valid: add the plate outcome (sninf, sntot)
		if 'ntot' not in request.GET:
			dils = form.add_outcome()
			return render(request,"templates/oneplate.html",{'form':form, 'dils':dils, 'status':'set_outcome'})

		# If the plate outcome has been submitted and is valid
		data = parse_plate_outcome( form.cleaned_data.copy() )
		# Process results
		#assay = midsin.Assay(Vinoc, dilmin, dilfac, ninf, ntot=ntot)
		#gridfig = midsin.plot.grid_plot(1,2)
		#ax = gridfig.subaxes(0)
		#midsin.plot.lC_post(idassay, ax)
		#ax.text(0.03,0.95,label,va='top',ha='left',transform=ax.transAxes) 
		#ax = gridfig.subaxes(0)
		#midsin.plot.observed_wells(idassay, ax)
		return render(request,"templates/oneplate.html",{'status':'results', 'params': data}) 


def oldv2oneplate(request):
	if request.method == "GET":
		form = sinforms.plate_layout(request.GET)
		# after layout, before outcome
		if form.is_valid():
			layout = form.cleaned_data
			layout_text = ['%s = %g'%(form.fields[key].label,val) for key,val in layout.items()]
			outcome_form = sinforms.plate_outcome()
			outcome_form.add_outcome(layout)
			return render(request, "templates/oneplate.html",{'layout_form': None, 'layout_text': layout_text, 'outcome_form': outcome_form})
		# after layout, after outcome
		if 'ntot0' in request.GET:
			form = sinforms.plate_outcome(request.GET)
			if form.is_valid():
				print(form.layout)
				return render(request, "templates/oneplate.html",{'layout_form': None, 'outcome_form': form})
		# Initial (before layout)
		form = sinforms.plate_layout()
		return render(request, "templates/oneplate.html",{'layout_form': form})


def batch(request):
	if request.method == "GET":
		return render(request, "templates/batch.html")

