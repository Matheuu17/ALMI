from django.urls import path
from . import views

app_name = 'PanelUser'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('contactos/', views.contactos_view, name='contactos'),
    path('contactos/nuevo/', views.form_contactos_view, name='form_contacto'),
    path('actividades/', views.actividades_view, name='actividades'),
    path('actividades/nueva/', views.form_actividades_view, name='form_actividad'),
    path('actividades/completar/<int:actividad_id>/', views.completar_actividad, name='completar_actividad'),
    path('actividades/eliminar/<int:actividad_id>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('actividades/editar/<int:actividad_id>/', views.editar_actividad, name='editar_actividad'),
    path('contactos/editar/<int:contacto_id>/', views.editar_contacto, name='editar_contacto'),
    path('contactos/desactivar/<int:contacto_id>/', views.desactivar_contacto, name='desactivar_contacto'),
]