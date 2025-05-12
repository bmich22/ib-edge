from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from checkout.models import Purchase
from tutoring_sessions.models import TutoringSession

@login_required
def user_profile(request):
    # Ensure the profile exists
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Superusers skip the form
    if request.user.is_superuser:
        return render(request, 'user_profiles/admin_dashboard.html')

    is_editing = request.GET.get('edit') == '1'

    # Regular users get the form
    form = UserProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated successfully!")
        return redirect('user_profile')

    # Show form if it's missing key info OR user clicked to edit form
    show_form = is_editing or not profile.subjects.exists() or not profile.parent_email

    # Get user's purchases, newest first
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_on')

    # Get user's logged sessions
    sessions = TutoringSession.objects.filter(purchase__user=request.user).order_by('-session_datetime')

    return render(request, 'user_profiles/user_profile.html', {
        'form': form,
        'show_form': show_form,
        'is_editing': is_editing,
        'profile': profile,
        'purchases': purchases,
})
