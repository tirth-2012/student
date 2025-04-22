from django.contrib import admin
from .models import studentdata,fees,attendance,Note

# Register your models here.

admin.site.register(studentdata)
admin.site.register(fees)
admin.site.register(attendance)
admin.site.register(Note)
