from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
from django.db import IntegrityError
from .models import Paciente, Fecha, Grupos, EGeneral, Interrogatorio, EFaparato 
from .formsP import EGeneralForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al usuario a la página de inicio (home)
        else:
            # Maneja el error de inicio de sesión
            context = {'error': 'Nombre de usuario o contraseña incorrectos.'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('login')  # Redirigir al usuario a la página de inicio de sesión
    else:
        return redirect('login') 

def home(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def lista_pacientes(request):
    # Obtener el término de búsqueda (si existe)
    search_query = request.GET.get('search', '')

    # Filtrar los pacientes por el término de búsqueda
    pacientes = Paciente.objects.filter(
        Q(ci__icontains=search_query) |
        Q(nombre__icontains=search_query) |
        Q(apellidos__icontains=search_query)
    )

    # Configurar la paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(pacientes, 15)  # Mostrar 15 pacientes por página
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'pacientes': page_obj,
        'search_query': search_query  # Guardar el término de búsqueda en el contexto
    }
    return render(request, 'pacientes/lista_pacientes.html', context)

def crear_paciente(request):
    if request.method == 'POST':
        ci = request.POST.get('ci')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        sexo = request.POST.get('sexo')
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')

        try:
            paciente = Paciente.objects.create(
                ci=ci,
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                direccion=direccion,
                sexo=sexo,
                raza=raza,
                edad=edad
            )
            return redirect('lista_pacientes')
        except IntegrityError:
            # La cédula de identidad ya existe en la base de datos
            error_message = 'La cédula de identidad ya existe. Por favor, ingrese una cédula de identidad única.'
            return render(request, 'crear_paciente.html', {'error_message': error_message})
    else:
        return render(request, 'pacientes/crear_paciente.html', {})

def modificar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        sexo = request.POST.get('sexo')
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')
        
        # Validar los datos, excepto la cédula de identidad
        if nombre and apellidos and telefono and edad:
            paciente.nombre = nombre
            paciente.apellidos = apellidos
            paciente.telefono = telefono
            paciente.direccion = direccion
            paciente.sexo = sexo
            paciente.raza = raza
            paciente.edad = edad
            paciente.save()
            return redirect('lista_pacientes')
    
    return render(request, 'pacientes/modificar_paciente.html', {'paciente': paciente})

def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')
    
    context = {
        'paciente': paciente
    }
    return render(request, 'pacientes/eliminar_paciente.html', context)

from datetime import datetime

def ver_fechas_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    search_query = request.GET.get('search', '')
    
    if search_query:
        try:
            search_date = datetime.strptime(search_query, '%d/%m/%Y')
            fechas = Fecha.objects.filter(paciente=paciente, fecha_inicial__date=search_date.date(), fecha_inicial__time=search_date.time())
        except ValueError:
            fechas = Fecha.objects.filter(paciente=paciente, fecha_inicial__icontains=search_query)
    else:
        fechas = Fecha.objects.filter(paciente=paciente)
    
    context = {
        'paciente': paciente,
        'fechas': fechas,
        'search_query': search_query
    }
    
    return render(request, 'fechas/fechas_paciente.html', context)

def crear_fecha_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        fecha_inicial = request.POST.get('fecha_inicial')
        new_fecha = Fecha.objects.create(paciente=paciente, fecha_inicial=fecha_inicial)
        return redirect('ver_fechas_paciente', pk=paciente.pk)

    return render(request, 'fechas/crear_fecha_paciente.html', {'paciente': paciente})

def editar_fecha_paciente(request, pk_paciente, pk_fecha):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
    fecha = get_object_or_404(Fecha, pk=pk_fecha, paciente=paciente)

    if request.method == 'POST':
        fecha_inicial = request.POST.get('fecha_inicial')
        fecha.fecha_inicial = fecha_inicial
        fecha.save()
        return redirect('ver_fechas_paciente', pk=paciente.pk)

    return render(request, 'fechas/editar_fecha_paciente.html', {'paciente': paciente, 'fecha': fecha})

def eliminar_fecha_paciente(request, pk_paciente, pk_fecha):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
    fecha = get_object_or_404(Fecha, pk=pk_fecha, paciente=paciente)

    if request.method == 'POST':
        fecha.delete()
        return redirect('ver_fechas_paciente', pk=paciente.pk)

    return render(request, 'fechas/eliminar_fecha_paciente.html', {'paciente': paciente, 'fecha': fecha})

def ver_egeneral(request, pk_paciente, pk_fecha):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
    fecha = get_object_or_404(Fecha, pk=pk_fecha, paciente=paciente)
    try:
        egeneral = EGeneral.objects.get(fecha=fecha)
    except EGeneral.DoesNotExist:
        # Si no se encuentra el EGeneral, puedes redirigir a una página de error o crear uno nuevo
        return redirect('crear_egeneral', paciente.pk, fecha.pk)
    return render(request, 'egeneral/ver_egeneral.html', {'paciente': paciente, 'fecha': fecha, 'egeneral': egeneral})

def crear_egeneral(request, pk_paciente, pk_fecha):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
    fecha = get_object_or_404(Fecha, pk=pk_fecha, paciente=paciente)

    if request.method == 'POST':
        form = EGeneralForm(request.POST)
        if form.is_valid():
            egeneral = form.save(commit=False)
            egeneral.fecha = fecha
            egeneral.save()
            return redirect('ver_egeneral', paciente.pk, fecha.pk)
    else:
        form = EGeneralForm()

    return render(request, 'egeneral/crear_egeneral.html', {'form': form, 'paciente': paciente, 'fecha': fecha})

def modificar_egeneral(request, pk_paciente, pk_fecha, pk_egeneral):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
    fecha = get_object_or_404(Fecha, pk=pk_fecha, paciente=paciente)
    egeneral = get_object_or_404(EGeneral, pk=pk_egeneral, fecha=fecha)

    if request.method == 'POST':
        form = EGeneralForm(request.POST, instance=egeneral)
        if form.is_valid():
            form.save()
            return redirect('ver_egeneral', paciente.pk, fecha.pk)
    else:
        form = EGeneralForm(instance=egeneral)

    return render(request, 'egeneral/modificar_egeneral.html', {'form': form, 'paciente': paciente, 'fecha': fecha, 'egeneral': egeneral})

def ver_interrogatorio(request, pk_paciente, pk_fecha, pk_egeneral):
    
    try:
        paciente = get_object_or_404(Paciente, pk=pk_paciente)
        egeneral = get_object_or_404(EGeneral, pk=pk_egeneral)
        interrogatorio = egeneral.interrogatorio
    except Interrogatorio.DoesNotExist:
        # Si no existe el interrogatorio, redirigir al usuario a la vista de creación
        return redirect('crear_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)

    context = {
        'paciente': paciente,
        'interrogatorio': interrogatorio
    }
    return render(request, 'interrogatorio/interrogatorio.html', context)

def crear_interrogatorio(request, pk_paciente, pk_fecha, pk_egeneral):
    if request.method == 'POST':
        antecedentes_personales = request.POST.get('antecedentes_personales')
        ap_personal_descripcion = request.POST.get('ap_personal_descripcion')
        antecedentes_familiares = request.POST.get('antecedentes_familiares')
        ap_familiar_descripcion = request.POST.get('ap_familiar_descripcion')
        h_toxicos = request.POST.get('h_toxicos')
        h_toxicos_descripcion = request.POST.get('h_toxicos_descripcion')
        alergias = request.POST.get('alergias')
        alergias_descripcion = request.POST.get('alergias_descripcion')
        operaciones = request.POST.get('operaciones')
        operaciones_descripcion = request.POST.get('operaciones_descripcion')
        transfuciones = request.POST.get('transfuciones')
        transfuciones_descripcion = request.POST.get('transfuciones_descripcion')
        carnet_salud = request.POST.get('carnet_salud')
        carnet_salud_descripcion = request.POST.get('carnet_salud_descripcion')
        p_enfermedad = request.POST.get('p_enfermedad')
        p_enfermedad_descripcion = request.POST.get('p_enfermedad_descripcion')
        ocupacion = request.POST.get('ocupacion')
        ocupacion_descripcion = request.POST.get('ocupacion_descripcion')
        egeneral = EGeneral.objects.get(pk=pk_egeneral)
        
        # Validar que los campos descripcion esten llenos cuando sea 'Si'
        if antecedentes_personales == 'S' and not ap_personal_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})

        if antecedentes_familiares == 'S' and not ap_familiar_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})
        
        if h_toxicos == 'S' and not h_toxicos_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})
        
        if alergias == 'S' and not alergias_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})
        
        if operaciones == 'S' and not operaciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})
        
        if transfuciones == 'S' and not transfuciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})
        
        if p_enfermedad == 'S' and not p_enfermedad_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})

        # Verificar si los campos de descripción están vacíos y asignar una cadena vacía
        if antecedentes_personales == 'N':
            ap_personal_descripcion = ''
        if antecedentes_familiares == 'N':
            ap_familiar_descripcion = ''
        if h_toxicos == 'N':
            h_toxicos_descripcion = ''
        if alergias == 'N':
            alergias_descripcion = ''
        if operaciones == 'N':
            operaciones_descripcion = ''
        if transfuciones == 'N':
            transfuciones_descripcion = ''
        if carnet_salud == 'N':
            carnet_salud_descripcion = None
        if p_enfermedad == 'N':
            p_enfermedad_descripcion = ''
        if ocupacion == 'T':
            ocupacion_descripcion = ''

        interrogatorio = Interrogatorio(
            antecedentes_personales=antecedentes_personales,
            ap_personal_descripcion=ap_personal_descripcion,
            antecedentes_familiares=antecedentes_familiares,
            ap_familiar_descripcion=ap_familiar_descripcion,
            h_toxicos=h_toxicos,
            h_toxicos_descripcion=h_toxicos_descripcion,
            alergias=alergias,
            alergias_descripcion=alergias_descripcion,
            operaciones=operaciones,
            operaciones_descripcion=operaciones_descripcion,
            transfuciones=transfuciones,
            transfuciones_descripcion=transfuciones_descripcion,
            carnet_salud=carnet_salud,
            carnet_salud_descripcion=carnet_salud_descripcion,
            p_enfermedad=p_enfermedad,
            p_enfermedad_descripcion=p_enfermedad_descripcion,
            ocupacion=ocupacion,
            ocupacion_descripcion=ocupacion_descripcion,
            egeneral=egeneral
            )
        interrogatorio.save()
        return redirect('ver_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
    else:
        egeneral = EGeneral.objects.get(pk=pk_egeneral)
        return render(request, 'interrogatorio/crear_interrogatorio.html', {'egeneral': egeneral})

def modificar_interrogatorio(request, pk_paciente, pk_fecha, pk_egeneral, pk_interrogatorio):
    if request.method == 'POST':
        # Obtener el objeto Interrogatorio a modificar
        interrogatorio = Interrogatorio.objects.get(pk=pk_interrogatorio)

        # Actualizar los campos del Interrogatorio con los valores recibidos del formulario
        interrogatorio.antecedentes_personales = request.POST.get('antecedentes_personales')
        interrogatorio.ap_personal_descripcion = request.POST.get('ap_personal_descripcion')
        interrogatorio.antecedentes_familiares = request.POST.get('antecedentes_familiares')
        interrogatorio.ap_familiar_descripcion = request.POST.get('ap_familiar_descripcion')
        interrogatorio.h_toxicos = request.POST.get('h_toxicos')
        interrogatorio.h_toxicos_descripcion = request.POST.get('h_toxicos_descripcion')
        interrogatorio.alergias = request.POST.get('alergias')
        interrogatorio.alergias_descripcion = request.POST.get('alergias_descripcion')
        interrogatorio.operaciones = request.POST.get('operaciones')
        interrogatorio.operaciones_descripcion = request.POST.get('operaciones_descripcion')
        interrogatorio.transfuciones = request.POST.get('transfuciones')
        interrogatorio.transfuciones_descripcion = request.POST.get('transfuciones_descripcion')
        interrogatorio.carnet_salud = request.POST.get('carnet_salud')
        interrogatorio.carnet_salud_descripcion = request.POST.get('carnet_salud_descripcion')
        interrogatorio.p_enfermedad = request.POST.get('p_enfermedad')
        interrogatorio.p_enfermedad_descripcion = request.POST.get('p_enfermedad_descripcion')
        interrogatorio.ocupacion = request.POST.get('ocupacion')
        interrogatorio.ocupacion_descripcion = request.POST.get('ocupacion_descripcion')

        # Validar que los campos descripcion esten llenos cuando sea 'Si'
        if interrogatorio.antecedentes_personales == 'S' and not interrogatorio.ap_personal_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.antecedentes_familiares == 'S' and not interrogatorio.ap_familiar_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        if interrogatorio.h_toxicos == 'S' and not interrogatorio.h_toxicos_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        if interrogatorio.alergias == 'S' and not interrogatorio.alergias_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        if interrogatorio.operaciones == 'S' and not interrogatorio.operaciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        if interrogatorio.transfuciones == 'S' and not interrogatorio.transfuciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        if interrogatorio.p_enfermedad == 'S' and not interrogatorio.p_enfermedad_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})
        
        # Verificar si los campos de descripción están vacíos y asignar una cadena vacía
        if interrogatorio.antecedentes_personales == 'N':
            interrogatorio.ap_personal_descripcion = ''
        if interrogatorio.antecedentes_familiares == 'N':
            interrogatorio.ap_familiar_descripcion = ''
        if interrogatorio.h_toxicos == 'N':
            interrogatorio.h_toxicos_descripcion = ''
        if interrogatorio.alergias == 'N':
            interrogatorio.alergias_descripcion = ''
        if interrogatorio.operaciones == 'N':
            interrogatorio.operaciones_descripcion = ''
        if interrogatorio.transfuciones == 'N':
            interrogatorio.transfuciones_descripcion = ''
        if interrogatorio.carnet_salud == 'N':
            interrogatorio.carnet_salud_descripcion = None
        if interrogatorio.p_enfermedad == 'N':
            interrogatorio.p_enfermedad_descripcion = ''
        if interrogatorio.ocupacion == 'T':
            interrogatorio.ocupacion_descripcion = ''

        interrogatorio.save()
        return redirect('ver_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
    else:
        interrogatorio = Interrogatorio.objects.get(pk=pk_interrogatorio)
        egeneral = EGeneral.objects.get(pk=pk_egeneral)
        return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

def eliminar_interrogatorio(request, pk_paciente, pk_fecha, pk_egeneral, pk_interrogatorio):
    interrogatorio = get_object_or_404(Interrogatorio, pk=pk_interrogatorio)
    egeneral = get_object_or_404(EGeneral, pk=pk_egeneral)

    if request.method == 'POST':
        interrogatorio.delete()
        return redirect('ver_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)

    context = {
        'interrogatorio': interrogatorio,
        'egeneral': egeneral,
        'pk_paciente': pk_paciente,
        'pk_fecha': pk_fecha,
        'pk_egeneral': pk_egeneral
    }
    return render(request, 'interrogatorio/eliminar_interrogatorio.html', context)


def ver_efaparato(request, pk_paciente, pk_fecha, pk_egeneral):
    
    try:
        egeneral = get_object_or_404(EGeneral, pk=pk_egeneral)
        efaparato = egeneral.efaparato
    except:
        return redirect('crear_efaparato', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
    
    context = {
        'efaparato': efaparato
    }
    return render(request, 'efaparato/efaparato.html', context)
    
    
def crear_efaparato(request, pk_paciente, pk_fecha, pk_egeneral):
    grupos = Grupos.objects.all()
    
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        grupo = get_object_or_404(Grupos, id=grupo_id)
        pym_humedo = request.POST.get('pym_humedo')
        pym_coloreado = request.POST.get('pym_coloreado')
        descripcion_pym = request.POST.get('descripcion_pym')
        tvs = request.POST.get('tvs')
        descripcion_tvs = request.POST.get('descripcion_tvs')
        inspeccion_respiratoria = request.POST.get('inspeccion_respiratoria')
        palpacion_respiratoria = request.POST.get('palpacion_respiratoria')
        percusion_respiratoria = request.POST.get('percusion_respiratoria')
        auscultacion_respiratoria = request.POST.get('auscultacion_respiratoria')
        descripcion_respiratoria = request.POST.get('descripcion_respiratoria')
        frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
        descripcion_frecuencia_respiratoria = request.POST.get('descripcion_frecuencia_respiratoria')
        inspeccion_cardiovascular = request.POST.get('inspeccion_cardiovascular')
        palpacion_cardiovascular = request.POST.get('palpacion_cardiovascular')
        percusion_cardiovascular = request.POST.get('percusion_cardiovascular')
        auscultacion_cardiovascular = request.POST.get('auscultacion_cardiovascular')
        descripcion_cardiovascular = request.POST.get('descripcion_cardiovascular')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        presion_arterial = request.POST.get('presion_arterial')
        pulso = request.POST.get('pulso')
        descripcion_fpp = request.POST.get('descripcion_fpp')
        inspeccion_abdominal = request.POST.get('inspeccion_abdominal')
        palpacion_abdominal = request.POST.get('palpacion_abdominal')
        auscultacion_abdominal = request.POST.get('auscultacion_abdominal')
        percusion_abdominal = request.POST.get('percusion_abdominal')
        descripcion_abdominal = request.POST.get('descripcion_abdominal')
        conciente = request.POST.get('conciente')
        orientado = request.POST.get('orientado')
        descripcion_sn_central = request.POST.get('descripcion_sn_central')
        signos_maningeos = request.POST.get('signos_maningeos')
        descripcion_signos_maningeos = request.POST.get('descripcion_signos_maningeos')
        pares_craneales = request.POST.get('pares_craneales')
        descripcion_pares_craneales = request.POST.get('descripcion_pares_craneales')
        soma = request.POST.get('soma')
        descripcion_soma = request.POST.get('descripcion_soma')
        genital_urinario = request.POST.get('genital_urinario')
        genital_urinario_descripcion = request.POST.get('genital_urinario_descripcion')
        mamas_simetricas = request.POST.get('mamas_simetricas')
        mamas_simetricas_descripcion = request.POST.get('mamas_simetricas_descripcion')
        mamas_nodulos = request.POST.get('mamas_nodulos')
        mamas_nodulos_descripcion = request.POST.get('mamas_nodulos_descripcion')
        estado_pezon = request.POST.get('estado_pezon')
        estado_pezon_descripcion = request.POST.get('estado_pezon_descripcion')
        estado_axila = request.POST.get('estado_axila')
        estado_axila_descripcion = request.POST.get('estado_axila_descripcion')
        genital_externo = request.POST.get('genital_externo')
        descripcion_genital_externo = request.POST.get('descripcion_genital_externo')
        peso = request.POST.get('peso')
        talla = request.POST.get('talla')
        indice_corporal = request.POST.get('indice_corporal')
        orientacion = request.POST.get('orientacion')
        proxima_cita = request.POST.get('proxima_cita')
        egeneral = EGeneral.objects.get(pk=pk_egeneral)
        
        efaparato = EFaparato(
            pym_humedo = pym_humedo,
            pym_coloreado = pym_coloreado,
            descripcion_pym = descripcion_pym,
            tvs = tvs,
            descripcion_tvs = descripcion_tvs,
            inspeccion_respiratoria = inspeccion_respiratoria,
            palpacion_respiratoria = palpacion_respiratoria,
            percusion_respiratoria = percusion_respiratoria,
            auscultacion_respiratoria = auscultacion_respiratoria,
            descripcion_respiratoria = descripcion_respiratoria,
            frecuencia_respiratoria = frecuencia_respiratoria,
            descripcion_frecuencia_respiratoria = descripcion_frecuencia_respiratoria,
            inspeccion_cardiovascular = inspeccion_cardiovascular,
            palpacion_cardiovascular = palpacion_cardiovascular,
            percusion_cardiovascular = percusion_cardiovascular,
            auscultacion_cardiovascular = auscultacion_cardiovascular,
            descripcion_cardiovascular = descripcion_cardiovascular,
            frecuencia_cardiaca = frecuencia_cardiaca,
            presion_arterial = presion_arterial,
            pulso = pulso,
            descripcion_fpp = descripcion_fpp,
            inspeccion_abdominal = inspeccion_abdominal,
            palpacion_abdominal = palpacion_abdominal,
            auscultacion_abdominal = auscultacion_abdominal,
            percusion_abdominal = percusion_abdominal,
            descripcion_abdominal = descripcion_abdominal,
            conciente = conciente,
            orientado = orientado,
            descripcion_sn_central = descripcion_sn_central,
            signos_maningeos = signos_maningeos,
            descripcion_signos_maningeos = descripcion_signos_maningeos,
            pares_craneales = pares_craneales,
            descripcion_pares_craneales = descripcion_pares_craneales,
            soma = soma,
            descripcion_soma = descripcion_soma,
            genital_urinario = genital_urinario,
            genital_urinario_descripcion = genital_urinario_descripcion,
            mamas_simetricas = mamas_simetricas,
            mamas_simetricas_descripcion = mamas_simetricas_descripcion,
            mamas_nodulos = mamas_nodulos,
            mamas_nodulos_descripcion = mamas_nodulos_descripcion,
            estado_pezon = estado_pezon,
            estado_pezon_descripcion = estado_pezon_descripcion,
            estado_axila = estado_axila,
            estado_axila_descripcion = estado_axila_descripcion,
            genital_externo = genital_externo,
            descripcion_genital_externo = descripcion_genital_externo,
            peso = peso,
            talla = talla,
            indice_corporal = indice_corporal,
            orientacion = orientacion,
            proxima_cita = proxima_cita,
            egeneral = egeneral,
            grupos = grupo,
            )
        efaparato.save()
        
        return redirect('ver_efaparato', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
    else:
        egeneral = EGeneral.objects.get(pk=pk_egeneral)
        return render(request, 'efaparato/crear_efaparato.html', {'egeneral': egeneral, 'grupos': grupos})
    


def modificar_efaparato(request, pk_paciente, pk_fecha, pk_egeneral, pk_efaparato):
    grupos = Grupos.objects.all()
    
    # Obtener el objeto EFaparato específico que se va a editar
    efaparato = get_object_or_404(EFaparato, egeneral_id=pk_egeneral)
    egeneral = efaparato.egeneral  # Obtener el objeto EGeneral asociado

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        grupo = get_object_or_404(Grupos, id=grupo_id)
        pym_humedo = request.POST.get('pym_humedo')
        pym_coloreado = request.POST.get('pym_coloreado')
        descripcion_pym = request.POST.get('descripcion_pym')
        tvs = request.POST.get('tvs')
        descripcion_tvs = request.POST.get('descripcion_tvs')
        inspeccion_respiratoria = request.POST.get('inspeccion_respiratoria')
        palpacion_respiratoria = request.POST.get('palpacion_respiratoria')
        percusion_respiratoria = request.POST.get('percusion_respiratoria')
        auscultacion_respiratoria = request.POST.get('auscultacion_respiratoria')
        descripcion_respiratoria = request.POST.get('descripcion_respiratoria')
        frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria')
        descripcion_frecuencia_respiratoria = request.POST.get('descripcion_frecuencia_respiratoria')
        inspeccion_cardiovascular = request.POST.get('inspeccion_cardiovascular')
        palpacion_cardiovascular = request.POST.get('palpacion_cardiovascular')
        percusion_cardiovascular = request.POST.get('percusion_cardiovascular')
        auscultacion_cardiovascular = request.POST.get('auscultacion_cardiovascular')
        descripcion_cardiovascular = request.POST.get('descripcion_cardiovascular')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        presion_arterial = request.POST.get('presion_arterial')
        pulso = request.POST.get('pulso')
        descripcion_fpp = request.POST.get('descripcion_fpp')
        inspeccion_abdominal = request.POST.get('inspeccion_abdominal')
        palpacion_abdominal = request.POST.get('palpacion_abdominal')
        auscultacion_abdominal = request.POST.get('auscultacion_abdominal')
        percusion_abdominal = request.POST.get('percusion_abdominal')
        descripcion_abdominal = request.POST.get('descripcion_abdominal')
        conciente = request.POST.get('conciente')
        orientado = request.POST.get('orientado')
        descripcion_sn_central = request.POST.get('descripcion_sn_central')
        signos_maningeos = request.POST.get('signos_maningeos')
        descripcion_signos_maningeos = request.POST.get('descripcion_signos_maningeos')
        pares_craneales = request.POST.get('pares_craneales')
        descripcion_pares_craneales = request.POST.get('descripcion_pares_craneales')
        soma = request.POST.get('soma')
        descripcion_soma = request.POST.get('descripcion_soma')
        genital_urinario = request.POST.get('genital_urinario')
        genital_urinario_descripcion = request.POST.get('genital_urinario_descripcion')
        mamas_simetricas = request.POST.get('mamas_simetricas')
        mamas_simetricas_descripcion = request.POST.get('mamas_simetricas_descripcion')
        mamas_nodulos = request.POST.get('mamas_nodulos')
        mamas_nodulos_descripcion = request.POST.get('mamas_nodulos_descripcion')
        estado_pezon = request.POST.get('estado_pezon')
        estado_pezon_descripcion = request.POST.get('estado_pezon_descripcion')
        estado_axila = request.POST.get('estado_axila')
        estado_axila_descripcion = request.POST.get('estado_axila_descripcion')
        genital_externo = request.POST.get('genital_externo')
        descripcion_genital_externo = request.POST.get('descripcion_genital_externo')
        peso = request.POST.get('peso')
        talla = request.POST.get('talla')
        indice_corporal = request.POST.get('indice_corporal')
        orientacion = request.POST.get('orientacion')
        proxima_cita = request.POST.get('proxima_cita')
        
        # Actualizar el objeto EFaparato con los nuevos datos
        efaparato.pym_humedo = pym_humedo
        efaparato.pym_coloreado = pym_coloreado
        efaparato.descripcion_pym = descripcion_pym
        efaparato.tvs = tvs
        efaparato.descripcion_tvs = descripcion_tvs
        efaparato.inspeccion_respiratoria = inspeccion_respiratoria
        efaparato.palpacion_respiratoria = palpacion_respiratoria
        efaparato.percusion_respiratoria = percusion_respiratoria
        efaparato.auscultacion_respiratoria = auscultacion_respiratoria
        efaparato.descripcion_respiratoria = descripcion_respiratoria
        efaparato.frecuencia_respiratoria = frecuencia_respiratoria
        efaparato.descripcion_frecuencia_respiratoria = descripcion_frecuencia_respiratoria
        efaparato.inspeccion_cardiovascular = inspeccion_cardiovascular
        efaparato.palpacion_cardiovascular = palpacion_cardiovascular
        efaparato.percusion_cardiovascular = percusion_cardiovascular
        efaparato.auscultacion_cardiovascular = auscultacion_cardiovascular
        efaparato.descripcion_cardiovascular = descripcion_cardiovascular
        efaparato.frecuencia_cardiaca = frecuencia_cardiaca
        efaparato.presion_arterial = presion_arterial
        efaparato.pulso = pulso
        efaparato.descripcion_fpp = descripcion_fpp
        efaparato.inspeccion_abdominal = inspeccion_abdominal
        efaparato.palpacion_abdominal = palpacion_abdominal
        efaparato.auscultacion_abdominal = auscultacion_abdominal
        efaparato.percusion_abdominal = percusion_abdominal
        efaparato.descripcion_abdominal = descripcion_abdominal
        efaparato.conciente = conciente
        efaparato.orientado = orientado
        efaparato.descripcion_sn_central = descripcion_sn_central
        efaparato.signos_maningeos = signos_maningeos
        efaparato.descripcion_signos_maningeos = descripcion_signos_maningeos
        efaparato.pares_craneales = pares_craneales
        efaparato.descripcion_pares_craneales = descripcion_pares_craneales
        efaparato.soma = soma
        efaparato.descripcion_soma = descripcion_soma
        efaparato.genital_urinario = genital_urinario
        efaparato.genital_urinario_descripcion = genital_urinario_descripcion
        efaparato.mamas_simetricas = mamas_simetricas
        efaparato.mamas_simetricas_descripcion = mamas_simetricas_descripcion
        efaparato.mamas_nodulos = mamas_nodulos
        efaparato.mamas_nodulos_descripcion = mamas_nodulos_descripcion
        efaparato.estado_pezon = estado_pezon
        efaparato.estado_pezon_descripcion = estado_pezon_descripcion
        efaparato.estado_axila = estado_axila
        efaparato.estado_axila_descripcion = estado_axila_descripcion
        efaparato.genital_externo = genital_externo
        efaparato.descripcion_genital_externo = descripcion_genital_externo
        efaparato.peso = peso
        efaparato.talla = talla
        efaparato.indice_corporal = indice_corporal
        efaparato.orientacion = orientacion
        efaparato.proxima_cita = proxima_cita
        efaparato.egeneral = egeneral
        efaparato.grupos = grupo
        
        
        efaparato.save()  # Guardar los cambios en el objeto EFaparato
        
        return redirect('ver_efaparato', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
    else:
        return render(request, 'efaparato/crear_efaparato.html', {'egeneral': egeneral, 'grupos': grupos, 'efaparato': efaparato})

    
def eliminar_efaparato(request, pk_paciente, pk_fecha, pk_egeneral, pk_efaparato):
    efaparato = get_object_or_404(EFaparato, pk=pk_efaparato)
    egeneral = get_object_or_404(EGeneral, pk=pk_egeneral)

    if request.method == 'POST':
        efaparato.delete()
        return redirect('ver_efaparato', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)

    context = {
        'efaparato': efaparato,
        'egeneral': egeneral,
        'pk_paciente': pk_paciente,
        'pk_fecha': pk_fecha,
        'pk_egeneral': pk_egeneral
    }
    return render(request, 'efaparato/eliminar_efaparato.html', context)




def grupos_pacientes(request):
    grupos = Grupos.objects.all()
    pacientes_por_grupo = {grupo.grupo: [] for grupo in grupos}

    # Crear un diccionario para mapear paciente a su última fecha y grupo correspondiente
    paciente_ultima_fecha_grupo = {}

    # Obtener todas las fechas ordenadas por fecha_inicial descendente por paciente
    fechas_por_paciente = {}
    for fecha in Fecha.objects.all().order_by('-fecha_inicial'):
        if fecha.paciente not in fechas_por_paciente:
            fechas_por_paciente[fecha.paciente] = fecha

    # Iterar sobre las fechas de cada paciente y obtener el último grupo seleccionado
    for paciente, fecha in fechas_por_paciente.items():
        try:
            egeneral = fecha.egeneral
            if egeneral:
                try:
                    efaparato = egeneral.efaparato
                    if efaparato:
                        grupo = efaparato.grupos
                        paciente_ultima_fecha_grupo[paciente] = grupo.grupo
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass

    # Agrupar pacientes por su último grupo seleccionado
    for paciente, ultimo_grupo in paciente_ultima_fecha_grupo.items():
        pacientes_por_grupo[ultimo_grupo].append({
            'ci': paciente.ci,
            'nombre': paciente.nombre,
            'apellidos': paciente.apellidos,
            'telefono': paciente.telefono,
        })

    context = {
        'pacientes_por_grupo': pacientes_por_grupo,
    }
    return render(request, 'grupos/grupos_pacientes.html', context)


def porcentaje_pacientes_por_grupo(request):
    grupos = Grupos.objects.all()
    pacientes_por_grupo = {grupo.grupo: [] for grupo in grupos}
    total_pacientes = 0

    # Crear un diccionario para mapear paciente a su última fecha y grupo correspondiente
    paciente_ultima_fecha_grupo = {}

    # Obtener todas las fechas ordenadas por fecha_inicial descendente por paciente
    fechas_por_paciente = {}
    for fecha in Fecha.objects.all().order_by('-fecha_inicial'):
        if fecha.paciente not in fechas_por_paciente:
            fechas_por_paciente[fecha.paciente] = fecha

    # Iterar sobre las fechas de cada paciente y obtener el último grupo seleccionado
    for paciente, fecha in fechas_por_paciente.items():
        try:
            egeneral = fecha.egeneral
            if egeneral:
                try:
                    efaparato = egeneral.efaparato
                    if efaparato:
                        grupo = efaparato.grupos
                        paciente_ultima_fecha_grupo[paciente] = grupo.grupo
                except ObjectDoesNotExist:
                    pass
        except ObjectDoesNotExist:
            pass

    # Contar el número total de pacientes y agrupar por último grupo seleccionado
    for paciente, ultimo_grupo in paciente_ultima_fecha_grupo.items():
        pacientes_por_grupo[ultimo_grupo].append(paciente)
        total_pacientes += 1

    porcentaje_pacientes_por_grupo = {}
    for grupo in grupos:
        grupo_pacientes = len(pacientes_por_grupo[grupo.grupo])
        grupo_porcentaje = (grupo_pacientes / total_pacientes) * 100 if total_pacientes > 0 else 0
        porcentaje_pacientes_por_grupo[grupo.grupo] = grupo_porcentaje

    return render(request, 'grupos/grupos_pacientes_porcentaje.html', {'porcentaje_pacientes_por_grupo': porcentaje_pacientes_por_grupo})


def render_pdf_view(request, pk_paciente, pk_fecha, pk_egeneral):
    # Obtén el interrogatorio que deseas mostrar en el PDF
    interrogatorio = get_object_or_404(Interrogatorio, egeneral__pk=pk_egeneral)
    
    # Contexto para pasar a la plantilla HTML
    context = {
        'interrogatorio': interrogatorio
    }
    
    # Renderizar la plantilla HTML
    template_path = 'interrogatorio/interrogatorio.html'  # Nombre de tu plantilla HTML
    template = get_template(template_path)
    html = template.render(context)
    
    # Crear un objeto HttpResponse con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="interrogatorio.pdf"'
    
    # Estilos específicos para el PDF (opcional)
    css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            .centered-title {
                text-align: center;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            /* Estilos específicos para el PDF */
            @media print {
                .no-pdf {
                    display: none; /* Ocultar elementos con la clase 'no-pdf' al imprimir */
                }
                .table {
                    page-break-inside: avoid; /* Evitar cortar tablas entre páginas */
                }
            }
        </style>
    """
    html = css + html  # Agregar estilos CSS al HTML
    
    html = remove_buttons(html)
    
    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Si se ha generado correctamente el PDF, devolverlo como respuesta
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % html)
    return response

def remove_buttons(html):
    """
    Función para eliminar botones del HTML generado.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for button in soup.find_all(class_='no-pdf'):
        button.decompose()  # Eliminar elemento del HTML

    return str(soup)

def render_pdf_efaparato(request, pk_paciente, pk_fecha, pk_egeneral):
    efaparato = get_object_or_404(EFaparato, egeneral__pk=pk_egeneral)
    template_path = 'efaparato/efaparato.html'  # Nombre del template HTML
    context = {'efaparato': efaparato}

    # Render template
    template = get_template(template_path)
    html = template.render(context)
    
    # Estilos específicos para el PDF (opcional)
    css = """
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            .centered-title {
                text-align: center;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            /* Estilos específicos para el PDF */
            @media print {
                .no-pdf {
                    display: none; /* Ocultar elementos con la clase 'no-pdf' al imprimir */
                }
                .table {
                    page-break-inside: avoid; /* Evitar cortar tablas entre páginas */
                }
            }
        </style>
    """
    html = css + html  # Agregar estilos CSS al HTML
    
    # Eliminar elementos no deseados (botones u otros elementos marcados)
    html = remove_elements(html)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="efaparato.pdf"'

    # Generar el PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='utf-8'
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def remove_elements(html):
    """
    Función para eliminar elementos no deseados del HTML generado.
    Aquí se puede ajustar para eliminar botones u otros elementos.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Ejemplo: eliminar elementos con clase 'no-pdf'
    for element in soup.select('.no-pdf'):
        element.decompose()

    # Convertir el soup de nuevo a HTML
    cleaned_html = str(soup)
    return cleaned_html


def pacientes_con_proxima_cita(request):
    # Lista de pacientes con próxima cita
    pacientes_con_cita = []

    # Obtener todos los pacientes
    pacientes = Paciente.objects.all()

    for paciente in pacientes:
        try:
            # Obtener la última fecha de cada paciente ordenada por fecha_inicial descendente
            ultima_fecha = Fecha.objects.filter(paciente=paciente).order_by('-fecha_inicial').first()

            if ultima_fecha:
                # Verificar si la última fecha tiene una cita próxima definida en EFaparato
                if ultima_fecha.egeneral and ultima_fecha.egeneral.efaparato and ultima_fecha.egeneral.efaparato.proxima_cita:
                    pacientes_con_cita.append({
                        'paciente': paciente,
                        'proxima_cita': ultima_fecha.egeneral.efaparato.proxima_cita
                    })

        except ObjectDoesNotExist:
            pass
    
    context = {
        'pacientes': pacientes_con_cita
    }
    
    return render(request, 'pacientes/lista_pacientes_proxima_cita.html', context)

