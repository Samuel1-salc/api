
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserId, Treino, Workout
from .serializer import UserIdSerializer, TreinoSerializer, WorkoutSerializer


#################################################################################################################################################
# Endpoint para listar todos os exercícios (Workout)

class WorkoutListView(generics.ListAPIView):
	queryset = Workout.objects.all()
	serializer_class = WorkoutSerializer


#################################################################################################################################################
# View para listar e criar treinos
class TreinoListCreateView(generics.ListCreateAPIView):
	queryset = Treino.objects.all()
	serializer_class = TreinoSerializer


#################################################################################################################################################
# View melhorada para criar treinos com validação detalhada
class CriarTreinoView(generics.CreateAPIView):
    serializer_class = TreinoSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            
            
            # Validar campos obrigatórios
            required_fields = ['id_treino_criado', 'letra_treino', 'id_exercicio', 'nome_exercicio', 'series', 'repeticoes']
            missing_fields = [field for field in required_fields if field not in data or data[field] == '']
            
            if missing_fields:
                return Response({
                    'error': f'Campos obrigatórios ausentes: {", ".join(missing_fields)}',
                    'missing_fields': missing_fields
                }, status=400)
            
            # Validar se o exercício existe na base de dados
            try:
                exercicio_id = int(data['id_exercicio'])
                workout = Workout.objects.get(id=exercicio_id)
                print(f"Exercício encontrado: {workout.nome_exercicio}")
            except Workout.DoesNotExist:
                return Response({
                    'error': f'Exercício com ID {data["id_exercicio"]} não encontrado na base de dados'
                }, status=400)
            except ValueError:
                return Response({
                    'error': f'ID do exercício deve ser um número válido. Recebido: {data["id_exercicio"]}'
                }, status=400)
            
            # Validar se o usuário existe (se fornecido)
            if 'UserId' in data:
                try:
                    user_id = int(data['UserId'])
                    user = UserId.objects.get(user_numeric_id=user_id)
                    data['UserId'] = user.id  # Usar o ID do banco para o relacionamento
                except UserId.DoesNotExist:
                    return Response({
                        'error': f'Usuário com ID numérico {data["UserId"]} não encontrado'
                    }, status=400)
                except ValueError:
                    return Response({
                        'error': f'ID do usuário deve ser um número válido. Recebido: {data["UserId"]}'
                    }, status=400)
          
            
            # Validar valores numéricos
            try:
                data['series'] = int(data['series'])
                if data['series'] <= 0:
                    return Response({'error': 'Número de séries deve ser maior que zero'}, status=400)
            except ValueError:
                return Response({'error': f'Número de séries deve ser um número válido. Recebido: {data["series"]}'}, status=400)
            
            # Criar o treino usando o serializer
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                treino = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Treino criado com sucesso',
                    'treino_id': treino.id,
                    'data_criacao': treino.data_criacao
                }, status=201)
            else:
                print(f"Erros de validação: {serializer.errors}")
                return Response({
                    'error': 'Dados inválidos',
                    'detalhes': serializer.errors
                }, status=400)
                
        except Exception as e:
            print(f"Erro interno: {str(e)}")
            return Response({
                'error': f'Erro interno do servidor: {str(e)}'
            }, status=500)


#################################################################################################################################################
# View para criar usuários com ID numérico
class CriarUsuarioNumericoView(APIView):
    def post(self, request):
        try:
            user_numeric_id = request.data.get('user_id')
            
            if not user_numeric_id:
                return Response({
                    'error': 'user_id é obrigatório'
                }, status=400)
            
            # Converter para inteiro
            try:
                user_numeric_id = int(user_numeric_id)
            except ValueError:
                return Response({
                    'error': 'user_id deve ser um número válido'
                }, status=400)
            
            # Verificar se já existe
            if UserId.objects.filter(user_numeric_id=user_numeric_id).exists():
                user = UserId.objects.get(user_numeric_id=user_numeric_id)
                return Response({
                    'success': True,
                    'message': 'Usuário já existe',
                    'user_id': user.user_numeric_id,
                    'created': False
                }, status=200)
            
            # Criar novo usuário
            user = UserId.objects.create(user_numeric_id=user_numeric_id)
            return Response({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'user_id': user.user_numeric_id,
                'created': True
            }, status=201)
            
        except Exception as e:
            return Response({
                'error': f'Erro interno: {str(e)}'
            }, status=500)


#################################################################################################################################################
# View para verificar se um ID de usuário já existe
class VerificarUsuarioView(APIView):
    def get(self, request, user_id):
        try:
            # Converter para inteiro
            try:
                user_numeric_id = int(user_id)
            except ValueError:
                return Response({
                    'error': 'user_id deve ser um número válido',
                    'exists': False
                }, status=400)
            
            # Verificar se existe
            if UserId.objects.filter(user_numeric_id=user_numeric_id).exists():
                user = UserId.objects.get(user_numeric_id=user_numeric_id)
                return Response({
                    'exists': True,
                    'user_id': user.user_numeric_id,
                    'message': 'Usuário encontrado'
                }, status=200)
            else:
                return Response({
                    'exists': False,
                    'user_id': user_numeric_id,
                    'message': 'Usuário não encontrado'
                }, status=404)
                
        except Exception as e:
            return Response({
                'error': f'Erro interno: {str(e)}',
                'exists': False
            }, status=500)



