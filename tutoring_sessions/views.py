from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LogSessionForm
from .models import TutoringSession
from user_profiles.models import UserProfile
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import make_aware


@login_required
def log_tutoring_session(request):
    # Only allow tutors or superusers to log sessions
    if not (request.user.is_superuser or request.user.userprofile.is_tutor):
        raise PermissionDenied("Only tutors can log sessions.")

    if request.method == 'POST':
        form = LogSessionForm(request.POST)
        if form.is_valid():
            profile = form.cleaned_data['student']
            session_date = form.cleaned_data['session_date']
            session_time = form.cleaned_data['session_time']
            session_time_obj = datetime.strptime(
                session_time, "%H:%M:%S").time()
            session_datetime = make_aware(
                datetime.combine(session_date, session_time_obj))
            notes = form.cleaned_data['notes']

            TutoringSession.objects.create(
                user=profile.user,
                session_datetime=session_datetime,
                notes=notes,
                logged_by=request.user
            )

            # Decrement student session count
            profile.total_sessions_available = max(
                0, profile.total_sessions_available - 1)
            profile.save()

            messages.success(
                request, f"Session logged for {profile.user.username}")
            return redirect('log_tutoring_session')
    else:
        form = LogSessionForm()

    return render(
        request, 'tutoring_sessions/log_session.html', {'form': form})
