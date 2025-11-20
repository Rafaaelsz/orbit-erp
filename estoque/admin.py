from django.contrib import admin
from .models import Produto, Categoria, Movimentacao
from django.utils.html import mark_safe

admin.site.site_header = "Administração do Estoque"
admin.site.site_title = "Sistema de Estoque"
admin.site.index_title = "Gerenciamento do Sistema"


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('imagem_preview', 'nome', 'categoria',
                    'quantidade', 'preco_venda', 'status_formatado')

    list_filter = ('categoria',)

    search_fields = ['nome']

    list_display_links = ('imagem_preview', 'nome')

    list_per_page = 10

    def imagem_preview(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />')
        return "Sem Foto"

    imagem_preview.short_description = "Foto"

    def status_formatado(self, obj):
        status = obj.status_estoque
        if status['texto'] == 'ZERADO':
            return mark_safe(f'<span style="color: red; font-weight: bold;">ZERADO</span>')
        return status['texto']

    status_formatado.short_description = "Status"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ['nome']


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'get_tipo_display',
                    'produto', 'quantidade', 'usuario')
    list_filter = ('tipo', 'data')
    search_fields = ['produto__nome']
