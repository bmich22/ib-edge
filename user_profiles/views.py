from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages

@login_required
def user_profile(request):
    profile = request.user.userprofile  # assumes OneToOneField
    form = UserProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated successfully!")
        return redirect('user_profile')  # redirect to the same page after saving

    return render(request, 'user_profiles/user_profile.html', {'form': form})
