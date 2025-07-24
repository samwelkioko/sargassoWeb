from django.db import models

class PlasticCollection(models.Model):
    CATEGORY_CHOICES = [
        ('PET', 'PET'),
        ('HDPE', 'HDPE'),
        ('LDPE', 'LDPE'),
        ('PP', 'PP'),
        ('Other', 'Other'),
    ]

    date = models.DateField()
    amount_kg = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.amount_kg} kg - {self.category} - {self.region}"

class Product(models.Model):
    CATEGORY_CHOICE = [
        ('3D-PRINTS', '3D-PRINTS'),
        ('BALES', 'BALES'),
        ('PELLETS', 'PELLETS'),
        ('JEWELLERY', 'JEWELLERY'),
        ('FLAKES', 'FLAKES'),
        ('OTHERS', 'OTHERS'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.ImageField(upload_to="assets/img/")
    desc = models.TextField()

    def __str__(self):
        return self.title

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    facebook = models.TextField()
    linkedin = models.TextField()
    twitter = models.TextField()
    linkedin = models.TextField()
    img = models.ImageField(upload_to="assets/img/")

    def __str__(self):
         return self.name

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    mission = models.TextField()
    vision = models.TextField()
    history = models.TextField()
    

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    testimony = models.TextField()
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.name
    
class Partner(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

class Contact(models.Model):
    title = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    education = models.TextField()
    location = models.TextField()
    experience = models.TextField()
    requirements = models.TextField()

    def __str__(self):
        return self.title