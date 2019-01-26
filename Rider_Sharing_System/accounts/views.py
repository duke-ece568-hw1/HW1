from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.forms import RegistrationForm, Driver_Form
#we want to use data stored in the User model
#from django.contrib.auth.models import User
#deny some users(not logged in, etc)
#a decorator allows you to add some functions to a view
from django.contrib.auth.decorators import login_required
from accounts.models import UserInfo
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    numbers = [1, 2, 3, 4, 5]
    name = 'A.W'
    args = {'name': name, 'numbers': numbers}
    return render(request, 'accounts/home.html', args)

def register(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/')

            #return redirect('/accounts')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

# @login_required
def driver_register(request):
    if request.method == 'POST':
        form = Driver_Form(request.POST)
        #user = get_object_or_404(User,user=request.user)
        user_profile = get_object_or_404(UserInfo, user=request.user)
        """
        if form.is_valid():
            user_profile.vehicle_id = form.cleaned_data['vehicle_id']
            user_profile.vehicle_max_passenger = form.cleaned_data['vehicle_max_passenger']
            user_profile.save()
            """
        return HttpResponseRedirect('/accounts/')
    else:
        form = Driver_Form(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        #take posted data in the request
        #representing the currently logged-in user.
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)
