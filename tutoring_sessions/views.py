from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LogSessionForm
from user_profiles.models import UserProfile
from tutoring_sessions.models import TutoringSession

# Create your views here.

@staff_member_required
def log_tutoring_session(request):
    if request.method == 'POST':
        form = LogSessionForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            session_datetime = form.cleaned_data['session_datetime']
            notes = form.cleaned_data['notes']

            TutoringSession.objects.create(
                user=student,
                session_datetime=session_datetime,
                notes=notes,
                logged_by=request.user
            )

            # Decrement session count
            profile = student.userprofile
            profile.total_sessions_available = max(0, profile.total_sessions_available - 1)
            profile.save()

            messages.success(request, f"Session logged for {student.get_full_name() or student.username}.")
            return redirect('log_tutoring_session')
    else:
        form = LogSessionForm()

    return render(request, 'tutoring_sessions/log_session.html', {'form': form})