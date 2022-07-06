"""Filtering classes."""

# Django
from django.contrib import admin

class MonthFilter(admin.SimpleListFilter):
    title = ("Month")
    parameter_name = ("month")
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    def lookups(self, request, model_admin):
        return [(x, m) for x, m in zip(range(1, 13), self.months)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__month=self.value())
        else:
            return queryset