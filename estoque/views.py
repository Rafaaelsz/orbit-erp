from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Produto, Movimentacao, Categoria
from .forms import ProdutoForm, MovimentacaoForm, CategoriaForm
from django.contrib import messages
import csv


@login_required
def dashboard(request):
    produtos = Produto.objects.all()
    query = request.GET.get('q')
    if query:
        produtos = produtos.filter(nome__icontains=query)

    total_produtos = produtos.count()
    total_itens = produtos.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    valor_estoque = produtos.aggregate(
        total=Sum(F('quantidade') * F('preco_venda')))['total'] or 0

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
            messages.success(request, 'Produto adicionado com sucesso!')
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
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('dashboard')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/adicionar_produto.html', {'form': form})


@login_required
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
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

            if movimentacao.tipo == 'E':
                produto.quantidade += movimentacao.quantidade
                messages.success(
                    request, f'Entrada de {movimentacao.quantidade} itens realizada!')
            elif movimentacao.tipo == 'S':
                if produto.quantidade < movimentacao.quantidade:
                    messages.error(
                        request, 'Erro: Saldo insuficiente para essa saída.')
                    return render(request, 'estoque/movimentar_produto.html', {'form': form, 'produto': produto, 'erro': 'Saldo insuficiente!'})
                produto.quantidade -= movimentacao.quantidade
                messages.success(
                    request, f'Saída de {movimentacao.quantidade} itens realizada!')

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
    return render(request, 'estoque/historico.html', {'produto': produto, 'movimentacoes': movimentacoes})


@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto})


@login_required
def lista_movimentacoes(request):
    movimentacoes = Movimentacao.objects.all().select_related(
        'produto', 'usuario').order_by('-data')
    return render(request, 'estoque/lista_movimentacoes.html', {'movimentacoes': movimentacoes})


@login_required
def relatorio_pdf(request):
    produtos = Produto.objects.all().order_by('nome')
    total_itens = produtos.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    valor_estoque = produtos.aggregate(
        total=Sum(F('quantidade') * F('preco_venda')))['total'] or 0
    template_path = 'estoque/relatorio_pdf.html'
    context = {'produtos': produtos, 'total_itens': total_itens,
               'valor_estoque': valor_estoque}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_estoque.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF <pre>' + html + '</pre>')
    return response


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nome')
    return render(request, 'estoque/lista_categorias.html', {'categorias': categorias})


@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'estoque/categoria_form.html', {'form': form})


@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'estoque/categoria_form.html', {'form': form})


@login_required
def deletar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('lista_categorias')


@login_required
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="estoque.csv"'

    writer = csv.writer(response)
    writer.writerow(['Produto', 'Categoria', 'Quantidade',
                    'Preço Custo', 'Preço Venda', 'Lucro (R$)', 'Margem (%)'])
    produtos = Produto.objects.all().order_by('nome')

    for produto in produtos:
        writer.writerow([
            produto.nome,
            produto.categoria.nome if produto.categoria else 'Sem Categoria',
            produto.quantidade,
            produto.preco_custo,
            produto.preco_venda,
            produto.lucro,
            produto.margem,
        ])

    return response
