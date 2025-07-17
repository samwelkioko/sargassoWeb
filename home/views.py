
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
import datetime
import pandas as pd
from .forms import ExcelUploadForm
from .models import *
from django.contrib import messages
import json

def custom_404(request, exception):
    return render(request, '404.html', status=404)
def homepage(request):
   
    testimonial = Testimonial.objects.all()

    context= {
        'testimonial':testimonial,
         }
    
    return render(request,'index.html',context=context)

def about(request):
    employee = Employee.objects.all()
   
    context= {
      'employee':employee,
    }
    return render(request,'about.html', context)
def offer(request):
    
    return render(request,'offer.html')
def droppoint(request):
    
    return render(request,'droppoint.html')
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

def impact_view(request):
    # Get all records
    qs = PlasticCollection.objects.all()

    # Distinct years for dropdown
    years = qs.dates('date', 'year', order='DESC')  # gives list of datetime.date objects

    # Initial data (e.g. current year if desired)
    selected_year = request.GET.get('year')
    if selected_year:
        qs = qs.filter(date__year=selected_year)

    # Monthly aggregation
    monthly_data = (
        qs.annotate(month=TruncMonth('date'))
          .values('month')
          .annotate(total_kg=Sum('amount_kg'))
          .order_by('month')
    )

    labels = [calendar.month_abbr[d['month'].month] for d in monthly_data]
    values = [round(d['total_kg'], 2) for d in monthly_data]

    context = {
        'labels': labels,
        'values': values,
        'years': years,
    }
    return render(request, 'impact.html', context)


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


def import_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                # Read Excel file
                df = pd.read_excel(excel_file)

                # Validate expected columns
                required_columns = {'Date', 'Category', 'Amount(kg)', 'Region'}
                if not required_columns.issubset(df.columns):
                    missing = required_columns - set(df.columns)
                    messages.error(request, f"Missing columns in Excel file: {', '.join(missing)}")
                    return render(request, 'import.html', {'form': form})

                # Optional: clear previous entries or check duplicates

                # Loop through rows and create Employee instances
                for index, row in df.iterrows():
                    # Validate fields
                    if pd.isnull(row['Date']) or pd.isnull(row['Category']) or pd.isnull(row['Amount(kg)']) or pd.isnull(row['Region']):
                        messages.error(request, f"Row {index + 2} has missing data.")  # +2 for header and 0-index
                        return render(request, 'import.html', {'form': form})

                    PlasticCollection.objects.create(
                        date=row['Date'],
                        region=row['Region'],
                        category=row['Category'],
                        amount_kg=row['Amount(kg)']
                    )

                messages.success(request, "Excel file imported successfully.")
                return render(request, 'import.html', {'form': ExcelUploadForm()})

            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return render(request, 'import.html', {'form': form})

    else:
        form = ExcelUploadForm()

    return render(request, 'import.html', {'form': form})
