from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def cronosPage(request):
    return render(request, "cronos/agente-ia.html")