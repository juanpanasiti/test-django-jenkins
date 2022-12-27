from django.contrib import admin

from .models import CreditCard, Installment, Period, Purchase

# Register your models here.
admin.site.register(CreditCard)
admin.site.register(Installment)
admin.site.register(Period)
admin.site.register(Purchase)
