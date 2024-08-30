from django import forms
from .models import Patient, LabTest, TestType

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['outpatient_number', 
            'lab_number', 
            'firstname', 
            'surname',
            'sex', 
            'age', 
            'unit', 
            'village', 
            'sample_type']

class LabResultForm(forms.ModelForm):
    test_type = forms.ModelChoiceField(
        queryset=TestType.objects.all(),  # Populates dropdown with TestType instances
        to_field_name='loinc_code', 
        label="Select Test",
        widget=forms.Select(attrs={'class': 'form-control'})  # Optional: Add CSS class for styling
    )

    class Meta:
        model = LabTest
        fields = ['test_type', 'result_value', 'unit', 'result_interpretation']
        widgets = {
            'result_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'result_interpretation': forms.TextInput(attrs={'class': 'form-control'}),
        }