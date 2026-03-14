from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from funcionarios.models import Funcionarios
# Create your views here.

@login_required(login_url="loginPage")
def rhPage(request):

    context = {
        'funcionarios': Funcionarios.objects.all().filter(avaliacao__gte=4.5).order_by('-avaliacao'), 
    }

    return render(request, "rh/rh.html", context)