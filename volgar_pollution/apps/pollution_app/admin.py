from django.contrib import admin

from pollution_app.models import Impurities, ImpuritiesData


class ImpuritiesDataAdmin(admin.ModelAdmin):
    readonly_fields = ('datetime',)
    list_display = ('datetime', 'impurity_id', 'value_st', 'value_pdk') 


admin.site.register(ImpuritiesData, ImpuritiesDataAdmin)
admin.site.register(Impurities)