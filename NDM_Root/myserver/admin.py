from django.contrib import admin
from .models import Dict

# Register your models here.
class DictAdmin(admin.ModelAdmin):
    list_display = ('word', 'pron', 'morf', 'forms', 'trans', 'last_date')
    list_filter = ('last_date',)
    ordering = ('word', )
    search_fields = ('word', )
    readonly_fields = ('created_date', 'last_date')

admin.site.register(Dict, DictAdmin)
