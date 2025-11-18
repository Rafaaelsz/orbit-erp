from django.contrib import admin
from .models import Produto, Categoria


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'preco_venda')
    search_fields = ['nome"']
    list_filter = ['categoria']


admin.site.register(Categoria)
