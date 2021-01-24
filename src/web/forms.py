from django import forms
from django.utils.safestring import mark_safe
import midsin



class plate_layout(forms.Form):
	#<!-- Vinoc, dilmin, dilfac, (ndils) ninf, ntot -->
	Vinoc = forms.FloatField(
		label = midsin.label['Vinoc'],
		help_text = midsin.info['Vinoc'],
		initial = midsin.example['Vinoc'],
	)
	dilmin = forms.FloatField(
		label = midsin.label['dilmin'],
		help_text = mark_safe(midsin.info['dilmin']),
		initial = midsin.example['dilmin'],
		max_value = 1.0,
	)
	dilfac = forms.FloatField(
		label = midsin.label['dilfac'],
		help_text = mark_safe(midsin.info['dilfac']),
		initial = midsin.example['dilfac'],
		max_value = 0.9999999,
	)
	ndils = forms.IntegerField(
		label = midsin.label['ndils'],
		help_text = midsin.info['ndils'],
		initial = midsin.example['ndils'],
		min_value = 1,
	)
	nreps = forms.IntegerField(
		label = midsin.label['nreps'],
		help_text = midsin.info['nreps'],
		initial = midsin.example['nreps'],
		min_value = 1,
	)
	## Fields related to sample outcomes
	name = forms.CharField(
		label = midsin.label['name'],
		help_text = midsin.info['name'],
		required = False,
	)
	ninf = forms.CharField(
		label = midsin.label['ninf'],
		help_text = midsin.info['ninf'],
		required = False,
		widget = forms.TextInput(attrs={'size': '50'}),
	)
	ntot = forms.CharField(
		label = midsin.label['ntot'],
		help_text = midsin.info['ntot'],
		required = False,
		widget = forms.TextInput(attrs={'size': '50'}),
	)
	comments = forms.CharField(
		label = midsin.label['comments'],
		help_text = midsin.info['comments'],
		required = False,
		widget = forms.TextInput(attrs={'placeholder': '24.0'})
	)

	def add_outcome(self):
		# Disable fields linked to plate layout
		# Enable fields linked to sample outcome
		for field in self.fields.values():
			if field.required == True:
				field.widget.attrs['readonly'] = True
			elif field.label != midsin.label['comments']:
				field.required = True
		# Add the sample outcome fields
		layout = self.cleaned_data
		dil = layout['dilmin']
		dilfac = layout['dilfac']
		nreps = layout['nreps']
		ndils = layout['ndils']
		# Now set default values for all required outcome fields
		data = self.data.copy()
		data['name'] = 'StrainA-24h'
		if (ndils == midsin.example['ndils']) and (nreps == midsin.example['nreps']):
			data['ninf'] = '\t'.join(map(str,midsin.example['ninf']))
			data['ntot'] = '\t'.join(map(str,midsin.example['ntot']))
		else:
			data['ninf'] = '\t'.join(['%d'%nreps]*(ndils-1)+['0'])
			data['ntot'] = '\t'.join(['%d'%nreps]*ndils)
		self.data = data
		return ['%.3g'%(dil*dilfac**idil) for idil in range(ndils)]
