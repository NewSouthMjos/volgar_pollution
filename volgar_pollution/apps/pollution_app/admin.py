from django.contrib import admin

from pollution_app.models import Impurity, ImpurityData


class ImpurityDataAdmin(admin.ModelAdmin):
    readonly_fields = ('datetime',)
    list_display = ('datetime', 'impurity_id', 'value_st', 'value_pdk') 


admin.site.register(ImpurityData, ImpurityDataAdmin)
admin.site.register(Impurity)