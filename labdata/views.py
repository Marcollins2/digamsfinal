import requests
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import PatientForm, LabResultForm
from .utils import push_patient_to_fhir, push_lab_result_to_fhir
from .models import Patient, TestType, LabTest
from django.contrib import messages

def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()  # Save the patient to the database
            
            # Push the patient data to FHIR server
            patient_id, response = push_patient_to_fhir(patient)
            
            if patient_id:
                # Save the patient ID from FHIR to your patient instance
                patient.fhir_id = patient_id
                patient.save()
                print(f"Patient successfully created with FHIR ID: {patient_id}")
            else:
                print(f"Failed to create patient on FHIR server. Status code: {response.status_code}")
                print(f"Response content: {response.content.decode()}")
                
            
            return redirect('submit_lab_result', outpatient_number=patient.outpatient_number)
    else:
        form = PatientForm()
    
    return render(request, 'add_patient.html', {'form': form})


''' def patient_list(request):
    tests = LabTest.objects.all()
    return render(request, 'patient_list.html', {'tests': tests})

def patient_detail(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients}) '''

def submit_lab_result(request, outpatient_number):
    patient = get_object_or_404(Patient, outpatient_number=outpatient_number)  # Get the patient instance
    if request.method == 'POST':
        form = LabResultForm(request.POST)
        if form.is_valid():
            lab_result = form.save(commit=False)
            lab_result.patient = patient  # Assign the patient to the lab result
            lab_result.save()

            patient_id = patient.fhir_id


            # Push the patient data to FHIR server
            status_code, response = push_lab_result_to_fhir(lab_result, patient_id)


                        
            if status_code == 201:
                print("LabTest successfully pushed to FHIR server.")

            else:
                print(f"Failed to create observation. Status code: {status_code}")
                print(f"Response content: {response.content.decode()}")  # Ensure you see the response content for debugging

                
           # If "Save and Exit" button is clicked, redirect to the success page
            if 'save_exit' in request.POST:
                return redirect('success')
            else:
                # Allow for multiple lab results to be entered for the same patient
                return redirect(reverse('submit_lab_result', args=[outpatient_number]))
    else:
        form = LabResultForm()

    return render(request, 'submit_lab_result.html', {'form': form, 'patient': patient})


def success_view(request):
    """
    This view renders the success page after successful submission of patient details and lab test results.
    """
    return render(request, 'success.html')