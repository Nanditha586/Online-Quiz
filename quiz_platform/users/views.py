from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import (StudentRegisterForm,StaffRegisterForm)

from quizzes.models import (StudentProfile,StaffProfile,UserRole)
def home(request):

    return render(
        request,
        'home.html'
    )


def register_choice(request):

    return render(
        request,
        'register_choice.html'
    )


def student_register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(
                request,
                'student_register.html',
                {'error': 'Passwords do not match'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        UserRole.objects.create(
            user=user,
            role='student'
        )

        StudentProfile.objects.create(
            user=user,
            branch=request.POST['branch'],
            year=request.POST['year'],
            
        )

        return redirect('login')

    return render(
        request,
        'student_register.html'
    )

def staff_register(request):

    if request.method == "POST":

        form = StaffRegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            UserRole.objects.create(
                user=user,
                role='staff'
            )

            StaffProfile.objects.create(
                user=user
            )

            return redirect('login')

    else:

        form = StaffRegisterForm()

    return render(
        request,
        'staff_register.html',
        {'form': form}
    )


from django.contrib import messages



def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            role = UserRole.objects.filter(
                user=user
            ).first()

            if role and role.role == 'staff':

                return redirect(
                    'analytics_dashboard'
                )

            return redirect(
                'user_dashboard'
            )

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        'login.html'
    )

def user_logout(request):

    logout(request)

    return redirect('login')

from django.contrib.auth.decorators import login_required
from quizzes.models import StudentProfile

@login_required
def student_profile(request):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        profile.branch = request.POST.get(
            'branch'
        )

        profile.year = request.POST.get(
            'year'
        )

        new_password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if new_password:

            if new_password == confirm_password:

                request.user.set_password(
                    new_password
                )

                request.user.save()

        profile.save()

        return redirect(
            'login'
        )

    return render(
        request,
        'student_profile.html',
        {
            'profile': profile
        }
    )