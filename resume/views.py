from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def resume(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Basic validation
        if not name or not email or not message:
            messages.error(request, "All fields are required. Please fill out the form completely.")
        else:
            # Save the message to the database
            ContactMessage.objects.create(name=name, email=email, message=message)
            
            # Add a success message
            messages.success(request, f"Thank you, {name}! Your message has been sent successfully.")
            
            # Redirect to avoid re-submission on page refresh
            return redirect("resume")

    return render(request, 'resume/resume.html')
