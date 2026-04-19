from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from users.models import Users
from funcionarios.models import Funcionarios
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
User = get_user_model()


context = {
    
}

@login_required(login_url="loginPage")
def sistemaPage(request):
    if request.user.tipo not in ['admin', 'Programador']:
        messages.error(request, 'Acesso negado.')
        return redirect('agente-ia')
    
    # Otimização: select_related para carregar os dados do funcionário e cargo de uma vez
    users = Users.objects.all().select_related('f_id').order_by('-date_joined')
    
    # Procurar todos os funcionários para preencher o dropdown
    funcionarios = Funcionarios.objects.all().select_related('cargo').order_by('f_nome')
    
    return render(request, "definicoes/definicoes.html", {
        'users': users, 
        'funcionarios': funcionarios
    })

@csrf_exempt
@login_required(login_url="loginPage")
def create_user(request):
    if request.user.tipo not in ['admin', 'Programador']:
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            tipo = request.POST.get('tipo', 'rh')
            nivel = request.POST.get('nivel', 'operario')
            
            if password1 != password2:
                messages.error(request, "As senhas não coincidem.")
            
            if Users.objects.filter(username=username).exists():
                messages.error(request, "Utilizador já existe")
            
            user = Users.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
                tipo=tipo,
                nivel=nivel
            )
            # f_id optional, set if provided (as ID)
            f_id_str = request.POST.get('f_id', '').strip()
            if f_id_str:
                try:
                    f_id = int(f_id_str)
                    funcionario = Funcionarios.objects.get(f_id=f_id)
                    user.f_id = funcionario
                    user.save()
                except (ValueError, Funcionarios.DoesNotExist):
                    pass  # Ignore invalid f_id
            
            messages.success(request, 'Utilizador criado com sucesso.')
        except Exception as e:
             messages.error(request, f"Erro ao registar Utilizador: {e}")
    return redirect('sistema')
