from django.contrib import admin
from .models import Module

# Register your models here.
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'submitted')
    list_filter = ('type', 'submitted')
    ordering = ('title', )
    search_fields = ('title', )
    readonly_fields = ('submitted', )

    fieldsets = (
        (None, {
            'fields': ('title', 'type', 'reference', 'description', 'submitted')
        }),
        # ('Module Information', {
        #     'classes': ('collapse', ),
        #     'fields': ('reference', 'description', 'submitted')
        # }),
    )


admin.site.register(Module, ModuleAdmin)
