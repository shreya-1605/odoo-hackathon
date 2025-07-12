from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from skills.models import Skill
from .forms import FeedbackForm

@login_required
def leave_feedback(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.skill = skill
            feedback.save()
            return redirect('skill_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form, 'skill': skill})
