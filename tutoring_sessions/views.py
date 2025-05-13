from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LogSessionForm
from .models import TutoringSession

@login_required
def log_tutoring_session(request):
    # Only allow tutors or superusers to log sessions
    if not (request.user.is_superuser or request.user.userprofile.is_tutor):
        raise PermissionDenied("Only tutors can log sessions.")

    if request.method == 'POST':
        form = LogSessionForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            session_datetime = form.cleaned_data['session_datetime']
            notes = form.cleaned_data['notes']

            # Create session record
            TutoringSession.objects.create(
                user=student,
                session_datetime=session_datetime,
                notes=notes,
                logged_by=request.user
            )

            # Decrement student session count
            profile = student.userprofile
            profile.total_sessions_available = max(0, profile.total_sessions_available - 1)
            profile.save()

            messages.success(request, f"Session logged for {student.username}")
            return redirect('log_tutoring_session')
    else:
        form = LogSessionForm()

    return render(request, 'tutoring_sessions/log_session.html', {'form': form})