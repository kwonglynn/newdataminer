from django.contrib import admin
from .models import Module

# Register your models here.
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'added_by',  'type', 'created_date')
    list_filter = ('type', 'created_date')
    ordering = ('title', )
    search_fields = ('title', )
    readonly_fields = ('created_date', )

    fieldsets = (
        (None, {
            'fields': ('title', 'added_by', 'type', 'usage', 'reference', 'description', 'code', 'script', 'created_date')
        }),
        # ('Module Information', {
        #     'classes': ('collapse', ),
        #     'fields': ('reference', 'description', 'created_date')
        # }),
    )


admin.site.register(Module, ModuleAdmin)
