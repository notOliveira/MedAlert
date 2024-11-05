from django.urls import path, include
from rest_framework.routers import DefaultRouter
from medicamentos import views

router = DefaultRouter()

router.register(r'medicamentos', views.MedicamentosViewSet, basename='api-medicamentos')

urlpatterns = [
    path('', include(router.urls)),
]