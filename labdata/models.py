from django.db import models
from django.core.validators import RegexValidator


alpha_validator = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetical characters are allowed.')

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    record_date = models.DateField(auto_now_add=True)  # Automatically sets the date when the record is created
    outpatient_number = models.CharField(max_length=100, primary_key=True)
    lab_number = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=255, validators=[alpha_validator])
    surname = models.CharField(max_length=255, validators=[alpha_validator])
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES,)
    age = models.IntegerField()
    unit = models.CharField(max_length=255, validators=[alpha_validator])
    village = models.CharField(max_length=255, validators=[alpha_validator])
    sample_type = models.CharField(max_length=255, validators=[alpha_validator])
    fhir_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.surname} ({self.outpatient_number})"
        
class TestType(models.Model):
    loinc_code = models.CharField(max_length=20, unique=True, primary_key=True)  # CODE
    long_name = models.CharField(max_length=255)  # LONG COMMON NAME
    short_name = models.CharField(max_length=100)  # SHORT NAME
    component = models.CharField(max_length=100)  # Component
    property = models.CharField(max_length=50)  # Property
    timing = models.CharField(max_length=50)  # Timing
    system = models.CharField(max_length=100)  # System
    scale = models.CharField(max_length=50)  # Scale
    method = models.CharField(max_length=100)  # Method
    unit = models.CharField(max_length=20, null=True, blank=True)  # Unit
    unit_code = models.CharField(max_length=20, null=True, blank=True)  # Unit_code
    result_interpretation = models.TextField(null=True, blank=True)  # result_interpretation
    interpretation_code = models.CharField(max_length=50, null=True, blank=True)  # interpretation_code

    def __str__(self):
        return f"{self.component} ({self.loinc_code})"


class LabTest(models.Model):
    patient = models.ForeignKey('Patient', to_field='outpatient_number', on_delete=models.CASCADE)  # Link to Patient model
    test_type = models.ForeignKey('TestType', to_field='loinc_code', on_delete=models.CASCADE)  # Link to TestType model
    result_value = models.DecimalField(max_digits=10, decimal_places=2)  # Result value entered by the user
    unit = models.CharField(max_length=20)  # Unit entered by the user
    result_interpretation = models.TextField(null=True, blank=True)  # Result interpretation entered by the user
    recorded_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f"{self.test_type.long_name}: {self.result_value} {self.unit} (Recorded on {self.recorded_at})"