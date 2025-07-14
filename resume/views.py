from django.shortcuts import render, redirect
from django.contrib import messages  # ADD THIS IMPORT
from django.core.mail import send_mail  # ADD THIS IMPORT
from django.conf import settings  # ADD THIS IMPORT
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
            
            # Send email notification
            try:
                send_mail(
                    subject=f"New Contact Form Submission from {name}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't show to user
                print(f"Failed to send email: {e}")
            
            # Add a success message
            messages.success(request, f"Thank you, {name}! Your message has been sent successfully.")
            
            # Redirect to avoid re-submission on page refresh
            return redirect("resume")

    return render(request, 'resume/resume.html')