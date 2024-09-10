from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Max
from ..models import Paciente, EGeneral, Interrogatorio, Fecha
from django.contrib.auth.decorators import login_required, permission_required


@login_required(login_url="/")
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

@login_required(login_url="/")
@permission_required("estudiantes.add_interrogatorio", login_url="/")
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

@login_required(login_url="/")
@permission_required("estudiantes.change_interrogatorio", login_url="/")
def modificar_interrogatorio(request, pk_paciente, pk_fecha, pk_egeneral, pk_interrogatorio):
    paciente = get_object_or_404(Paciente, pk=pk_paciente)
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
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.antecedentes_familiares == 'S' and not interrogatorio.ap_familiar_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.h_toxicos == 'S' and not interrogatorio.h_toxicos_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.alergias == 'S' and not interrogatorio.alergias_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.operaciones == 'S' and not interrogatorio.operaciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.transfuciones == 'S' and not interrogatorio.transfuciones_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

        if interrogatorio.p_enfermedad == 'S' and not interrogatorio.p_enfermedad_descripcion:
            egeneral = EGeneral.objects.get(pk=pk_egeneral)
            messages.error(request, "El campo es obligatorio.")
            return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral})

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
        return render(request, 'interrogatorio/modificar_interrogatorio.html', {'interrogatorio': interrogatorio, 'egeneral': egeneral, 'paciente': paciente,})

@login_required(login_url="/")
@permission_required("estudiantes.delete_interrogatorio", login_url="/")
def eliminar_interrogatorio(request, pk_interrogatorio, pk_paciente, pk_fecha, pk_egeneral):
    # Mostrar página de confirmación
    if request.method == 'GET':
        return render(request, 'interrogatorio/eliminar_interrogatorio.html', {
            'pk_interrogatorio': pk_interrogatorio,
            'pk_paciente': pk_paciente,
            'pk_fecha': pk_fecha,
            'pk_egeneral': pk_egeneral
        })

    # Procesar confirmación de eliminación
    elif request.method == 'POST':
        interrogatorio = get_object_or_404(Interrogatorio, pk=pk_interrogatorio)
        interrogatorio.delete()
        messages.success(request, "El interrogatorio ha sido eliminado correctamente.")
        return redirect('ver_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)

    # Manejar el caso de método no permitido
    else:
        messages.error(request, "Método no permitido.")
        return redirect('ver_interrogatorio', pk_paciente=pk_paciente, pk_fecha=pk_fecha, pk_egeneral=pk_egeneral)
