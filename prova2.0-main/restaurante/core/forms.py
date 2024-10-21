from django import forms  # Importa o módulo de formulários do Django.
from .models import Cliente, Reserva  # Importa os modelos Cliente e Reserva do módulo atual.
from django.contrib.auth.forms import UserCreationForm  # Importa o formulário de criação de usuários do Django.
from django.contrib.auth.models import User  # Importa o modelo de usuário do Django.
from .models import Mesa  # Importa o modelo Mesa do módulo atual.

# Formulário para o modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente  # Define o modelo associado ao formulário como Cliente.
        fields = ['nome', 'email', 'telefone']  # Especifica os campos a serem incluídos no formulário.

from django.utils import timezone  # Importa o módulo timezone para trabalhar com horários

# Formulário para o modelo Reserva
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva  # Define o modelo associado ao formulário como Reserva.
        fields = ['cliente', 'mesa', 'data_reserva', 'hora_entrada', 'hora_saida', 'num_pessoas']  # Campos a serem incluídos no formulário.

    # Define o campo data_reserva como um seletor de data
    data_reserva = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Usar um seletor de data HTML5.
    )
    # Define o campo hora_entrada como um seletor de hora
    hora_entrada = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})  # Usar um seletor de hora HTML5.
    )
    # Define o campo hora_saida como um seletor de hora
    hora_saida = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})  # Usar um seletor de hora HTML5.
    )

    def clean(self):  # Método de limpeza do formulário, que valida os dados.
        cleaned_data = super().clean()  # Chama a implementação da superclasse para obter os dados limpos.
        mesa = cleaned_data.get('mesa')  # Obtém o valor do campo mesa.
        data_reserva = cleaned_data.get('data_reserva')  # Obtém o valor do campo data_reserva.
        hora_entrada = cleaned_data.get('hora_entrada')  # Obtém o valor do campo hora_entrada.
        hora_saida = cleaned_data.get('hora_saida')  # Obtém o valor do campo hora_saida.

        # Verifica se todos os campos necessários estão preenchidos
        if not mesa or not data_reserva or not hora_entrada or not hora_saida:
            return cleaned_data  # Se algum campo não estiver preenchido, retorna os dados limpos.

         # Cria um objeto datetime para a data e hora de entrada
        data_hora_entrada = timezone.datetime.combine(data_reserva, hora_entrada)
        data_hora_saida = timezone.datetime.combine(data_reserva, hora_saida)

        # Torna data_hora_entrada e data_hora_saida cientes do fuso horário
        data_hora_entrada = timezone.make_aware(data_hora_entrada)
        data_hora_saida = timezone.make_aware(data_hora_saida)
        # Verifica se a data e hora da reserva são anteriores ao horário atual
        if data_hora_entrada < timezone.now():
            raise forms.ValidationError("A data e hora de entrada não podem ser no passado.")

        # Verifica se a data e hora da saída são anteriores ao horário atual
        if data_hora_saida < timezone.now():
            raise forms.ValidationError("A data e hora de saída não podem ser no passado.")


        # Verifica se já existe uma reserva para a mesma mesa, data e horário
        reservas_existentes = Reserva.objects.filter(
            mesa=mesa,
            data_reserva=data_reserva,
            hora_entrada__lt=hora_saida,  # Verifica se a hora de entrada da nova reserva é antes da hora de saída da reserva existente.
            hora_saida__gt=hora_entrada  # Verifica se a hora de saída da nova reserva é depois da hora de entrada da reserva existente.
        )

        if reservas_existentes.exists():  # Se já existir uma reserva que conflita.
            raise forms.ValidationError(f"A mesa {mesa} já está reservada para {data_reserva} entre {hora_entrada} e {hora_saida}.")  # Levanta um erro de validação.

        return cleaned_data  # Retorna os dados limpos.
    

# Formulário para o modelo Mesa
class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa  # Define o modelo associado ao formulário como Mesa.
        fields = ['numero', 'capacidade']  # Campos da tabela Mesa a serem incluídos no formulário.


# Formulário para criar novos usuários
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Campo de email, obrigatório.
    is_staff = forms.BooleanField(required=False, label='Membro da Equipe')  # Campo para indicar se o usuário é membro da equipe.
    is_superuser = forms.BooleanField(required=False, label='Superusuário')  # Campo para indicar se o usuário é um superusuário.
    is_active = forms.BooleanField(required=True, label='Ativo')  # Campo para indicar se o usuário está ativo.

    class Meta:
        model = User  # Define o modelo associado ao formulário como User.
        fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active']  # Campos a serem incluídos no formulário.

# Formulário para editar usuários
class EditUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Nova Senha', widget=forms.PasswordInput, required=False)  # Campo para nova senha, opcional.
    password2 = forms.CharField(label='Confirme a Nova Senha', widget=forms.PasswordInput, required=False)  # Campo para confirmação da nova senha, opcional.

    class Meta:
        model = User  # Define o modelo associado ao formulário como User.
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']  # Campos a serem incluídos no formulário.

    def clean(self):  # Método de limpeza do formulário.
        cleaned_data = super().clean()  # Chama a implementação da superclasse para obter os dados limpos.
        password1 = cleaned_data.get('password1')  # Obtém o valor do campo password1.
        password2 = cleaned_data.get('password2')  # Obtém o valor do campo password2.

        if password1 and password1 != password2:  # Se a nova senha for preenchida e não coincidir com a confirmação.
            self.add_error('password2', "As senhas não coincidem.")  # Adiciona um erro ao campo password2.

        return cleaned_data  # Retorna os dados limpos.

    def save(self, commit=True):  # Método para salvar o usuário.
        user = super().save(commit=False)  # Cria o objeto User, mas não salva ainda.
        password1 = self.cleaned_data.get('password1')  # Obtém a nova senha.

        if password1:  # Se uma nova senha foi fornecida.
            user.set_password(password1)  # Define a nova senha.

        if commit:  # Se o commit estiver ativado.
            user.save()  # Salva o objeto User no banco de dados.

        return user  # Retorna o usuário salvo.
    


