from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.


def contact(request):
    """ A view to display and process the contact form with email notification """
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save()
        send_mail(
            subject="New Contact Message",
            message=f"From {contact.name} <{contact.email}>:\n\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return redirect('contact_success')

    return render(request, 'contacts/contact.html', {'form': form})