#################################################################################################################################################
# View para listar e criar UserId
class UserIdListCreateView(generics.ListCreateAPIView):
	queryset = UserId.objects.all()
	serializer_class = UserIdSerializer


#################################################################################################################################################
class UltimoTreinoUsuarioView(generics.RetrieveAPIView):
    serializer_class = TreinoSerializer
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        return Treino.objects.filter(UserId=user_id).order_by('-data_criacao').first()


#################################################################################################################################################
# View para buscar grupos musculares únicos
class GruposMusculares(APIView):
    def get(self, request):
        grupos = Workout.objects.values_list('grupo_muscular', flat=True).distinct().order_by('grupo_muscular')
        return Response(list(grupos))



#################################################################################################################################################
# View para buscar exercícios por grupo muscular
class WorkoutPorGrupoView(generics.ListAPIView):
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        grupo = self.request.query_params.get('grupo')
        if grupo:
            return Workout.objects.filter(grupo_muscular=grupo)
        return Workout.objects.all()


#################################################################################################################################################
# View para buscar exercícios por grupo muscular (alternativa com parâmetro na URL)
class WorkoutPorGrupoParamView(generics.ListAPIView):
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        grupo = self.kwargs.get('grupo')
        return Workout.objects.filter(grupo_muscular=grupo)



#################################################################################################################################################
# View para listar treinos de um usuário com query parameter
class TreinosPorUsuarioView(generics.ListAPIView):
    serializer_class = TreinoSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Treino.objects.filter(UserId=user_id).order_by('-data_criacao', '-id')
        return Treino.objects.all().order_by('-data_criacao', '-id')



#################################################################################################################################################

# View para buscar o último treino completo de um usuário
class UltimoTreinoCompletoView(APIView):

    def get(self, request, user_id):
        
        try:
            # Tentar encontrar usuário por ID numérico ou ID do banco
            if len(user_id) > 10:  # ID numérico longo
                user = UserId.objects.get(user_numeric_id=int(user_id))
            else:  # ID do banco (pk)
                user = UserId.objects.get(pk=int(user_id))
            
            # Buscar o último treino criado pelo usuário
            ultimo_treino = Treino.objects.filter(UserId=user).order_by('-data_criacao', '-id').first()
            
            if not ultimo_treino:
                return Response({
                    'message': 'Nenhum treino encontrado para este usuário',
                    'treinos': []
                }, status=200)
            
            # Buscar todos os treinos com o mesmo id_treino_criado
            treinos_completos = Treino.objects.filter(
                UserId=user,
                id_treino_criado=ultimo_treino.id_treino_criado
            ).order_by('letra_treino')
            
            # Serializar os treinos
            serializer = TreinoSerializer(treinos_completos, many=True)
            
            # Agrupar por letra_treino
            treinos_agrupados = {}
            for treino in serializer.data:
                letra = treino['letra_treino']
                if letra not in treinos_agrupados:
                    treinos_agrupados[letra] = []
                treinos_agrupados[letra].append(treino)
            
            return Response({
                'id_treino_criado': ultimo_treino.id_treino_criado,
                'data_criacao': ultimo_treino.data_criacao,
                'treinos_por_letra': treinos_agrupados,
                'total_treinos': len(serializer.data)
            })
            
        except UserId.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
#################################################################################################################################################




# View para estatísticas do usuário (com suporte a UUID)
class EstatisticasUsuarioView(APIView):
    def get(self, request, user_id):
        try:
            # Tentar encontrar usuário por ID numérico ou ID do banco
            if len(user_id) > 10:  # ID numérico longo
                user = UserId.objects.get(user_numeric_id=int(user_id))
            else:  # ID do banco (pk)
                user = UserId.objects.get(pk=int(user_id))
            
            # Buscar estatísticas
            total_treinos = Treino.objects.filter(UserId=user).count()
            treinos_agrupados = Treino.objects.filter(UserId=user).values('id_treino_criado').distinct().count()
            ultimo_treino = Treino.objects.filter(UserId=user).order_by('-data_criacao').first()
            
            # Exercícios únicos treinados
            exercicios_unicos = Treino.objects.filter(UserId=user).values('nome_exercicio').distinct().count()
            
            return Response({
                'user_id': user.user_numeric_id,
                'total_exercicios_treino': total_treinos,
                'total_treinos_criados': treinos_agrupados,
                'exercicios_unicos_treinados': exercicios_unicos,
                'ultimo_treino_data': ultimo_treino.data_criacao if ultimo_treino else None,
                'ultimo_treino_letra': ultimo_treino.letra_treino if ultimo_treino else None,
            })
        except UserId.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



#################################################################################################################################################
# View para listar todos os treinos de um usuário específico (por UUID)
class TreinosDoUsuarioView(generics.ListAPIView):
    serializer_class = TreinoSerializer
    
    def get_queryset(self):
        user_identifier = self.kwargs['user_id']
        
        try:
            # Tentar como ID numérico primeiro
            if len(user_identifier) > 10:  # ID numérico longo
                user = UserId.objects.get(user_numeric_id=int(user_identifier))
            else:
                # Fallback para ID do banco (pk)
                user = UserId.objects.get(id=int(user_identifier))
            
            return Treino.objects.filter(UserId=user).order_by('-data_criacao', '-id')
        except (UserId.DoesNotExist, ValueError):
            return Treino.objects.none()  # Retorna queryset vazio se usuário não encontrado