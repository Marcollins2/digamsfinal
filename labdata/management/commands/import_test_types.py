import pandas as pd
import os
from django.core.management.base import BaseCommand
from labdata.models import TestType  # Make sure to replace 'myapp' with your actual app name
from django.conf import settings

# Define the path to the Excel file
file_path = os.path.join(settings.BASE_DIR, 'labdata', 'data', 'Test_Type-LOINC.xlsx')


class Command(BaseCommand):
    help = 'Populate TestType data from Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel data
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            # Use update_or_create to ensure no duplicates and update existing entries
            TestType.objects.update_or_create(
                loinc_code=row['CODE'],  # Ensure 'CODE' matches the LOINC code field in your Excel file
                defaults={
                    'long_name': row['LONG COMMON NAME'],  # Adjusted field name
                    'short_name': row['SHORT NAME'],
                    'component': row['Component'],
                    'property': row['Property'],
                    'timing': row['Timing'],
                    'system': row['System'],
                    'scale': row['Scale'],
                    'method': row['Method'],
                    'unit': row.get('Unit'),  # Use .get() to avoid KeyError if the field is missing
                    'unit_code': row.get('Unit_code'),
                    'result_interpretation': row.get('result_interpretation'),
                    'interpretation_code': row.get('interpretation_code')
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated TestType data'))
