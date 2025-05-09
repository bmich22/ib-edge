from django.shortcuts import render
from .models import Package

# Create your views here.


def packages(request):
    """ A view to return the packages page """
    
    return render(request, 'packages/packages.html')


def package_list(request):
    packages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': packages})




