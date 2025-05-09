from django.shortcuts import render, get_object_or_404, redirect
from .models import Package
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import PackageForm


# Create your views here.


def packages(request):
    """ A view to return the packages page """
    
    packages = Package.objects.all()
    return render(request, 'packages/packages.html', {'packages': packages})


def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'packages/package_detail.html', {'package': package})


@staff_member_required
def add_package(request):
    form = PackageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Package added successfully!")
        return redirect('packages')
    return render(request, 'packages/package_form.html', {'form': form, 'title': 'Add Package'})


@staff_member_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    form = PackageForm(request.POST or None, instance=package)
    if form.is_valid():
        form.save()
        messages.success(request, "Package updated successfully!")
        return redirect('packages')
    return render(request, 'packages/package_form.html', {'form': form, 'title': 'Edit Package'})


@staff_member_required
def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        package.delete()
        messages.success(request, f"'{package.name}' was deleted.")
        return redirect('packages')
    return render(request, 'packages/package_confirm_delete.html', {'package': package})


