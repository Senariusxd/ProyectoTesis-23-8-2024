from django.contrib import admin

from .models import Paciente, Fecha, EGeneral , Interrogatorio, EFaparato, Grupos

admin.site.register(Paciente)
admin.site.register(Fecha)
admin.site.register(EGeneral)
admin.site.register(Interrogatorio)
admin.site.register(EFaparato)
admin.site.register(Grupos)
