from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ContactForm

# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # For now, we'll just print the email to the console.
            # Later, we can configure a real email backend.
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            html = render_to_string('contact/emails/contact_form.html', {
                'name': name,
                'email': email,
                'message': message,
            })

            print('--- FAKE EMAIL ---')
            print(f'To: your_email@example.com')
            print(f'From: {name} <{email}>')
            print(f'Subject: New Contact Form Submission')
            print(html)
            print('------------------')

            return redirect('contact_success') # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form}) 

def contact_success(request):
    return render(request, 'contact/contact_success.html')
