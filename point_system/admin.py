from django.contrib import admin
from .models import PointSystem, ContractorPoints
@admin.register(PointSystem)
class PointSystemAdmin(admin.ModelAdmin):
    list_display = ('product', 'minimum_quantity', 'points_awarded')
    search_fields = ('product__specification',)

@admin.register(ContractorPoints)
class ContractorPointsAdmin(admin.ModelAdmin):
    list_display = ('contractor_code', 'order_id', 'points')
    search_fields = ('contractor_code', 'order_id')
    list_filter = ('points',)

# admin.py
from django.contrib import admin
from .models import ContractorPointSummary

@admin.register(ContractorPointSummary)
class ContractorPointSummaryAdmin(admin.ModelAdmin):
    list_display = ['contractor_code', 'total_points']
    search_fields = ['contractor_code']