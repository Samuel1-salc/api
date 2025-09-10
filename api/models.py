
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class UserId(models.Model):
    user_numeric_id = models.BigIntegerField(unique=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.id_user:
            return f"UserId {self.id_user.username} - {self.user_numeric_id}"
        return f"UserId {self.user_numeric_id}"



class Treino(models.Model):
    id_treino_criado = models.BigIntegerField(null=True, blank=True)
    letra_treino    = models.CharField(max_length=5)
    id_exercicio   = models.IntegerField()
    nome_exercicio  = models.CharField(max_length=100)
    series          = models.IntegerField()
    repeticoes      = models.CharField(max_length=20)
    observacao      = models.TextField(blank=True, null=True)
    data_criacao    = models.DateField(auto_now_add=True)
    UserId          = models.ForeignKey(UserId, on_delete=models.CASCADE, related_name='treinos')

    def __str__(self):
        return f"Treino {self.letra_treino} - {self.UserId} - Exercicio {self.id_exercicio}: {self.nome_exercicio}"


class Workout(models.Model):
    nome_exercicio = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=100)
    descricao      = models.TextField(blank=True, null=True)
    imagem = models.URLField(blank=True, null=True)


    def __str__(self):
        return f"{self.nome_exercicio} - {self.grupo_muscular}"



        
