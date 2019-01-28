from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import auth
from accounts.forms import RegistrationForm, Driver_Form, LoginForm, RequestForm
#we want to use data stored in the User model
#from django.contrib.auth.models import User
#deny some users(not logged in, etc)
#a decorator allows you to add some functions to a view
from django.contrib.auth.decorators import login_required
from accounts.models import UserInfo, Ride
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    numbers = [1, 2, 3, 4, 5]
    name = 'A.W'
    args = {'name': name, 'numbers': numbers}
    return render(request, 'accounts/home.html', args)

def register(request, isdriver=False):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password2']
            user = User.objects.create_user(username=username,
                    password=password, email=email, first_name=first_name,
                    last_name=last_name)
            user_profile = UserInfo(user=user)
            user_profile.vehicle_id = request.POST.get('vehicle_id', None)
            vehicle_max_passenger = request.POST.get('vehicle_max_passenger', None)
            user_profile.vehicle_max_passenger = vehicle_max_passenger
            user_profile.isDriver = True
            user_profile.save()
            auth.logout(request)
            return HttpResponseRedirect('/accounts/')
        else:
            return render(request, 'accounts/reg_form.html', {'form': form})
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

def driver_register(request):
    if request.method == 'POST':
        form = Driver_Form(request.POST)
        user_profile = UserInfo.objects.filter(user=request.user)[0]
        if form.is_valid():
            user_profile.vehicle_id = form.cleaned_data['vehicle_id']
            user_profile.vehicle_max_passenger = form.cleaned_data['vehicle_max_passenger']
            user_profile.isDriver = True
            user_profile.save()
            auth.logout(request)
            return HttpResponseRedirect('/accounts/')
        else:
            auth.logout(request)
            return HttpResponseRedirect('/accounts/')
    else:
        form = Driver_Form()
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def passenger_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/accounts/passenger')

            else:
                # 登陆失败
                  return render(request, 'accounts/passenger_login.html', {'form': form,
                               'message': 'Wrong password. Please try again.'})
    else:
        if request.user.is_authenticated :
            return HttpResponseRedirect('/accounts')
        else:
            form = LoginForm()

    return render(request, 'accounts/passenger_login.html', {'form': form})

def passenger_home(request):
    history_request_list = Ride.objects.filter(user=request.user, isFinished=True)
    current_request_list = Ride.objects.filter(user=request.user, isFinished=False)
    if current_request_list.count() == 0:
        current_request = None
    else:
        current_request = current_request_list[0]
    return render(request, 'accounts/passenger.html',
            {'history_request_list': history_request_list, 'current_request': current_request,
            'message': request.session.get('message', default=None)})

def make_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            #save_it = form.save(commit=False)
            newride = Ride(destination=form.cleaned_data['destination'],
                        arrival_time=form.cleaned_data['arrival_time'],
                        number_passenger=form.cleaned_data['number_passenger'],
                        passenger_id=request.user.id
                        )
            newride.save()
            newride.user.add(request.user)

            request.session['message'] = 'You have required a ride.'
            return HttpResponseRedirect('/accounts/passenger')
    else:
        requested_rides = Ride.objects.filter(user=request.user, isPicked=False)
        if len(requested_rides) != 0:
            request.session['message'] = 'You have unfinished ride.'
            return HttpResponseRedirect('/accounts/passenger')
        else:
            form = RequestForm()
            args = {'form': form}
            return render(request, 'accounts/make_request.html', args)

def edit_request(request, ride_id):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user_request = Ride.objects.filter(id=ride_id)[0]
            user_request.destination = form.cleaned_data['destination']
            user_request.arrival_time = form.cleaned_data['arrival_time']
            user_request.number_passenger = form.cleaned_data['number_passenger']
            user_request.vehicle_type = form.cleaned_data['vehicle_type']
            user_request.save()
            return redirect('../../../')

    else:
        user_request = Ride.objects.filter(id=ride_id)[0]
        form = RequestForm(instance=user_request)
        return render(request, 'accounts/edit_request.html', {'form':form})

