from django.urls import path
from .views import (
    TreinoListCreateView, 
    CriarTreinoView,
    CriarUsuarioNumericoView,
    VerificarUsuarioView,
    WorkoutListView, 
    UserIdListCreateView, 
    UltimoTreinoUsuarioView,
    UltimoTreinoCompletoView,
    GruposMusculares,
    WorkoutPorGrupoView,
    WorkoutPorGrupoParamView,
    TreinosDoUsuarioView,
    TreinosPorUsuarioView,
    EstatisticasUsuarioView
)

urlpatterns = [
	# Endpoints principais de treinos
	path('treinos/', TreinoListCreateView.as_view(), name='treino-list-create'),
	path('treinos/criar/', CriarTreinoView.as_view(), name='criar-treino-melhorado'),  # Nova URL com validação melhorada
	
	# Endpoints de usuários
	path('users/', UserIdListCreateView.as_view(), name='userid-list-create'),
	path('users/criar/', CriarUsuarioNumericoView.as_view(), name='criar-usuario-numerico'),  # Nova URL para usuários numéricos
	path('users/verificar/<str:user_id>/', VerificarUsuarioView.as_view(), name='verificar-usuario'),  # Nova URL para verificar usuário
	path('users/<str:user_id>/ultimo-treino/', UltimoTreinoUsuarioView.as_view(), name='ultimo-treino-usuario'),
	path('users/<str:user_id>/ultimo-treino-completo/', UltimoTreinoCompletoView.as_view(), name='ultimo-treino-completo'),  # Nova URL para treino completo
	path('users/<str:user_id>/treinos/', TreinosDoUsuarioView.as_view(), name='treinos-do-usuario'),
	path('users/<str:user_id>/estatisticas/', EstatisticasUsuarioView.as_view(), name='estatisticas-usuario'),
	
	# Outros endpoints
	path('workouts/', WorkoutListView.as_view(), name='workout-list'),
	
	# Endpoints para otimização
	path('workouts/grupos/', GruposMusculares.as_view(), name='grupos-musculares'),
	path('workouts/por-grupo/', WorkoutPorGrupoView.as_view(), name='workouts-por-grupo-query'),
	path('workouts/grupo/<str:grupo>/', WorkoutPorGrupoParamView.as_view(), name='workouts-por-grupo-param'),
	
	# Endpoints para treinos do usuário (queries)
	path('treinos/por-usuario/', TreinosPorUsuarioView.as_view(), name='treinos-por-usuario-query'),
]
