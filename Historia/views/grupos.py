from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Max, Count, Q
from django.core.exceptions import ObjectDoesNotExist
from ..models import  Fecha, Grupos, Paciente, EGeneral, Interrogatorio
from django.contrib.auth.decorators import login_required



@login_required(login_url="/")
def grupos_pacientes(request):
    pacientes = []

    # Obtener el término de búsqueda
    search_term = request.GET.get('search', '')

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

    # Agrupar todos los pacientes en una lista
    for paciente in paciente_ultima_fecha_grupo.keys():
        grupo = paciente_ultima_fecha_grupo[paciente]
        pacientes.append({
            'grupo': grupo,
            'ci': paciente.ci,
            'nombre': paciente.nombre,
            'apellidos': paciente.apellidos,
            'telefono': paciente.telefono,
        })

    # Filtrar por búsqueda
    if search_term:
        pacientes = [p for p in pacientes if search_term.lower() in p['nombre'].lower() or search_term.lower() in p['apellidos'].lower()]

    # Paginación
    paginator = Paginator(pacientes, 5)  # 5 pacientes por página
    page_number = request.GET.get('page')
    paginated_patients = paginator.get_page(page_number)

    context = {
        'pacientes': paginated_patients,
        'search': search_term,  # Para mantener el valor en el formulario
    }
    return render(request, 'grupos/grupos_pacientes.html', context)

@login_required(login_url="/")
def estadisticas_generales_view(request):
    # Obtener la última fecha para cada paciente
    latest_fecha_per_paciente = Fecha.objects.values('paciente').annotate(
        latest_fecha=Max('fecha_inicial')
    ).values('paciente', 'latest_fecha')

    # Obtener el id del EGeneral relacionado con la última fecha de cada paciente
    egeneral_per_paciente = EGeneral.objects.filter(
        fecha__in=Fecha.objects.filter(
            paciente__in=[entry['paciente'] for entry in latest_fecha_per_paciente],
            fecha_inicial__in=[entry['latest_fecha'] for entry in latest_fecha_per_paciente]
        )
    ).values('id', 'fecha_id')

    # Obtener el Interrogatorio relacionado con el EGeneral más reciente
    interrogatorio_per_paciente = Interrogatorio.objects.filter(
        egeneral__in=[entry['id'] for entry in egeneral_per_paciente]
    ).values('ocupacion', 'ocupacion_descripcion')

    # Contar ocupaciones
    occupation_counts = interrogatorio_per_paciente.aggregate(
        total_estudiantes=Count('id', filter=Q(ocupacion='E')),
        total_trabajadores=Count('id', filter=Q(ocupacion='T'))
    )

    # Contar la cantidad de estudiantes por carrera
    carrera_counts = (
        interrogatorio_per_paciente
        .filter(ocupacion='E')
        .values('ocupacion_descripcion')
        .annotate(count=Count('ocupacion_descripcion'))
        .order_by('ocupacion_descripcion')
    )

    # Obtener estadísticas generales
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
                efaparato = egeneral.efaparato
                if efaparato:
                    grupo = efaparato.grupos
                    paciente_ultima_fecha_grupo[paciente] = grupo.grupo
        except ObjectDoesNotExist:
            pass

    # Contar el número total de pacientes y agrupar por último grupo seleccionado
    for paciente, ultimo_grupo in paciente_ultima_fecha_grupo.items():
        pacientes_por_grupo[ultimo_grupo].append(paciente)
        total_pacientes += 1

    # Calcular porcentajes por grupo
    porcentaje_pacientes_por_grupo = {}
    for grupo in grupos:
        grupo_pacientes = len(pacientes_por_grupo[grupo.grupo])
        grupo_porcentaje = (grupo_pacientes / total_pacientes) * 100 if total_pacientes > 0 else 0
        porcentaje_pacientes_por_grupo[grupo.grupo] = grupo_porcentaje

    # Inicializar contadores para los rangos de índice corporal
    rango_peso_insuficiente = 0
    rango_normal = 0
    rango_sobrepeso = 0
    rango_obesidad = 0

    # Obtener índice corporal de la última fecha de cada paciente
    resultados_indice_corporal = []
    for paciente in Paciente.objects.prefetch_related('fechas__egeneral__efaparato'):
        ultima_fecha = paciente.fechas.order_by('-fecha_inicial').first()
        if ultima_fecha:
            egeneral = ultima_fecha.egeneral
            if egeneral and hasattr(egeneral, 'efaparato'):
                efaparato = egeneral.efaparato
                if efaparato:
                    indice_corporal = efaparato.indice_corporal
                    resultados_indice_corporal.append({
                        'nombre': paciente.nombre,
                        'apellidos': paciente.apellidos,
                        'indice_corporal': indice_corporal,
                    })

                    # Clasificar el índice corporal en rangos
                    if indice_corporal < 18.5:
                        rango_peso_insuficiente += 1
                    elif 18.5 <= indice_corporal <= 24.9:
                        rango_normal += 1
                    elif 25.0 <= indice_corporal <= 29.9:
                        rango_sobrepeso += 1
                    elif indice_corporal >= 30.0:
                        rango_obesidad += 1

    # Preparar datos para el gráfico de rangos
    rangos = {
        'Peso_Insuficiente': rango_peso_insuficiente,
        'Peso_Normal': rango_normal,
        'Sobrepeso': rango_sobrepeso,
        'Obesidad': rango_obesidad,
    }

    # Contar totales de pacientes
    total_masculino = Paciente.objects.filter(sexo='M').count()
    total_femenino = Paciente.objects.filter(sexo='F').count()
    total_blanco = Paciente.objects.filter(raza='B').count()
    total_negro = Paciente.objects.filter(raza='N').count()

    # Preparar datos para Chart.js
    context = {
        'total_estudiantes': occupation_counts['total_estudiantes'],
        'total_trabajadores': occupation_counts['total_trabajadores'],
        'carrera_counts': list(carrera_counts),  # Convertir queryset a lista
        'porcentaje_pacientes_por_grupo': porcentaje_pacientes_por_grupo,
        'resultados_indice_corporal': resultados_indice_corporal,
        'total_masculino': total_masculino,
        'total_femenino': total_femenino,
        'total_blanco': total_blanco,
        'total_negro': total_negro,
        'rangos': rangos,
    }

    return render(request, 'grupos/estadisticas_generales.html', context)
