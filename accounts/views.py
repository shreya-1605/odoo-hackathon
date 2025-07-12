from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, ProfileForm
from .models import Profile
from skills.models import Skill  # ✅ Correct position

# 🔹 User Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)  # Create empty profile
            messages.success(request, '✅ User created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# 🔹 User Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, '✅ Logged in successfully!')
            return redirect('profile')  # Redirect to complete profile
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# 🔹 Home Page View
def home_view(request):
    return render(request, 'accounts/home.html')

# 🔹 User Logout View
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# 🔹 Profile View (Create/Update)
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    user_skills = Skill.objects.filter(user=request.user)  # ✅ Fetch user’s skills

    return render(request, 'accounts/profile.html', {
        'form': form,
        'skills': user_skills
    })
