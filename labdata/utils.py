import requests
import json

def push_patient_to_fhir(patient):
    url = 'http://hapi.fhir.org/baseR4/Patient'
    headers = {'Content-Type': 'application/fhir+json'}
    
    patient_data = {
        "resourceType": "Patient",
        "_id": patient.outpatient_number,
        "identifier": [
            {"system": "http://hospital.smarthealth.org/patient-ids", "value": patient.outpatient_number},
            {"system": "http://hospital.smarthealth.org/lab-ids", "value": patient.lab_number}
        ],
        "name": [{
            "use" : "official",
            "given": patient.firstname,
            "family": patient.surname
            }],

        "gender": patient.sex.lower(),
        "address": [
            {
                "city": patient.unit,
                "state": patient.village
            }
        ],
        "extension": [
            {
                "url": "http://hl7.org/fhir/StructureDefinition/sample-type",
                "valueString": patient.sample_type
            },

            {
                "url": "http://hl7.org/fhir/StructureDefinition/patient-age",
                "valueAge": {
                    "value": patient.age,
                    "unit": "years",
                    "system": "http://unitsofmeasure.org",
                    "code": "a"
                }
            }
        ]


    }
    
    response = None
    try:
        response = requests.post(url, data=json.dumps(patient_data), headers=headers)
        if response.status_code == 201:
            response_json = response.json()
            if response_json.get('resourceType') == 'Patient':
                patient_id = response_json.get('id')
                return patient_id, response
            else:
                print("Unexpected response format. Expected 'Patient' resource.")
                return None, response
        else:
            print(f"Failed to create patient on FHIR server. Status code: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            return None, response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, response

def push_lab_result_to_fhir(labtest, patient_id):
    url = 'http://hapi.fhir.org/baseR4/Observation'
    headers = {'Content-Type': 'application/fhir+json'}
    
    # Build FHIR Observation data
    observation_data = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "laboratory",
                        "display": "Laboratory"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": labtest.test_type.loinc_code,  # LOINC code for the test
                    "display": labtest.test_type.long_name  # Test name
                }
            ],
            "text": labtest.test_type.long_name  # Test name
        },
        "subject": {
            "reference":  f"Patient/{patient_id}",   # Reference to the patient
            "display": f"{labtest.patient.firstname} {labtest.patient.surname}"  # Patient display name
        },
        "effectiveDateTime": labtest.recorded_at.isoformat(),  # Date and time of the observation
        "valueQuantity": {
            "value": float(labtest.result_value),  # Convert result value to float
            "unit": labtest.unit,  # Unit of the result
            "system": "http://unitsofmeasure.org",
            # "code": labtest.unit_code  # Uncomment if you have a unit code
        },
        "interpretation": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        #"code": labtest.interpretation_code if labtest.interpretation_code else "",  # Interpretation code, if available
                        "display": labtest.result_interpretation  # Interpretation display text
                    }
                ]
            }
        ]
    }
    
    # Send to FHIR server
    response = requests.post(url, data=json.dumps(observation_data), headers=headers)

   # Return both status_code and response object
    return response.status_code, response

