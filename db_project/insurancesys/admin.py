from django.contrib import admin

from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'c_id',
        'c_firstname',
        'c_lastname',
        'c_street',
        'c_city',
        'c_state',
        'c_zipcode',
        'c_gender',
        'c_maritalstatus',
        'c_customertype',
    )


admin.site.register(models.Customer, CustomerAdmin)

class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        'startdate',
        'enddate',
        'premium_amount',
        'policy_status',
        'policy_type',
        'c_id',
    )


admin.site.register(models.Policy, PolicyAdmin)
admin.site.register(models.Invoice)
admin.site.register(models.Payment)
admin.site.register(models.Home)
admin.site.register(models.Vehicle)
admin.site.register(models.Driver)

