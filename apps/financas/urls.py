from django.urls import path
from . import views

app_name = 'financas'

urlpatterns =[
    path('nova_categoria', views.nova_categoria, name='nova_categoria'),
    path('lista_categorias', views.lista_categorias, name='lista_categorias'),
    path('editar_categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('apagar_categoria/<int:pk>/', views.apagar_categoria, name='apagar_categoria'),
    path('nova_receita/', views.nova_receita, name='nova_receita'),
    path('lista_receitas/', views.lista_receitas, name='lista_receitas'),
    path('editar_receita/<int:pk>/', views.editar_receita, name='editar_receita'),
    path('apagar_receita/<int:pk>/', views.apagar_receita, name='apagar_receita'),
    path('lista_despesas/', views.lista_despesas, name='lista_despesas'),
    path('nova_despesa/', views.nova_despesa, name='nova_despesa'),
    path('editar_despesa/<int:pk>', views.editar_despesa, name='editar_despesa'),
    path('apagar_despesa/<int:pk>', views.apagar_despesa, name='apagar_despesa'),
    path('', views.principal, name='principal'),
]
