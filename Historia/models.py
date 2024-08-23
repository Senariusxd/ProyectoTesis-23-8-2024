from django.db import models

class Paciente(models.Model):
    ci = models.CharField(primary_key=True, max_length=11)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    telefono = models.IntegerField(null=True)
    direccion = models.CharField(max_length=255)
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    RAZA_CHOICES = (
        ('B', 'Blanco'),
        ('N', 'Negro'),
    )
    raza = models.CharField(max_length=1, choices=RAZA_CHOICES)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre



class Fecha(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_inicial = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='fechas')

    def __str__(self):
        return self.fecha_inicial

class EGeneral(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=750)
    fecha = models.OneToOneField(Fecha, on_delete=models.CASCADE, related_name='egeneral')

class Interrogatorio(models.Model):
    id = models.IntegerField(primary_key=True)
    AP_CHOICES = (
        ('S', 'Sí'),
        ('N', 'No'),
    )
    antecedentes_personales = models.CharField(max_length=1, choices=AP_CHOICES)
    ap_personal_descripcion = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.CharField(max_length=1, choices=AP_CHOICES)
    ap_familiar_descripcion = models.TextField(blank=True, null=True)
    HT_CHOICES = (
        ('T', 'Tabaco'),
        ('A', 'Alcohol'),
        ('D', 'Droga'),
    )
    h_toxicos = models.CharField(max_length=1, choices=AP_CHOICES)
    h_toxicos_descripcion = models.CharField(max_length=1, choices=HT_CHOICES)
    alergias = models.CharField(max_length=1, choices=AP_CHOICES)
    alergias_descripcion =models.TextField(blank=True, null=True)
    operaciones = models.CharField(max_length=1, choices=AP_CHOICES)
    operaciones_descripcion =models.TextField(blank=True, null=True)
    transfuciones = models.CharField(max_length=1, choices=AP_CHOICES)
    transfuciones_descripcion =models.TextField(blank=True, null=True)
    carnet_salud = models.CharField(max_length=1, choices=AP_CHOICES)
    carnet_salud_descripcion = models.DateTimeField(blank=True, null=True)
    p_enfermedad = models.CharField(max_length=1, choices=AP_CHOICES)
    p_enfermedad_descripcion =models.TextField(blank=True, null=True)
    OCUPATION_CHOICES = (
        ('E', 'Estudiante'),
        ('T', 'Trabajador de la Cocina'),
    )
    ocupacion = models.CharField(max_length=1, choices=OCUPATION_CHOICES)
    TYPES_CHOICES = (
        ('A', 'Ingeniero Informatico'),
        ('B', 'Ingeniero Mecanico'),
        ('C', 'Ingeniería Química'),
        ('D', 'Ingeniería Industrial'),
        ('E', 'Ingeniería en Transporte'),        
        ('F', 'Ingeniería en Agronomía'),
        ('G', 'Ingeniería en Procesos Agroindustriales'),
        ('H', 'Licenciatura en Derecho'),
        ('I', 'Licenciatura en Economía'),
        ('J', 'Licenciatura en Contabilidad y Finanzas'),
        ('K', 'Licenciatura en Turismo'),
        ('L', 'Licenciatura en Educación Economía'),
        ('M', 'Licenciatura en Educación Matemática'),
        ('N', 'Licenciatura en Gestión Sociocultural para el Desarrollo'),
        ('O', 'Licenciatura en Comunicación Social'),
        ('P', 'Licenciatura en Cultura Física'),
        ('Q', 'Licenciatura en Educación. Construcción'),
        ('R', 'Licenciatura en Educación. Mecánica'),
        ('S', 'Licenciatura en Educación. Informática'),
        ('T', 'Licenciatura en Educación. Química'),
        ('U', 'Licenciatura en Educación Laboral'),
        ('V', 'Licenciatura en Educación Física'),
        ('W', 'Licenciatura en Historia'),
        ('X', 'Licenciatura en Educación. Marxismo-Leninismo e Historia'),
        ('Y', 'Licenciatura en Educación. Español-Literatura'),
        ('Z', 'Licenciaturas en Educación. Lenguas Extranjeras. Inglés'),
        ('1', 'Licenciatura en Educación Artística'),
        ('2', 'Licenciatura en Educación Especial'),
        ('3', 'Licenciatura en Educación. Logopedia'),
        ('4', 'Licenciatura en Educación Primaria'),
        ('5', 'Licenciatura en Educación Preescolar'),
        ('6', 'Licenciatura en Educación. Pedagogía-Psicología'),
        ('7', 'Licenciatura en Educación. Biología'),
        ('8', 'Licenciatura en Educación. Geografía'),
        ('9', 'Licenciatura en Educación Agropecuaria'),
        ('0', 'Medicina Veterinaria'),
        ('+', 'Técnico Superior en Gestión de la Innovación Agraria'),
    )
    ocupacion_descripcion = models.TextField(max_length=1, choices=TYPES_CHOICES, blank=True, null=True)
    
    egeneral = models.OneToOneField(EGeneral, on_delete=models.CASCADE, related_name='interrogatorio')

