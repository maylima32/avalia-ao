# core/urls.py
from django.urls import path
from . import views
from .views import listar_mesas, criar_mesa, atualizar_mesa, deletar_mesa
from django.urls import path
from .views import editar_usuario
from django.contrib.auth import views as auth_views
from .views import (
    gerar_relatorio_reservas,
    gerar_relatorio_clientes,
    gerar_relatorio_usuarios,
    gerar_relatorio_mesas,)


urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/deletar/<int:cliente_id>/', views.deletar_cliente, name='deletar_cliente'),

    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/criar/', views.criar_reserva, name='criar_reserva'),
    path('reservas/editar/<int:reserva_id>/ ', views.editar_reserva, name='editar_reserva'),
    path('reservas/deletar/<int:pk>/', views.deletar_reserva, name='deletar_reserva'),

    path('menu/', views.menu, name='menu'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),
    
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
     path('usuarios/<int:user_id>/editar/', editar_usuario, name='editar_usuario'), 
    path('usuarios/<int:user_id>/deletar/', views.deletar_usuario, name='deletar_usuario'),

    path('mesas/', listar_mesas, name='listar_mesas'),
    path('mesas/criar/', criar_mesa, name='criar_mesa'),
    path('mesas/atualizar/<int:pk>/', atualizar_mesa, name='atualizar_mesa'),
    path('mesas/deletar/<int:pk>/', deletar_mesa, name='deletar_mesa'),

    path('relatorio/reservas/', gerar_relatorio_reservas, name='gerar_relatorio_reservas'),
    path('relatorio/clientes/', gerar_relatorio_clientes, name='gerar_relatorio_clientes'),
    path('relatorio/usuarios/', gerar_relatorio_usuarios, name='gerar_relatorio_usuarios'),
    path('relatorio/mesas/', gerar_relatorio_mesas, name='gerar_relatorio_mesas'),

]
