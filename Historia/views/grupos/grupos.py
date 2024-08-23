from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from ...models import  Fecha, Grupos



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