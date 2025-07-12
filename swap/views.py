from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Swap
from .forms import SwapForm
from skills.models import Skill


# 🔹 View all swaps (for browsing or admin-style overview)
def swap_list(request):
    swaps = Swap.objects.all().order_by('-created_at')
    return render(request, 'swap/swap_list.html', {'swaps': swaps})


# 🔹 Initiate a swap (send skill from sender to receiver)
@login_required
def initiate_swap(request, skill_id, receiver_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    receiver = get_object_or_404(User, id=receiver_id)

    # Prevent sending to self
    if receiver == request.user:
        messages.warning(request, "⚠️ You cannot swap with yourself.")
        return redirect('skill_list')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        Swap.objects.create(
            sender=request.user,
            receiver=receiver,
            skill=skill,
            message=message
        )
        messages.success(request, f"✅ Swap request sent to {receiver.username}!")
        return redirect('skill_list')

    return render(request, 'swap/initiate_swap.html', {
        'skill': skill,
        'receiver': receiver
    })


# 🔹 Complete the swap: transfer skill to receiver and mark completed
@login_required
def complete_swap(request, swap_id):
    swap = get_object_or_404(Swap, id=swap_id, receiver=request.user)

    if swap.is_completed:
        messages.info(request, "ℹ️ This swap is already completed.")
        return redirect('profile')

    # Transfer ownership of skill
    skill = swap.skill
    skill.user = request.user  # Assign to receiver
    skill.save()

    swap.is_completed = True
    swap.save()

    messages.success(request, f"🎉 You now own the skill: {skill.title}")
    return redirect('profile')


# 🔹 Delete your own swap (sender or receiver)
@login_required
def delete_swap(request, swap_id):
    swap = get_object_or_404(Swap, id=swap_id)
    if swap.sender != request.user and swap.receiver != request.user:
        messages.error(request, "❌ You don't have permission to delete this swap.")
        return redirect('swap_list')

    if request.method == 'POST':
        swap.delete()
        messages.success(request, "🗑️ Swap deleted.")
        return redirect('swap_list')

    return render(request, 'swap/delete_swap.html', {'swap': swap})


# 🔹 View your own sent and received swaps
@login_required
def my_swaps(request):
    sent_swaps = Swap.objects.filter(sender=request.user).order_by('-created_at')
    received_swaps = Swap.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'swap/my_swaps.html', {
        'sent_swaps': sent_swaps,
        'received_swaps': received_swaps
    })
