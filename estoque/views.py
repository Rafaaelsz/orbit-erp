from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from .models import Produto, Movimentacao
from .forms import ProdutoForm, MovimentacaoForm


@login_required
def dashboard(request):
    produtos = Produto.objects.all()

    # Lógica de Busca
    query = request.GET.get('q')
    if query:
        produtos = produtos.filter(nome__icontains=query)

    # Cálculos
    total_produtos = produtos.count()
    total_itens = produtos.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    valor_estoque = produtos.aggregate(
        total=Sum(F('quantidade') * F('preco_venda'))
    )['total'] or 0

    por_categoria = produtos.values(
        'categoria__nome').annotate(total=Sum('quantidade'))

    cat_labels = [item['categoria__nome']
                  for item in por_categoria if item['categoria__nome']]
    cat_data = [item['total']
                for item in por_categoria if item['categoria__nome']]

    context = {
        'produtos': produtos,
        'total_produtos': total_produtos,
        'total_itens': total_itens,
        'valor_estoque': valor_estoque,
        'query': query if query else '',
        'cat_labels': cat_labels,
        'cat_data': cat_data,
    }
    return render(request, 'estoque/dashboard.html', context)


@login_required
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            return redirect('dashboard')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/adicionar_produto.html', {'form': form})


@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/adicionar_produto.html', {'form': form})


@login_required
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('dashboard')


@login_required
def movimentar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.produto = produto
            movimentacao.usuario = request.user

            if movimentacao.tipo == 'E':  # Entrada
                produto.quantidade += movimentacao.quantidade
            elif movimentacao.tipo == 'S':  # Saída
                if produto.quantidade < movimentacao.quantidade:
                    return render(request, 'estoque/movimentar_produto.html', {
                        'form': form,
                        'produto': produto,
                        'erro': 'Saldo insuficiente em estoque!'
                    })
                produto.quantidade -= movimentacao.quantidade

            produto.save()
            movimentacao.save()
            return redirect('dashboard')
    else:
        form = MovimentacaoForm()

    return render(request, 'estoque/movimentar_produto.html', {'form': form, 'produto': produto})


@login_required
def historico_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    movimentacoes = Movimentacao.objects.filter(
        produto=produto).select_related('usuario').order_by('-data')

    return render(request, 'estoque/historico.html', {
        'produto': produto,
        'movimentacoes': movimentacoes
    })


@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto})


@login_required
def lista_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().select_related(
        'produto', 'usuario').order_by('-data')
    return render(request, 'estoque/lista_movimentacoes.html', {'movimentacoes': movimentacoes})
