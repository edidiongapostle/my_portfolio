from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ContactForm
import smtplib

# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()

            subject = f"Message from {contact_instance.name}: {contact_instance.subject}"
            
            context = {
                'name': contact_instance.name,
                'email': contact_instance.email,
                'subject': contact_instance.subject,
                'message': contact_instance.message,
            }

            # Render the HTML email and create a plain text version
            html_content = render_to_string('contact/emails/contact_form.html', context)
            text_content = strip_tags(html_content)

            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.ADMIN_EMAIL]

            try:
                # Send a multipart email with both HTML and text
                email = EmailMultiAlternatives(
                    subject,
                    text_content, # plain text body
                    sender_email,
                    recipient_list
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except smtplib.SMTPAuthenticationError as e:
                print(f"\n--- SMTP AUTHENTICATION ERROR ---")
                print(f"An authentication error occurred: {e}")
                print("Please check your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py.")
                print("Ensure you are using a Google App Password, not your regular password.")
                print("-----------------------------------\n")
                return HttpResponse('Email sending failed due to an authentication error. Check server logs for details.')
            except Exception as e:
                print(f"\n--- UNEXPECTED EMAIL ERROR ---")
                print(f"An unexpected error occurred: {e}")
                print("--------------------------------\n")
                return HttpResponse('An unexpected error occurred while sending the email. Check server logs for details.')
            
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact/contact_success.html')
