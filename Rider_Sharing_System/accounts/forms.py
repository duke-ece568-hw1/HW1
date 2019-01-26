from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserInfo, Ride

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
#    isDriver = forms.BooleanField(required=False)


    class Meta:
        model = User
        fields = (
            'username','first_name','last_name','email','password1','password2',
#            'isDriver','vehicle_max_passenger','vehicle_id',
            )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
                          #prevent hacking
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):
    vehicle_id = forms.CharField(required=True)
    vehicle_max_passenger = forms.IntegerField(required=True)
    class Meta:
        model = UserInfo
        fields = (
            'vehicle_id',
            'vehicle_max_passenger',
        )

class Driver_Form(forms.ModelForm):
        vehicle_id = forms.CharField(required=True)
        vehicle_max_passenger = forms.IntegerField(required=True)

        class Meta:
            model = UserInfo
            fields = (
                'vehicle_id',
                'vehicle_max_passenger',
            )

class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules
    """
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("This email does not exist.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                           raise forms.ValidationError("This username does not exist. Please register first.")

        return username
    """
class RequestForm(forms.ModelForm):

    destination = forms.CharField(required=True)
    arrival_time = forms.CharField(required=True)
    number_passenger = forms.IntegerField(required=True)
    vehicle_type = forms.CharField(required=False)

    class Meta:
        model = Ride
        fields = (
            'destination',
            'arrival_time',
            'number_passenger',
            'vehicle_type',
        )
