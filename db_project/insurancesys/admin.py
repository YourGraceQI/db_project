from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'c_id',
        'c_firstname',
        'c_lastname',
        'c_street',
        'c_city',
    )

    fields = [
        'c_id',
        'c_firstname',
        'c_lastname',
        'c_street',
        'c_city',
    ]


admin.site.register(Customer, CustomerAdmin)
