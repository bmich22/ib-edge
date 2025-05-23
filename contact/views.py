from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect


def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        if form.cleaned_data['bot_field']:
            # Detected spam bot — do NOT save or send
            return redirect('contact_success')

        # Legit user — process form
        contact = form.save()

        # Admin notification
        send_mail(
            subject="New Contact Message",
            message=f"From {contact.name} "
                    f"<{contact.email}>:\n\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )

        # Confirmation to user
        send_mail(
            subject="Thanks for contacting us!",
            message=f"Hi {contact.name},\n\nThanks for reaching out. "
                    f"We'll get back to you soon.\n\n"
                    f"Your message:\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
        )

        return redirect('contact_success')

    return render(request, 'contacts/contact.html', {'form': form})
