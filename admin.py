from django.contrib import admin
from .models import DoctorProfile, PatientProfile, Appointment
from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_full_name', 'specialization', 'phone')

    def doctor_full_name(self, obj):
        return obj.name or "No Name"
    doctor_full_name.short_description = 'Doctor Name'

@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_full_name', 'phone', 'date_of_birth')

    def patient_full_name(self, obj):
        return obj.name or "Unknown Patient"
    patient_full_name.short_description = 'Patient Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'patient_name', 'start_time', 'end_time', 'created_at')
    list_filter = ('start_time', 'end_time')
