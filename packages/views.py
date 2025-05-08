from django.shortcuts import render

# Create your views here.


def packages(request):
    """ A view to return the packages page """
    
    return render(request, 'packages/packages.html')



