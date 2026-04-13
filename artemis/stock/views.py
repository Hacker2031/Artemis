from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from .models import Produto, Categoria, Fornecedor, Movimentacao
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

@login_required(login_url='loginPage')
def stockPage(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    
    movimentacoes = Movimentacao.objects.all().order_by('-data')[:15]

    esgotados = [p for p in produtos if p.stock_atual == 0]
    baixo_stock = [p for p in produtos if 0 < p.stock_atual <= p.stock_minimo]
    alertas = esgotados + baixo_stock  # Mantido para compatibilidade se necessário
    

    total_stock = sum(p.stock_atual for p in produtos)
    
    # 3. Calculation for Total Value (Keep as is)
    valor_total = sum(p.stock_atual * p.preco_custo for p in produtos)

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'movimentacoes': movimentacoes,
        'fornecedores': fornecedores,
        'alertas': alertas,
        'esgotados_count': len(esgotados),
        'baixo_stock_count': len(baixo_stock),
        'total_stock': total_stock,
        'valor_total': valor_total,
    }
    return render(request, "stock/stock.html", context)

@login_required(login_url='loginPage')
def adicionarProduto(request):
    # Cria novo produto via formulario POST
    if request.method == "POST":
        try:
            id_db = request.POST.get('id')  # ID do banco de dados para edição
            id_manual = request.POST.get('id_produto')
            
            if id_db:
                produto = get_object_or_404(Produto, id=id_db)
                msg = "Produto atualizado com sucesso"
            else:
                produto = Produto()
                msg = "Produto registado com sucesso"

            produto.nome = request.POST.get('nome')
            produto.categoria_id = request.POST.get('categoria')
            produto.fornecedor_id = request.POST.get('fornecedor')
            produto.preco_custo = request.POST.get('preco_custo')
            produto.stock_minimo = request.POST.get('stock_minimo', 5)
            
            if id_manual:
                produto.id_produto = id_manual
                
            produto.save()
            messages.success(request, msg)
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

@login_required(login_url='loginPage')
def adicionarFornecedor(request):
    if request.method == "POST":
        try:
            id_db = request.POST.get('id')
            if id_db:
                forn = get_object_or_404(Fornecedor, id=id_db)
                msg = "Fornecedor atualizado com sucesso"
            else:
                forn = Fornecedor()
                msg = "Fornecedor registado com sucesso"

            forn.nome_empresa = request.POST.get('nome_empresa')
            forn.contacto = request.POST.get('contacto')
            forn.email = request.POST.get('email')
            forn.tempo_entrega_dias = request.POST.get('tempo_entrega_dias', 0)
            
            forn.save()
            messages.success(request, msg)
        except Exception as e:
            messages.error(request, f"Erro ao registar fornecedor: {e}")
    return redirect('stock')


@login_required(login_url='loginPage')
def export_inventario(request):
    produtos = Produto.objects.all().order_by('nome')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventario_stock.pdf"'

    doc      = SimpleDocTemplate(response, pagesize=letter)
    styles   = getSampleStyleSheet()
    elements = [Paragraph("Relatório de Inventário de Stock", styles['Title'])]

    # Cabeçalhos da tabela
    data = [['ID Produto', 'Nome', 'Categoria', 'Stock Atual', 'Stock Mínimo','Preço Custo', 'Valor Total']]
    
    total_geral = 0
    for p in produtos:
        stock = p.stock_atual
        stock_min = p.stock_minimo
        valor_item = stock * p.preco_custo
        total_geral += valor_item
        
        categoria_nome = p.categoria.nome if p.categoria else 'N/A'
        data.append([p.id_produto, p.nome, categoria_nome, str(stock), str(stock_min), f"{p.preco_custo} Kz", f"{valor_item} Kz"])

    data.append(['', '', '', '', '', 'TOTAL GERAL:', f"{total_geral} Kz"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR',     (0, 0), (-1, 0), (0, 0, 0)),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND',    (0, 1), (-1, -1), (0.95, 0.95, 0.95)),
        ('GRID',          (0, 0), (-1, -1), 1, (0, 0, 0)),
        ('FONTNAME',      (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 1), (-1, -1), 10),
    ]))

    elements.append(table)
    doc.build(elements)
    
    return response