def delete_request(request, ride_id):
    ride = Ride.objects.filter(id=ride_id);
    ride.delete()
    return HttpResponseRedirect('/accounts/passenger/')

def search_for_join(request):
    requested_rides = Ride.objects.filter(passenger_id=request.user.id, isFinished=False)
    if len(requested_rides) != 0:
        request.session['message'] = 'You have unfinished ride.'
        return HttpResponseRedirect('/accounts/passenger')
    else:
        ride_not_picked_list = Ride.objects.filter(isPicked=False)
        return render(request, 'accounts/search_join.html',
        {'ride_not_picked_list': ride_not_picked_list})

def join(request, ride_id):
    join_ride = Ride.objects.filter(id=ride_id)[0]
    if join_ride.isPicked == False and join_ride.isFinished == False:
        join_ride.number_passenger += 1;
        join_ride.user.add(request.user)
        join_ride.save()
        return HttpResponseRedirect('/accounts/passenger')
    else:
        request.session['message'] = 'Join failed'
        return HttpResponseRedirect('/accounts/passenger')

def driver_home(request):
    history_pickup_list = Ride.objects.filter(driver_id=request.user.id, isFinished=True)
    current_pickup_list = Ride.objects.filter(driver_id=request.user.id, isFinished=False)
    if current_pickup_list.count() == 0:
        current_pickup = None
    else:
        current_pickup = current_pickup_list[0]
    return render(request, 'accounts/driver.html',
            {'history_pickup_list': history_pickup_list, 'current_pickup': current_pickup,
            'message': request.session.get('message', default=None)})

def driver_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                userinfo = UserInfo.objects.filter(user=request.user)[0]
                if(userinfo.isDriver == True):
                    ride_list = Ride.objects.all()
                    return HttpResponseRedirect('/accounts/driver')
                else:
                    auth.logout(request)
                    return render(request, 'accounts/driver_login.html',
                    {'form': form, 'message': 'You are not a DRIVER.Please login as a passenger.'})
            else:
            # 登陆失败
              return render(request, 'accounts/driver_login.html', {'form': form,
                           'message': 'Wrong password. Please try again.'})

    else:
        if request.user.is_authenticated :
            return HttpResponseRedirect('/accounts/')
        else:
            form = LoginForm()
            return render(request, 'accounts/driver_login.html', {'form': form})

def search(request):
    picked_rides = Ride.objects.filter(driver_id=request.user.id, isFinished=False)
    requested_rides = Ride.objects.filter(user=request.user, isFinished=False)
    if len(picked_rides) != 0 or len(requested_rides) != 0:
        request.session['message'] = 'You have unfinished ride.'
        return HttpResponseRedirect('/accounts/driver')
    else:
        ride_not_picked_list = Ride.objects.filter(isPicked=False)
        return render(request, 'accounts/search_pickup.html',
        {'ride_not_picked_list': ride_not_picked_list})

def pickup(request, ride_id):
    selected_ride = Ride.objects.filter(id=ride_id)[0]
    driver_info = UserInfo.objects.filter(user=request.user)[0]
    if selected_ride.number_passenger <= driver_info.vehicle_max_passenger:
        selected_ride.isPicked = True
        selected_ride.driver_id = request.user.id
        selected_ride.save()
        return HttpResponseRedirect('/accounts/driver')
    else:
        return HttpResponseRedirect('/accounts')
        #return search(request, context={'message': 'You can\'t pick up that ride.'})

def finish(request, ride_id):
    selected_ride = Ride.objects.filter(id=ride_id)[0]
    if selected_ride.isFinished == False:
        selected_ride.isFinished = True
        selected_ride.save()
        return HttpResponseRedirect('/accounts/driver')
    else:
        return HttpResponseRedirect('/accounts/driver')


@login_required
def view_profile(request):
    user_info = UserInfo.objects.filter(user=request.user)[0]
    args = {'user': request.user, 'user_info':user_info}
    return render(request, 'accounts/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)
