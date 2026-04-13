from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    # Adicionamos um prefixo para a categoria (ex: 'LAR' para Laranjas)
    prefixo = models.CharField(max_length=3, help_text="Ex: LAR, ADU, PRG", blank=True, null=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome_empresa = models.CharField(max_length=200)
    contacto = models.CharField(max_length=50)
    email = models.EmailField()
    tempo_entrega_dias = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome_empresa

class Produto(models.Model):
    id_produto = models.CharField(max_length=50, unique=True, blank=True) # Código Único (Auto-gerado se vazio)
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.PositiveIntegerField(default=5)

    def save(self, *args, **kwargs):
        # Só geramos o SKU/id_ produto, whatevesser kkkkkkk. se o objeto for novo (não tiver ID)
        # E se o id_produto não foi fornecido manualmente
        if not self.id and not self.id_produto:
            # Verifica se a categoria e o seu prefixo existem antes de tentar gerar o id_produto
            if self.categoria and self.categoria.prefixo:
                # 1. Pegar o prefixo da categoria (em maiúsculas)
                prefixo = self.categoria.prefixo.upper()
                
                # 2. Contar quantos produtos já existem nesta categoria para gerar o próximo número
                total_na_categoria = Produto.objects.filter(categoria=self.categoria).count()
                proximo_numero = total_na_categoria + 1
                
                # 3. Formatar o id_produto: Prefixo + Hífen + Número com 3 casas decimais (001, 002...). Sou bom kota kkk.
                # O zfill(3) garante que o 1 vire 001
                self.id_produto = f"{prefixo}-{str(proximo_numero).zfill(3)}"
            
        super(Produto, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_produto} - {self.nome}"
    @property
    def stock_atual(self):
        entradas = Movimentacao.objects.filter(produto=self, tipo='E').aggregate(models.Sum('quantidade'))['quantidade__sum'] or 0
        saidas = Movimentacao.objects.filter(produto=self, tipo='S').aggregate(models.Sum('quantidade'))['quantidade__sum'] or 0
        return entradas - saidas

    def __str__(self):
        return f"{self.id_produto} - {self.nome}"
    
class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    data = models.DateTimeField(auto_now_add=True)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    motivo = models.CharField(max_length=255, help_text="Ex: Venda, Reposição, Perda")

    class Meta:
        verbose_name_plural = "Movimentações"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"


    