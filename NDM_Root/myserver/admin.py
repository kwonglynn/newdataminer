from django.contrib import admin
from .models import Dict

# Register your models here.
class DictAdmin(admin.ModelAdmin):
    list_display = ('word', 'morf', 'word_forms', 'word_user', 'name_label', 'last_date', 'last_name_date_label', 'trans_all')
    list_filter = ('added_by', 'last_date')
    ordering = ('word', )
    search_fields = ('word','word_forms')
    # readonly_fields = ('created_date', 'last_date')

admin.site.register(Dict, DictAdmin)
