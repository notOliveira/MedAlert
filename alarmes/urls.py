from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alarmes import views


router = DefaultRouter()

router.register(r'alarmes', views.AlarmeViewSet, basename='api-alarmes')

urlpatterns = [
    path('', include(router.urls)),
]