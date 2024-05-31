from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass