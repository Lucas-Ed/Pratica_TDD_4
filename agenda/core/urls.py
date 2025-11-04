from django.urls import path
from core.views import login, logout, home
from . import views


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    
    path('cadastrar/', views.cadastrar_contato, name='cadastrar_contato'),
    path('listar/', views.listar_contatos, name='listar_contatos'),
    path('editar/<int:id>/', views.editar_contato, name='editar_contato'),
    path('excluir/<int:id>/', views.excluir_contato, name='excluir_contato'),
]