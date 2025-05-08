from django.shortcuts import render

# Create your views here.


def faq(request):
    """ A view to return the reviews page """
    
    return render(request, 'faqs/faq.html')