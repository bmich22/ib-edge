from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LogSessionForm

# Create your views here.

@staff_member_required
def log_tutoring_session(request):
    if request.method == 'POST':
        form = LogSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.logged_by = request.user
            session.save()
            messages.success(request, "Tutoring session logged successfully.")
            return redirect('log_tutoring_session')
    else:
        form = LogSessionForm()

    return render(request, 'tutoring_sessions/log_session.html', {'form': form})
