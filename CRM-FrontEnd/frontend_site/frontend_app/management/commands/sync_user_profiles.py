from django.core.management.base import BaseCommand
import requests
from frontend_app.models import UserProfile

class Command(BaseCommand):
    help = 'Synchronize user profiles with the external API'

    def handle(self, *args, **kwargs):
        response = requests.get('http://127.0.0.1:8000/userprofile/users/profiles/')
        
        if response.status_code == 200:
            profiles = response.json()
            for profile in profiles:
                # Check if profile already exists
                user_profile, created = UserProfile.objects.update_or_create(
                    user_id=profile['user'],
                    defaults={
                        'first_name': profile['first_name'],
                        'last_name': profile['last_name'],
                        'email': profile['email'],
                        'address': profile['address'],
                        'city': profile['city'],
                        'country': profile['country'],
                        'phone_number': profile['phone_number'],
                        'employee_id': profile['employee_id'],
                        'hire_date': profile.get('hire_date', None),
                        'position': profile['position'],
                        'work_location': profile['work_location'],
                        'work_mode': profile['work_mode'],
                        'emergency_contact_name': profile['emergency_contact_name'],
                        'emergency_contact_phone': profile['emergency_contact_phone'],
                        'education_degree': profile['education_degree'],
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Profile {'created' if created else 'updated'}: {user_profile}"))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch profiles from the API'))
