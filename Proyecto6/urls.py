from django.contrib import admin
from django.urls import path, include
from Historia.views import views
from Historia.views import pacientes
from Historia.views import fechas
from Historia.views import egeneral
from Historia.views import interrogatorio
from Historia.views import efaparato
from Historia.views import grupos
from Historia.views import pdf
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about_view, name='about'),
    
    path('pacientes/', pacientes.lista_pacientes, name='lista_pacientes'),
    path('pacientes/crear/', pacientes.crear_paciente, name='crear_paciente'),
    path('pacientes/modificar/<str:pk>/', pacientes.modificar_paciente, name='modificar_paciente'),
    path('pacientes/eliminar/<str:pk>/', pacientes.eliminar_paciente, name='eliminar_paciente'),
    
    path('pacientes/<str:pk>/fechas/', fechas.ver_fechas_paciente, name='ver_fechas_paciente'),
    path('pacientes/<str:pk>/crear-fecha/', fechas.crear_fecha_paciente, name='crear_fecha_paciente'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/editar/', fechas.editar_fecha_paciente, name='editar_fecha_paciente'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/eliminar/', fechas.eliminar_fecha_paciente, name='eliminar_fecha_paciente'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/crear/', egeneral.crear_egeneral, name='crear_egeneral'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/', egeneral.ver_egeneral, name='ver_egeneral'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/modificar/', egeneral.modificar_egeneral, name='modificar_egeneral'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/', interrogatorio.ver_interrogatorio, name='ver_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/crear/', interrogatorio.crear_interrogatorio, name='crear_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/<int:pk_interrogatorio>/modificar/', interrogatorio.modificar_interrogatorio, name='modificar_interrogatorio'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/<int:pk_interrogatorio>/eliminar/', interrogatorio.eliminar_interrogatorio, name='eliminar_interrogatorio'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/', efaparato.ver_efaparato, name='ver_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/crear/', efaparato.crear_efaparato, name='crear_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/<int:pk_efaparato>/modificar/', efaparato.modificar_efaparato, name='modificar_efaparato'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/<int:pk_efaparato>/eliminar/', efaparato.eliminar_efaparato, name='eliminar_efaparato'),
    
    path('grupos-pacientes/', grupos.grupos_pacientes, name='grupos_pacientes'),
    path('estadisticas_generales/', grupos.estadisticas_generales_view, name='estadisticas_generales'),
    
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/interrogatorio/generar-pdf/', pdf.render_pdf_view, name='generar_pdf'),
    path('pacientes/<str:pk_paciente>/fechas/<int:pk_fecha>/egeneral/<int:pk_egeneral>/efaparato/generar-pdf/', pdf.render_pdf_efaparato, name='generar_pdf_efaparato'),

    path('pacientes/con_proxima_cita/', pacientes.pacientes_con_proxima_cita, name='pacientes_con_proxima_cita'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)