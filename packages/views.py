from django.shortcuts import render
from .models import Package

# Create your views here.


def packages(request):
    """ A view to return the packages page """
    
    packages = Package.objects.all()
    return render(request, 'packages/packages.html', {'packages': packages})




