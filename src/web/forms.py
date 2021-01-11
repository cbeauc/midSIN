from django import forms
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.safestring import mark_safe
import midsin

class FlexFloatField(forms.CharField):
	def to_python(self, value):
		if value:
			return float(eval(repr(value)))
		return value


class plate_layout(forms.Form):
	#<!-- Vinoc, dilmin, dilfac, (ndils) ninf, ntot -->
	Vinoc = forms.FloatField(
		#label="blah",
		#help_text="wrong text",
		label = midsin.label['Vinoc'],
		help_text = midsin.info['Vinoc'],
		initial = 0.1,
	)
	dilmin = forms.FloatField(
		label = midsin.label['dilmin'],
		help_text = mark_safe(midsin.info['dilmin']),
		max_value = 1.0,
		initial = 0.01,
		#validator = [MaxValueValidator(1.0)],
	)
	dilfac = forms.FloatField(
		label = midsin.label['dilfac'],
		help_text = mark_safe(midsin.info['dilfac']),
		max_value = 0.9999999,
		initial = 0.1,
	)
	ndils = forms.IntegerField(
		label = midsin.label['ndils'],
		help_text = midsin.info['ndils'],
		min_value = 1,
		initial = 11,
	)
	nreps = forms.IntegerField(
		label = midsin.label['nreps'],
		help_text = midsin.info['nreps'],
		min_value = 1,
		initial = 8,
	)
	## Fields related to plate outcomes
	name = forms.CharField(
		label = midsin.label['name'],
		help_text = midsin.info['name'],
		initial = 'strainA',
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
		# Enable fields linked to plate outcome
		for field in self.fields.values():
			if field.required == True:
				field.widget.attrs['readonly'] = True
			elif 'Comment' not in field.label:
				field.required = True
		# Add the plate outcome fields
		layout = self.cleaned_data
		dil = layout['dilmin']
		dilfac = layout['dilfac']
		nreps = layout['nreps']
		ndils = layout['ndils']
		# Now set default values for all required outcome fields
		data = self.data.copy()
		data['name'] = 'StrainA-24h'
		if (ndils == 11) and (nreps == 8):
			data['ninf'] = '8\t'*5+'7\t7\t5\t2\t0\t0'
		else:
			data['ninf'] = (('0\t')*ndils)[:-1]
		data['ntot'] = (('%d\t'%nreps)*ndils)[:-1]
		self.data = data
		return ['%.3g'%(dil*dilfac**idil) for idil in range(ndils)]


if False:
	def add_outcome(self,layout):
		# Disable fields linked to plate layout
		for field in self.fields.values():
			field.widget.attrs['readonly'] = True
		# Add the plate outcome fields
		dil = layout['dilmin']
		dilfac = layout['dilfac']
		nreps = layout['nreps']
		ndils = layout['ndils']
		dils = ['%.3g'%(dil*dilfac**idil) for idil in range(ndils)]
		sninf = (('0\t')*ndils)[:-1]
		sntot = (('%d\t'%nreps)*ndils)[:-1]
		self.fields['name'] = forms.CharField(
			label = 'Plate outcome label',
			initial = 'strainA',
		)
		self.fields['sninf'] = forms.CharField(
			label = '# wells infected',
			initial = sninf,
		)
		self.fields['sntot'] = forms.CharField(
			label='# wells total',
			initial = sntot,
		)
		self.fields['comments'] = forms.CharField(
			label = 'Comment (optional)',
			help_text="Can be anything you want (e.g. 24h).",
			required = False,
		)
		self.fields['sninf'].widget.attrs.update(size='45')
		self.fields['sntot'].widget.attrs.update(size='45')
		return {'dils': dils, 'sninf': sninf, 'sntot': sntot}

#class plate_outcome(plate_layout):
