from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from .models import Produto, Categoria, Fornecedor, Movimentacao

@login_required(login_url='loginPage')
def stockPage(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    
    # 1. Calculation for Alerts (Keep as is, it uses the property correctly)
    alertas = [p for p in produtos if p.stock_atual <= p.stock_minimo]
    
    # 2. FIX: Use Python's sum() instead of aggregate()
    # This calls the @property stock_atual for every product in the list
    total_stock = sum(p.stock_atual for p in produtos)
    
    # 3. Calculation for Total Value (Keep as is)
    valor_total = sum(p.stock_atual * p.preco_custo for p in produtos)

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'fornecedores': fornecedores,
        'alertas': alertas,
        'total_stock': total_stock,
        'valor_total': valor_total,
    }
    return render(request, "stock/stock.html", context)

@login_required(login_url='loginPage')
def adicionarProduto(request):
    # Cria novo produto via formulario POST
    if request.method == "POST":
        try:
            Produto.objects.create(
                id_produto=request.POST.get('id_produto'),
                nome=request.POST.get('nome'),
                categoria_id=request.POST.get('categoria'),
                fornecedor_id=request.POST.get('fornecedor'),
                preco_custo=request.POST.get('preco_custo'),
                stock_minimo=request.POST.get('stock_minimo', 5)
            )
            messages.success(request, "Produto registado com sucesso")
        except Exception as e:
            messages.error(request, f"Erro ao registar produto: {e}")
    return redirect('stock')

@login_required(login_url='loginPage')
def registarMovimentacao(request):
    # Processa entradas (E) ou saidas (S) de stock
    if request.method == "POST":
        try:
            p_id = request.POST.get('produto_id')
            qtd = int(request.POST.get('quantidade'))
            tipo = request.POST.get('tipo')
            produto = get_object_or_404(Produto, id=p_id)

            # Valida disponibilidade em caso de saida
            if tipo == 'S' and produto.stock_atual < qtd:
                messages.error(request, f"Stock insuficiente para {produto.nome}")
                return redirect('stock')

            Movimentacao.objects.create(
                produto=produto,
                quantidade=qtd,
                tipo=tipo,
                motivo=request.POST.get('motivo')
            )
            messages.success(request, "Movimentacao concluida")
        except Exception as e:
            messages.error(request, f"Erro na movimentacao: {e}")
    return redirect('stock')