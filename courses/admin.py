from django.contrib import admin

from courses.models import Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    ...
