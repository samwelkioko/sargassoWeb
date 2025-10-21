# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import PlasticCollection, Product, Employee
import json
from datetime import datetime


def board_view(request):
    selected_region = request.GET.get("region")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    plastic_qs = PlasticCollection.objects.all()

    # Apply region filter
    if selected_region:
        plastic_qs = plastic_qs.filter(region=selected_region)

    # Apply date range filter
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            plastic_qs = plastic_qs.filter(date__range=[start, end])
        except ValueError:
            pass

    # KPI calculations
    total_plastic = plastic_qs.aggregate(total=Sum("amount_kg"))["total"] or 0
    total_products = Product.objects.count()
    total_employees = Employee.objects.count()

    # Chart data
    plastic_by_category = list(
        plastic_qs.values("category").annotate(total=Sum("amount_kg")).order_by("-total")
    )
    products_by_category = list(
        Product.objects.values("category").annotate(total=Count("id")).order_by("-total")
    )
    employees_by_position = list(
        Employee.objects.values("position").annotate(total=Count("id")).order_by("-total")
    )

    # Handle AJAX requests
    if request.headers.get("x-requested-with") == "X
