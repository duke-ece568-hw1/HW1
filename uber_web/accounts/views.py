from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#django has two types of views: function based view and class based view
def home(request):
    numbers = [1, 2, 3, 4, 5]
    name = 'A.W'
    args = {'name': name, 'numbers': numbers}
    return render(request, 'accounts/home.html', args)
