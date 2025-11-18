from django.shortcuts import render
from .models import Produto
from django.db.models import Sum, F


def dashboard(request):
    produtos = Produto.objects.all()

    total_produtos = produtos.count()

    total_itens = produtos.aggregate(Sum('quantidade'))[
        ('quantidade__sum')] or 0

    valor_estoque = produtos.aggregate(
        total=Sum(F("quantidade") * F('preco_venda')))['total'] or 0

    context = {
        'produtos': produtos,
        'total_produtos': total_produtos,
        'total_itens': total_itens,
        'valor_estoque': valor_estoque
    }

    return render(request, 'estoque/dashboard.html', context)
