import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Login API endpoint
        login_api_url = f"{settings.API_SERVER_URL}/auth/login/"
        response = requests.post(login_api_url, data={"email": email, "password": password})
        
        if response.status_code == 200:
            # Store tokens in session
            data = response.json()
            access_token = data.get('access')
            request.session['access_token'] = access_token

            # Updated profile API URL
            profile_api_url = f"{settings.API_SERVER_URL}/userprofile/users/profiles/"
            headers = {"Authorization": f"Bearer {access_token}"}

            # Check if user profile exists
            profile_response = requests.get(profile_api_url, headers=headers)
            if profile_response.status_code == 200:
                user_profiles = profile_response.json()
                if user_profiles:  # Profile exists
                    return redirect("dashboard")
                else:  # No profile exists
                    return redirect("create_profile")
            else:
                messages.error(request, f"Failed to check profile status. {profile_response.text}")
                return redirect("login")
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "login.html")


def create_profile_view(request):
    access_token = request.session.get("access_token")

    if not access_token:
        messages.error(request, "You must be logged in to create a profile.")
        return redirect("login")

    if request.method == "POST":
        # Profile creation API endpoint
        profile_api_url = f"{settings.API_SERVER_URL}/user-profiles/"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
        }

        response = requests.post(profile_api_url, headers=headers, data=data)

        if response.status_code == 201:
            messages.success(request, "Profile created successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, f"Failed to create profile. {response.text}")

    return render(request, "create_profile.html")


def dashboard_view(request):
    access_token = request.session.get("access_token")
    
    if not access_token:
        messages.error(request, "You must be logged in to access the dashboard.")
        return redirect("login")
    
    return render(request, "dashboard.html")


def logout_view(request):
    # Clear the session data
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("login")