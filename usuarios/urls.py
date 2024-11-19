from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from usuarios import views

router = DefaultRouter()

# Ajustes nos basenames para manter os nomes nos testes
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-atualizar'),
    path('registro/', views.RegistroUsuario.as_view(), name='registro'),
    # path('users/<int:id>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),
]
