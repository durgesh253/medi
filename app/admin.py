from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
# Register your models here.

admin.site.register(staff)

admin.site.register(Doctor)
admin.site.register(role)
# admin.site.register(DoctorPost)
# admin.site.register(PatientBook)

admin.site.register(Patient)
admin.site.unregister(Group)
admin.site.unregister(User)