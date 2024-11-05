from django.urls import path, include
from rest_framework.routers import DefaultRouter
from receitas import views

router = DefaultRouter()

router.register(r'receitas', views.ReceitaViewSet, basename='api-receitas')

urlpatterns = [
    path('', include(router.urls)),
]