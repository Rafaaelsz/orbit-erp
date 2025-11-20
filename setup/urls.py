from django.contrib import admin
from django.urls import path, include
from estoque import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.dashboard, name='dashboard'),

    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('deletar/<int:id>/', views.deletar_produto, name='deletar_produto'),

    path('movimentar/<int:id>/', views.movimentar_produto,
         name='movimentar_produto'),
    path('historico/<int:id>/', views.historico_produto, name='historico_produto'),
    path('produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
