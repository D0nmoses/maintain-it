from django.contrib import admin
from .models import Profile, DocumentationRecord, Hardware, MaintenanceRecord, MaintenanceType, Software, SysAdmin, System

# Register your models here.
admin.site.register(Profile)
admin.site.register(DocumentationRecord)
admin.site.register(Hardware)
admin.site.register(MaintenanceRecord)
admin.site.register(MaintenanceType)
admin.site.register(Software)
admin.site.register(SysAdmin)
admin.site.register(System)
