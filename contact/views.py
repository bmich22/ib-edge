from django.shortcuts import render

# Create your views here.


def contact(request):
    """ A view to return the reviews page """
    
    return render(request, 'contacts/contact.html')