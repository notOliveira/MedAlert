from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

v1 = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{v1}/', include('alarmes.urls')),
    path(f'{v1}/', include('usuarios.urls')),
    path(f'{v1}/', include('receitas.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    # path(f'{v1}/', include('medicamentos.urls')),
    # re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]
