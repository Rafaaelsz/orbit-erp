from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField(default=0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def lucro(self):
        """Calcula o lucro líquido em Reais"""
        return self.preco_venda - self.preco_custo

    @property
    def margem(self):
        """Calcula a margem de lucro em %"""
        if self.preco_venda > 0:
            margem_bruta = (self.lucro / self.preco_venda) * 100
            return round(margem_bruta, 1)
        return 0

    @property
    def status_estoque(self):
        """Define a cor e o texto do status"""
        if self.quantidade <= 0:
            return {'classe': 'bg-red-100 text-red-800 border-red-200', 'texto': 'ZERADO'}
        elif self.quantidade < 5:
            return {'classe': 'bg-yellow-100 text-yellow-800 border-yellow-200', 'texto': 'BAIXO'}
        else:
            return {'classe': 'bg-green-100 text-green-800 border-green-200', 'texto': 'OK'}


class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada (Compra/Devolução)'),
        ('S', 'Saída (Venda/Perda)'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"
