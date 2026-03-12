from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def stockPage(request):
    return render(request, "stock/stock.html")