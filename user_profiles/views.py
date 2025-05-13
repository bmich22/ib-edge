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

    # Superusers and tutors skip the form
    if request.user.is_superuser:
        return render(request, 'user_profiles/admin_dashboard.html')
    elif request.user.userprofile.is_tutor:
        return render(request, 'user_profiles/tutor_dashboard.html')
    
    is_editing = request.GET.get('edit') == '1'
    form = UserProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated successfully!")
        return redirect('user_profile')

    show_form = is_editing or not profile.subjects.exists() or not profile.parent_email

    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_on')

    sessions = TutoringSession.objects.filter(user=request.user).order_by('-session_datetime')

    total_sessions_available = profile.get_total_sessions_available()

    return render(request, 'user_profiles/user_profile.html', {
        'form': form,
        'show_form': show_form,
        'is_editing': is_editing,
        'profile': profile,
        'purchases': purchases,
        'sessions': sessions,
        'total_sessions_available': total_sessions_available,
})
