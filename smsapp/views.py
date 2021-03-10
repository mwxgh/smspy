from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from smsapp.emailbackend import EmailBackEnd
from django.contrib import messages
from django.urls import reverse
# Create your views here.


def Login(request):
    return render(request, 'login.html')


def DoLogin(request):
    if request.method != 'POST':
        return HttpResponse('<h2> Method Not Allowed </h2>')
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('adminhome'))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('staffhome'))
            else:
                return HttpResponseRedirect(reverse('studenthome'))
        else:
            messages.error(request, 'Invaild Login Details')
            return HttpResponseRedirect('/')


def LogOut(request):
    logout(request)
    return HttpResponseRedirect('/')
