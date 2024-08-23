from django.shortcuts import render, redirect, get_object_or_404
from ...formsP import EGeneralForm
from ...models import Paciente, Fecha, EGeneral

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