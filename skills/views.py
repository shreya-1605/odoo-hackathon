from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Skill
from .forms import SkillForm

# 🔹 List all skills (Public view)
def skill_list(request):
    skills = Skill.objects.all().order_by('-created_at')
    return render(request, 'skills/skill_list.html', {'skills': skills})

# 🔹 Add a new skill (Only logged-in users)
@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, "✅ Skill posted successfully!")
            return redirect('skill_list')
    else:
        form = SkillForm()
    return render(request, 'skills/add_skill.html', {'form': form})

# 🔹 Edit a skill (Only owner can edit)
@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Skill updated!")
            return redirect('skill_list')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'skills/edit_skill.html', {'form': form})  # make sure template name is correct

# 🔹 Delete a skill (Only owner can delete)
@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "❌ Skill deleted!")
        return redirect('skill_list')
    return render(request, 'skills/delete_skill.html', {'skill': skill})

# 🔹 View details of a skill (Public)
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    # Optional: If you have related feedbacks, show them
    feedbacks = getattr(skill, 'feedbacks', None)
    if feedbacks:
        feedbacks = feedbacks.all().order_by('-created_at')
    else:
        feedbacks = []

    context = {
        'skill': skill,
        'feedbacks': feedbacks,
    }
    return render(request, 'skills/skill_detail.html', context)
