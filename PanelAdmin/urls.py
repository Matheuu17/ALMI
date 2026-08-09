from django.urls import path
from . import views

app_name = 'PanelAdmin'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('usuarios/<int:user_id>/toggle-estado/', views.toggle_estado_usuario_view, name='toggle_estado'),
    path('usuarios/<int:user_id>/reset-password/', views.reset_password_usuario_view, name='reset_password'),
]