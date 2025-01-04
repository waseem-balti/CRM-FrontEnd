import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        api_url = f"{settings.API_SERVER_URL}/auth/login/"
        response = requests.post(api_url, data={"email": email, "password": password})
        
        if response.status_code == 200:
            data = response.json()
            request.session['access_token'] = data['access']
            request.session['refresh_token'] = data['refresh']
            messages.success(request, "Logged in successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, "login.html")

def dashboard_view(request):
    # Fetch the access token from the session
    access_token = request.session.get("access_token")

    if not access_token:
        messages.error(request, "You must be logged in to access the dashboard.")
        return redirect("login")

    # API endpoint to fetch user profile data
    api_url = f"{settings.API_SERVER_URL}/user-profiles/"  # Adjust based on your API endpoint
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            user_profiles = response.json()  # Parse the response data
        else:
            messages.error(request, "Failed to fetch user profiles.")
            user_profiles = []
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error: {e}")
        user_profiles = []

    # Pass the user profiles to the dashboard template
    return render(request, "dashboard.html", {"user_profiles": user_profiles})

def logout_view(request):
    # Clear the session data
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("login")