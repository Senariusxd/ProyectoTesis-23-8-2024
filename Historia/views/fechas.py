from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from ..models import Paciente, Fecha

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