class EFaparato(models.Model):
    id = models.IntegerField(primary_key=True)
    PYMHUMEDA_CHOICES = (
        ('S', 'Humeda'),
        ('N', 'No es Humeda'),
    )
    PYMCOLOR_CHOICES = (
        ('S', 'Normocoloreado'),
        ('N', 'No es Normocoloreado'),
    )
    TVS_CHOICES = (
        ('S', 'Infiltrado'),
        ('N', 'No Infiltrado'),
    )
    YON_CHOICES = (
        ('S', 'Sí'),
        ('N', 'No'),
    )
    NOP_CHOICES = (
        ('N', 'Normal'),
        ('P', 'Patológico'),
    )
    PUL_CHOICES = (
        ('P', 'Presente'),
        ('N', 'No Presente'),
    )
    pym_humedo = models.CharField(max_length=1, choices=PYMHUMEDA_CHOICES)
    pym_coloreado = models.CharField(max_length=1, choices=PYMCOLOR_CHOICES)
    descripcion_pym = models.TextField(blank=True, null=True)
    
    tvs = models.CharField(max_length=1, choices=YON_CHOICES)
    descripcion_tvs = models.TextField(blank=True, null=True)
    #Aparato Respiratorio
    inspeccion_respiratoria = models.CharField(max_length=1, choices=NOP_CHOICES)
    palpacion_respiratoria = models.CharField(max_length=1, choices=NOP_CHOICES)
    percusion_respiratoria = models.CharField(max_length=1, choices=NOP_CHOICES)
    auscultacion_respiratoria = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_respiratoria = models.TextField(blank=True, null=True)
    
    frecuencia_respiratoria = models.CharField(max_length=255)
    descripcion_frecuencia_respiratoria = models.TextField(blank=True, null=True)
    #Aparato Cardiovascular
    inspeccion_cardiovascular = models.CharField(max_length=1, choices=NOP_CHOICES)
    palpacion_cardiovascular = models.CharField(max_length=1, choices=NOP_CHOICES)
    percusion_cardiovascular = models.CharField(max_length=1, choices=NOP_CHOICES)
    auscultacion_cardiovascular = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_cardiovascular = models.TextField(blank=True, null=True)
    
    frecuencia_cardiaca = models.CharField(max_length=255)
    presion_arterial = models.CharField(max_length=255)
    pulso = models.CharField(max_length=1, choices=PUL_CHOICES)
    descripcion_fpp = models.TextField(blank=True, null=True)
    #Abdomen
    inspeccion_abdominal = models.CharField(max_length=1, choices=NOP_CHOICES)
    palpacion_abdominal = models.CharField(max_length=1, choices=NOP_CHOICES)
    auscultacion_abdominal = models.CharField(max_length=1, choices=NOP_CHOICES)
    percusion_abdominal = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_abdominal = models.TextField(blank=True, null=True)
    
    #Sistema Nervioso Central
    conciente = models.CharField(max_length=1, choices=YON_CHOICES)
    orientado = models.CharField(max_length=1, choices=YON_CHOICES)
    descripcion_sn_central = models.TextField(blank=True, null=True)
    signos_maningeos = models.CharField(max_length=1, choices=YON_CHOICES)
    descripcion_signos_maningeos = models.TextField(blank=True, null=True)
    pares_craneales = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_pares_craneales = models.TextField(blank=True, null=True)
    #Soma
    soma = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_soma = models.TextField(blank=True, null=True)
    
    genital_urinario = models.CharField(max_length=1, choices=NOP_CHOICES)
    genital_urinario_descripcion = models.TextField(blank=True, null=True)
    mamas_simetricas = models.CharField(max_length=1, choices=YON_CHOICES)
    mamas_simetricas_descripcion = models.TextField(blank=True, null=True)
    mamas_nodulos = models.CharField(max_length=1, choices=YON_CHOICES)
    mamas_nodulos_descripcion = models.TextField(blank=True, null=True)
    estado_pezon = models.CharField(max_length=1, choices=NOP_CHOICES)
    estado_pezon_descripcion = models.TextField(blank=True, null=True)
    estado_axila = models.CharField(max_length=1, choices=NOP_CHOICES)
    estado_axila_descripcion = models.TextField(blank=True, null=True)
    genital_externo = models.CharField(max_length=1, choices=NOP_CHOICES)
    descripcion_genital_externo = models.TextField(blank=True, null=True)
    
    peso = models.CharField(max_length=255)
    talla = models.CharField(max_length=255)
    indice_corporal = models.CharField(max_length=255)
    
    orientacion = models.CharField(max_length=255)
    proxima_cita = models.DateTimeField()
    egeneral = models.OneToOneField(EGeneral, on_delete=models.CASCADE, related_name='efaparato')
    grupos = models.ForeignKey('Grupos', on_delete=models.CASCADE, related_name='efaparatos')

class Grupos(models.Model):
    id = models.IntegerField(primary_key=True)
    grupo = models.CharField(max_length=255)

    def __str__(self):
        return self.grupo