from django.contrib import admin
from .models import Deep

# Register your models here.
class DeepAdmin(admin.ModelAdmin):
    list_display = ('title', 'usage', 'added_by', 'created_date')
    list_filter = ('created_date',)
    ordering = ('title', )
    search_fields = ('title', )
    readonly_fields = ('created_date', )

    fieldsets = (
        (None, {
            'fields': ('title', 'usage', 'reference', 'added_by')
        }),
        ('More details', {
             'classes': ('collapse', ),
             'fields': ('description', 'parameters', 'code', 'script')
        }),
    )

admin.site.register(Deep, DeepAdmin)
