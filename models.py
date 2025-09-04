from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class User(AbstractUser):

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

class DoctorProfile(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return f"Dr. {self.name}"

class PatientProfile(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name or "Unknown Patient"
class Appointment(models.Model):
    STATUS_REQUESTED = 0
    STATUS_CONFIRMED = 1
    STATUS_COMPLETED = 2
    STATUS_CANCELLED = 3

    STATUS_CHOICES = (
        (STATUS_REQUESTED, "Requested"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    doctor_name = models.CharField(max_length=100, blank=True, default="")
    patient_name = models.CharField(max_length=100, blank=True, default="")
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_REQUESTED)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor_name} for {self.patient_name} ({self.get_status_display()})"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class HospitalMessage(models.Model):
    CATEGORY_CHOICES = [
        ('appointment', 'Appointment'),
        ('payment', 'Payment'),
        ('system', 'System'),
        ('patient', 'Patient'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"{self.title} - {self.category}"



class HospitalPackage(models.Model):
    PACKAGE_TYPES = (
        ('health_checkup', 'Health Check-up'),
        ('cancer_screening', 'Cancer Screening'),
        ('orthopedic', 'Orthopedic'),
        ('neurology', 'Neurology'),
        ('child_care','Child Care')
    )

    name = models.CharField(max_length=255)
    package_type = models.CharField(max_length=50, choices=PACKAGE_TYPES)
    description = models.TextField()
    services_included = models.TextField(help_text="List of services separated by comma")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    special_offer = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def services_list(self):
        return self.services_included.split(',')

    def __str__(self):
        return self.name


class PackageBooking(models.Model):
    STATUS = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('success','Success'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(HospitalPackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='created')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


# appointments/models.py


class Medication(models.Model):
    CATEGORY_CHOICES = [
        ('Prescription', 'Prescription'),
        ('OTC', 'Over-the-Counter'),
        ('Supplements', 'Supplements'),
        ('Personal Care', 'Personal Care'),
        ('Equipment', 'Medical Equipment'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    prescription_required = models.BooleanField(default=False)
    image = models.ImageField(upload_to="medications/", blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.medication.price

class Payment(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)