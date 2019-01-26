from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserInfo

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    isDriver = forms.BooleanField(required=False)


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
class EditForm(UserChangeForm):
    pass
