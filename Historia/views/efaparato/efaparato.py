from django.shortcuts import render, redirect, get_object_or_404

from ...models import Grupos, EGeneral, EFaparato


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