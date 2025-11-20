from django import forms
from .models import Produto, Movimentacao


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'quantidade',
                  'preco_custo', 'preco_venda', 'imagem']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'categoria': forms.Select(attrs={'class': 'w-full p-2 border rounded mb-4 bg-white'}),
            'quantidade': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'imagem': forms.FileInput(attrs={'class': 'w-full p-2 border rounded mb-4 bg-white'}),
        }


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['tipo', 'quantidade']

        widgets = {
            'tipo': forms.Select(attrs={'class': 'w-full p-2 border rounded mb-4 bg-white'}),
            'quantidade': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
        }
