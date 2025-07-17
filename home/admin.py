
from .models import PlasticCollection,Product, Employee, Profile, Testimonial, Project, Contact, Job

from django.contrib import admin

admin.site.site_header = "Sargasso Reclamation Admin"
admin.site.site_title = "Sargasso Admin Portal"
admin.site.index_title = "Welcome to the Admin Dashboard"

class PaslticAdmin(admin.ModelAdmin):
    ordering = ('category',)  
    list_display = ('date', 'amount_kg', 'category', 'region')  # Column headers in admin list view

admin.site.register(PlasticCollection, PaslticAdmin)  # Register the model with the custom admin class

class Product_de(admin.ModelAdmin):
    list_display = ('title', 'category')  # Column headers in admin list view

admin.site.register(Employee)

admin.site.register(Product, Product_de)  # Register the model with the custom admin class
admin.site.register(Profile) 
admin.site.register(Testimonial) 
admin.site.register(Project) 
admin.site.register(Contact) 
admin.site.register(Job) 