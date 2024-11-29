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
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('callback/', views.google_login_callback, name='callback'),
    path('google/validade_token/', views.validate_google_token, name='validate-token'),
    path('password-reset-request/', views.RequestPasswordResetEmail.as_view(), name='password-reset-request'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    # path('users/<int:id>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),
]
