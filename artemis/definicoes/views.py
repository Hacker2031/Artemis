from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from users.models import Users
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
User = get_user_model()

@login_required(login_url="loginPage")
def sistemaPage(request):
    if request.user.tipo not in ['admin', 'Programador']:
        messages.error(request, 'Acesso negado.')
        return redirect('Dashboard')
    users = Users.objects.all().order_by('-date_joined')
    return render(request, "definicoes/definicoes.html", {'users': users})

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
                return JsonResponse({'error': 'As senhas não coincidem.'})
            
            if Users.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Usuário já existe.'})
            
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
                    from funcionarios.models import Funcionarios
                    funcionario = Funcionarios.objects.get(f_id=f_id)
                    user.f_id = funcionario
                    user.save()
                except (ValueError, Funcionarios.DoesNotExist):
                    pass  # Ignore invalid f_id
            
            return JsonResponse({'success': True, 'user': {
                'username': user.username,
                'name': f"{user.first_name} {user.last_name}".strip(),
                'email': user.email,
                'tipo': user.get_tipo_display(),
                'nivel': user.get_nivel_display(),
                'f_id': user.f_id.f_id if user.f_id else None
            }})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método inválido.'}, status=405)
