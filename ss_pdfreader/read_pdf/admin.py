from django.contrib import admin
from .models import template, Fields, Jobs


# Register your models here.

class TemplateAdmin(admin.ModelAdmin):
    list_display = [x.name for x in template._meta.fields]


class FieldsAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Fields._meta.fields]


class JobsAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Jobs._meta.fields]


admin.site.register(Fields, FieldsAdmin)
admin.site.register(template, TemplateAdmin)
admin.site.register(Jobs, JobsAdmin)
