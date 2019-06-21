from django.contrib import admin
from .models import Dict

# Register your models here.
class DictAdmin(admin.ModelAdmin):
    list_display = ('word', 'pron', 'morf', 'forms', 'trans', 'last_date', 'accordion_id')
    list_filter = ('added_by', 'last_date')
    ordering = ('word', 'accordion_id')
    search_fields = ('word', )
    readonly_fields = ('created_date', 'last_date')

admin.site.register(Dict, DictAdmin)
