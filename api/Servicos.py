from .models import aluno
from .models import Treino

def cadastrar_aluno(dados_aluno):
    aluno_novo = aluno(**dados_aluno)
    aluno_novo.save()
    return aluno_novo

def cadastrar_treino(dados_treino):
    treino_novo = Treino(**dados_treino)
    treino_novo.save()
    return treino_novo

