from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib import messages
import calendar
import pandas as pd
import datetime
import logging
import json

from .forms import ExcelUploadForm
from .models import *

logger = logging.getLogger(__name__)


# --- Basic Pages ---
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def homepage(request):
    testimonial = Testimonial.objects.all()
    partner = Partner.objects.all()
    profile = Profile.objects.all()
    return render(request, 'index.html', {'testimonial': testimonial,'partner': partner, 'profile': profile})

def about(request):
    employee = Employee.objects.all()
    profile = Profile.objects.all()
    return render(request, 'about.html', {'employee': employee, 'profile': profile})

def offer(request):
    return render(request, 'offer.html')

def droppoint(request):
    return render(request, 'droppoint.html')

def product(request):
    items = Product.objects.all()
    menu_data = [
        {
            "id": item.id,
            "title": item.title,
            "category": item.category,
            "price": float(item.price),
            "img": item.img.url.lstrip('/'),
            "desc": item.desc
        } for item in items
    ]
    return render(request, "product.html", {"menu_json": json.dumps(menu_data)})


# --- Impact Visualization ---
def impact_view(request):
    qs = PlasticCollection.objects.all()
    years = qs.dates('date', 'year', order='DESC')

    selected_year = request.GET.get('year')
    if selected_year:
        qs = qs.filter(date__year=selected_year)

    monthly_data = (
        qs.annotate(month=TruncMonth('date'))
          .values('month')
          .annotate(total_kg=Sum('amount_kg'))
          .order_by('month')
    )

    labels = [calendar.month_abbr[d['month'].month] for d in monthly_data]
    values = [round(d['total_kg'], 2) for d in monthly_data]

    return render(request, 'impact.html', {
        'labels': labels,
        'values': values,
        'years': years,
    })


def chart_data_by_year(request):
    year = request.GET.get('year')
    qs = PlasticCollection.objects.all()
    if year:
        qs = qs.filter(date__year=year)

    monthly_data = (
        qs.annotate(month=TruncMonth('date'))
          .values('month')
          .annotate(total_kg=Sum('amount_kg'))
          .order_by('month')
    )

    labels = [calendar.month_abbr[d['month'].month] for d in monthly_data]
    values = [round(d['total_kg'], 2) for d in monthly_data]

    return JsonResponse({'labels': labels, 'values': values})


# --- Excel Import ---
def import_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            if not excel_file.name.endswith(('.xls', '.xlsx')):
                messages.error(request, "Invalid file format. Please upload an Excel file (.xls or .xlsx).")
                return render(request, 'import.html', {'form': form})

            try:
                df = pd.read_excel(excel_file, usecols=['Date', 'Category', 'Amount(kg)', 'Region'])

                required_columns = {'Date', 'Category', 'Amount(kg)', 'Region'}
                if not required_columns.issubset(df.columns):
                    missing = required_columns - set(df.columns)
                    messages.error(request, f"Missing columns: {', '.join(missing)}")
                    return render(request, 'import.html', {'form': form})

                # Clean and convert fields
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Amount(kg)'] = pd.to_numeric(df['Amount(kg)'], errors='coerce')
                df['Category'] = df['Category'].astype(str).str.strip()
                df['Region'] = df['Region'].astype(str).str.strip()

                existing_set = set(PlasticCollection.objects.values_list('date', 'region', 'category'))
                plastic_entries = []
                errors = []

                for index, row in df.iterrows():
                    row_number = index + 2
                    if pd.isnull(row['Date']) or pd.isnull(row['Category']) or pd.isnull(row['Amount(kg)']) or pd.isnull(row['Region']):
                        errors.append(f"Row {row_number}: missing data.")
                        continue

                    key = (row['Date'], row['Region'], row['Category'])
                    if key in existing_set:
                        errors.append(f"Row {row_number}: duplicate entry skipped.")
                        continue

                    try:
                        entry = PlasticCollection(
                            date=row['Date'],
                            region=row['Region'],
                            category=row['Category'],
                            amount_kg=row['Amount(kg)']
                        )
                        plastic_entries.append(entry)
                    except Exception as e:
                        errors.append(f"Row {row_number}: {str(e)}")

                if plastic_entries:
                    PlasticCollection.objects.bulk_create(plastic_entries)

                if errors:
                    messages.warning(request, "File imported with issues. See below.")
                    return render(request, 'import.html', {
                        'form': ExcelUploadForm(),
                        'errors': errors
                    })
                else:
                    messages.success(request, "Excel file imported successfully.")
                    return render(request, 'import.html', {'form': ExcelUploadForm()})

            except Exception as e:
                logger.exception("Excel import failed.")
                messages.error(request, f"Error reading file: {str(e)}")
                return render(request, 'import.html', {'form': form})

    else:
        form = ExcelUploadForm()

    return render(request, 'import.html', {'form': form})
