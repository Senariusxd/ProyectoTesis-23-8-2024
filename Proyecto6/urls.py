from django.contrib import admin
from django.urls import path, include
from Historia import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about_view, name='about'),
    
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/modificar/<str:pk>/', views.modificar_paciente, name='modificar_paciente'),
    path('pacientes/eliminar/<str:pk>/', views.eliminar_paciente, name='eliminar_paciente'),
    
    path('pacientes/<str:pk>/fechas/', views.ver_fechas_paciente, name='ver_fechas_paciente'),
    path('pacientes/<str:pk>/crear-fecha/', views.crear_fecha_paciente, name='crear_fecha_paciente'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/editar/', views.editar_fecha_paciente, name='editar_fecha_paciente'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/eliminar/', views.eliminar_fecha_paciente, name='eliminar_fecha_paciente'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/crear/', views.crear_egeneral, name='crear_egeneral'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/', views.ver_egeneral, name='ver_egeneral'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/modificar/', views.modificar_egeneral, name='modificar_egeneral'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/', views.ver_interrogatorio, name='ver_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/crear/', views.crear_interrogatorio, name='crear_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/<int:pk_interrogatorio>/modificar/', views.modificar_interrogatorio, name='modificar_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/<int:pk_interrogatorio>/eliminar/', views.eliminar_interrogatorio, name='eliminar_interrogatorio'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/', views.ver_efaparato, name='ver_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/crear/', views.crear_efaparato, name='crear_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/<int:pk_efaparato>/modificar/', views.modificar_efaparato, name='modificar_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/<int:pk_efaparato>/eliminar/', views.eliminar_efaparato, name='eliminar_efaparato'),
    
    path('grupos-pacientes/', views.grupos_pacientes, name='grupos_pacientes'),
    path('porcentaje-pacientes-por-grupo/', views.porcentaje_pacientes_por_grupo, name='porcentaje_pacientes_por_grupo'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/generar-pdf/', views.render_pdf_view, name='generar_pdf'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/generar-pdf/', views.render_pdf_efaparato, name='generar_pdf_efaparato'),

    path('pacientes/con_proxima_cita/', views.pacientes_con_proxima_cita, name='pacientes_con_proxima_cita'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)