
from .models import Cliente, Mesa, Reserva  # Importa os modelos Cliente, Mesa e Reserva.
from .forms import ClienteForm, ReservaForm, MesaForm  # Importa os formulários personalizados para Cliente, Reserva e Mesa.
from django.shortcuts import render, redirect, get_object_or_404  # Funções utilitárias para renderizar templates e redirecionar.
from django.contrib.auth.models import User  # Importa o modelo de usuário padrão do Django.
from django.http import HttpResponse  # Para retornar respostas HTTP.
from django.template.loader import render_to_string  # Carrega um template HTML como string.
from weasyprint import HTML  # Para gerar arquivos PDF a partir de HTML.
from .forms import EditUserForm, CustomUserCreationForm  # Importa formulários personalizados para criação e edição de usuários.
from django.contrib.auth.decorators import login_required  # Decorador que restringe acesso a usuários autenticados.
from django.db.models import Value  # Importa a classe Value para usar em anotações.
from django.db.models.functions import Concat  # Importa a função Concat para concatenar strings em queries.
from django.views.generic import ListView  # Importa a classe ListView para criar views baseadas em listas.


# menu

@login_required  # Restringe o acesso à view somente para usuários autenticados.
def menu(request):
    return render(request, 'menu.html')  # Renderiza o template do menu principal.

# cliente

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()  # Busca todos os clientes no banco de dados.
    return render(request, 'core/clientes/lista_clientes.html', {'clientes': clientes})  # Renderiza a lista de clientes.

@login_required
def criar_cliente(request):
    if request.method == 'POST':  # Verifica se o formulário foi enviado (POST).
        form = ClienteForm(request.POST)  # Instancia o formulário com os dados enviados.
        if form.is_valid():  # Verifica se os dados são válidos.
            form.save()  # Salva o cliente no banco de dados.
            return redirect('lista_clientes')  # Redireciona para a lista de clientes.
    else:
        form = ClienteForm()  # Exibe um formulário vazio se for uma requisição GET.
    return render(request, 'core/clientes/criar_cliente.html', {'form': form})  # Renderiza o formulário.

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Obtém o cliente ou retorna erro 404 se não existir.
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)  # Preenche o formulário com os dados existentes do cliente.
        if form.is_valid():
            form.save()  # Salva as alterações.
            return redirect('lista_clientes')  # Redireciona para a lista de clientes.
    else:
        form = ClienteForm(instance=cliente)  # Preenche o formulário com os dados do cliente.
    return render(request, 'core/clientes/editar_cliente.html', {'form': form, 'cliente': cliente})  # Renderiza o formulário para edição.

@login_required
def deletar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Busca o cliente ou retorna erro 404.
    if request.method == 'POST':
        cliente.delete()  # Deleta o cliente do banco de dados.
        return redirect('lista_clientes')  # Redireciona para a lista de clientes.
    return render(request, 'core/clientes/deletar_cliente.html', {'cliente': cliente})  # Renderiza a página de confirmação de deleção.

# reservas
@login_required
def lista_reservas(request):
    reservas = Reserva.objects.all().order_by('data_reserva', 'hora_entrada')  # Busca todas as reservas e ordena por data e hora de entrada.
    query = request.GET.get('q')  # Obtém o termo de busca (se houver).
    if query:
        reservas = Reserva.objects.annotate(  # Adiciona um campo "nome_cliente" à query para pesquisar.
            cliente_nome=Concat('cliente__nome', Value(''))  # Concatena o nome do cliente.
        ).filter(cliente__nome__icontains=query)  # Filtra as reservas que contenham o termo buscado.
    else:
        reservas = Reserva.objects.all()  # Caso não haja busca, retorna todas as reservas.
    return render(request, 'core/reservas/lista_reservas.html', {'reservas': reservas})  # Renderiza a lista de reservas.

