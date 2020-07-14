from django import forms

CHOICES = [
    ('1','Residue Labelling'),
    ('2','Hydrogen Deuterium Exchange'),
    ('3','DOPE Score'),
    ('4','Custom Residue Score')
]

HDX_CHOICES = [
    ('na',''),
    ('folding','Folding'),
    ('stability','Stability')
]

class PDBForm(forms.Form):
    PDB = forms.CharField(label='PDB',max_length=4,required=False)
    choice = forms.ChoiceField(label='Experimental Data Type',choices = CHOICES,required=False)
    hdx_opt = forms.ChoiceField(label='HDX Experiment (HDX Only)',choices=HDX_CHOICES,required=False)
    data = forms.FileField(label='Input Data',required=False)
