from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="loginPage")
def rhPage(request):
    return render(request, "rh/rh.html")