@login_required
def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)  # Instancia o formulário com os dados enviados.
        if form.is_valid():
            form.save()  # Salva a nova reserva.
            return redirect('lista_reservas')  # Redireciona para a lista de reservas.
    else:
        form = ReservaForm()  # Exibe o formulário vazio para criação.
    return render(request, 'core/reservas/criar_reserva.html', {'form': form})  # Renderiza o formulário de criação de reserva.

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)  # Obtém a reserva pelo ID ou retorna erro 404.
    mesas = Mesa.objects.all()  # Busca todas as mesas.
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)  # Preenche o formulário com os dados existentes da reserva.
        if form.is_valid():
            form.save()  # Salva as alterações na reserva.
            return redirect('lista_reservas')  # Redireciona para a lista de reservas.
    else:
        form = ReservaForm(instance=reserva)  # Preenche o formulário com os dados da reserva.
    return render(request, 'core/reservas/editar_reserva.html', {'reserva': reserva, 'mesas': mesas})  # Renderiza o formulário de edição.

@login_required
def deletar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)  # Busca a reserva ou retorna erro 404.
    if request.method == 'POST':
        reserva.delete()  # Deleta a reserva.
        return redirect('lista_reservas')  # Redireciona para a lista de reservas.
    return render(request, 'core/reservas/deletar_reserva.html', {'reserva': reserva})  # Renderiza a página de confirmação de deleção.

# Tudo sobre usuário
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()  # Busca todos os usuários.
    return render(request, 'core/usuarios/listar_usuarios.html', {'usuarios': usuarios})  # Renderiza a lista de usuários.


@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Preenche o formulário de criação de usuário.
        if form.is_valid():
            form.save()  # Salva o novo usuário.
            return redirect('listar_usuarios')  # Redireciona para a lista de usuários.
    else:
        form = CustomUserCreationForm()  # Exibe o formulário vazio.
    return render(request, 'core/usuarios/criar_usuario.html', {'form': form})  # Renderiza o formulário de criação de usuário.

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Busca o usuário pelo ID ou retorna erro 404.
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)  # Preenche o formulário de edição do usuário.
        if form.is_valid():
            form.save()  # Salva as alterações no usuário.
            return redirect('perfil_usuario')  # Redireciona para o perfil do usuário.
    else:
        form = EditUserForm(instance=user)  # Preenche o formulário com os dados do usuário.
    return render(request, 'core/usuarios/editar_usuario.html', {'form': form})  # Renderiza o formulário de edição.


@login_required
def deletar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)  # Busca o usuário ou retorna erro 404.
    if request.method == 'POST':
        usuario.delete()  # Deleta o usuário.
        return redirect('listar_usuarios')  # Redireciona para a lista de usuários.
    return render(request, 'core/usuarios/deletar_usuario.html', {'usuario': usuario})  # Renderiza a página de confirmação de deleção.


# View para listar mesas
@login_required
def listar_mesas(request):
    mesas = Mesa.objects.all()  # Busca todas as mesas.
    return render(request, 'core/mesas/listar_mesas.html', {'mesas': mesas})  # Renderiza a lista de mesas.

# View para criar mesa
@login_required
def criar_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)  # Preenche o formulário de criação de mesa.
        if form.is_valid():
            form.save()  # Salva a nova mesa.
            return redirect('listar_mesas')  # Redireciona para a lista de mesas.
    else:
        form = MesaForm()  # Exibe o formulário vazio.
    return

# View para atualizar mesa
@login_required
def atualizar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'core/mesas/criar_mesa.html', {'form': form, 'mesa': mesa})

# View para deletar mesa
@login_required
def deletar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('listar_mesas')
    return render(request, 'core/mesas/deletar_mesa.html', {'mesa': mesa})

import datetime

# Função genérica para gerar PDF
def gerar_pdf(html_string, nome_arquivo):
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={nome_arquivo}.pdf'
    return response

