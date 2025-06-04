from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),  # Ruta principal al dashboard
    path('abonar/', views.abonar, name='abonar'),
    path('editar_local/', views.editar_local, name='editar_local'),
    path('crear_local/', views.crear_local, name='crear_local'),  # <--- ESTA LÍNEA ES CLAVE
    path('actualizar_rentado/', views.actualizar_rentado, name='actualizar_rentado'),
]