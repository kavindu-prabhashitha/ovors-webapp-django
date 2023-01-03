from django.contrib import admin
from .models import Service, ServicePart, PartForService

# Register your models here.
admin.site.register(Service)
admin.site.register(ServicePart)
admin.site.register(PartForService)