# Gerar PDF de Reservas
@login_required
def gerar_relatorio_reservas(request):
    reservas = Reserva.objects.all()
     # Captura a data atual no formato DD/MM/AAAA
    data_atual = datetime.date.today().strftime('%d/%m/%Y')  # Exemplo: 19/10/2024
    hora_atual = datetime.datetime.now().strftime('%H:%M')   # Exemplo: 14:35
    # Renderiza o HTML incluindo a data atual no contexto
    html_string = render_to_string('core/relatorio_reservas.html', {
        'reservas': reservas,
        'data_atual': data_atual,  # Adiciona a data atual ao contexto
        'hora_atual': hora_atual,   # Adiciona o horário atual ao contexto
    })
    return gerar_pdf(html_string, 'relatorio_reservas')

# Gerar PDF de Clientes
@login_required
def gerar_relatorio_clientes(request):
    clientes = Cliente.objects.all()
     # Captura a data atual no formato DD/MM/AAAA
    data_atual = datetime.date.today().strftime('%d/%m/%Y')  # Exemplo: 19/10/2024
    hora_atual = datetime.datetime.now().strftime('%H:%M')   # Exemplo: 14:35
    # Renderiza o HTML incluindo a data atual no contexto
    html_string = render_to_string('core/relatorio_clientes.html', {
        'clientes': clientes,
        'data_atual': data_atual,  # Adiciona a data atual ao contexto
        'hora_atual': hora_atual,   # Adiciona o horário atual ao contexto
    })
    return gerar_pdf(html_string, 'relatorio_clientes')

# Gerar PDF de Usuários
@login_required
def gerar_relatorio_usuarios(request):
    usuarios = User.objects.all()
     # Captura a data atual no formato DD/MM/AAAA
    data_atual = datetime.date.today().strftime('%d/%m/%Y')  # Exemplo: 19/10/2024
    hora_atual = datetime.datetime.now().strftime('%H:%M')   # Exemplo: 14:35
    # Renderiza o HTML incluindo a data atual no contexto
    html_string = render_to_string('core/relatorio_usuarios.html', {
        'usuarios': usuarios,
        'data_atual': data_atual,  # Adiciona a data atual ao contexto
        'hora_atual': hora_atual,   # Adiciona o horário atual ao contexto
    })
    return gerar_pdf(html_string, 'relatorio_usuarios')

# Gerar PDF de Mesas
@login_required
def gerar_relatorio_mesas(request):
    mesas = Mesa.objects.all()
     # Captura a data atual no formato DD/MM/AAAA
    data_atual = datetime.date.today().strftime('%d/%m/%Y')  # Exemplo: 19/10/2024
    hora_atual = datetime.datetime.now().strftime('%H:%M')   # Exemplo: 14:35
    # Renderiza o HTML incluindo a data atual no contexto
    html_string = render_to_string('core/relatorio_mesas.html', {
        'mesas': mesas,
        'data_atual': data_atual,  # Adiciona a data atual ao contexto
        'hora_atual': hora_atual,   # Adiciona o horário atual ao contexto
    })
    return gerar_pdf(html_string, 'relatorio_mesas')


class ReservaListView(ListView):  # Define uma nova view chamada ReservaListView que herda de ListView.
    model = Reserva  # Especifica que esta view deve trabalhar com o modelo Reserva.
    template_name = 'core/reservas/lista_reservas.html'  # Define o template a ser usado para renderizar a lista de reservas.
    context_object_name = 'reservas'  # Define o nome do objeto no contexto que será acessado no template.

    def get_queryset(self):  # Método que retorna o conjunto de dados a ser exibido.
        query = self.request.GET.get('q')  # Obtém o parâmetro de busca 'q' da URL (se houver).
        if query:  # Se houver um termo de busca.
            return Reserva.objects.annotate(  # Realiza uma consulta no modelo Reserva e adiciona anotações.
                nome_cliente=Concat('cliente__nome_completo', Value(''))  # Concatena o nome completo do cliente à consulta.
            ).filter(cliente__nome__icontains=query)  # Filtra as reservas onde o nome do cliente contém o termo de busca.
        return Reserva.objects.all()  # Se não houver busca, retorna todas as reservas disponíveis.

