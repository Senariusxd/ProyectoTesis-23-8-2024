from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..models import Paciente, Fecha
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url="/")
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

@login_required(login_url="/")
@permission_required("estudiantes.add_paciente", login_url="/")
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

@login_required(login_url="/")
@permission_required("estudiantes.change_paciente", login_url="/")
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

@login_required(login_url="/")
@permission_required("estudiantes.delete_paciente", login_url="/")
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')

    context = {
        'paciente': paciente
    }
    return render(request, 'pacientes/eliminar_paciente.html', context)

@login_required(login_url="/")
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
