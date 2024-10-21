
# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=255)  # Campo para o nome do cliente
    email = models.EmailField(unique=True)             # Campo para o e-mail do cliente
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)  # Número da mesa
    capacidade = models.IntegerField()  # Capacidade da mesa

    def __str__(self):
        return f'Mesa {self.numero} (Capacidade: {self.capacidade})'


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relaciona a reserva com o cliente
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # Relaciona a reserva com a mesa
    data_reserva = models.DateField()
    hora_entrada = models.TimeField()  # Horário de entrada
    hora_saida = models.TimeField()     # Horário de saída
    num_pessoas = models.IntegerField()

    def __str__(self):
        return f'Reserva de {self.cliente.nome} na {self.mesa} para {self.num_pessoas} pessoas'

    
