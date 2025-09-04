#
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.contrib.auth import logout
# from django.shortcuts import redirect
# from .models import Appointment, PatientProfile, DoctorProfile, Service, Client, Employee
#
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
# @login_required
# # def calendar_view(request):
# #     appointments = Appointment.objects.all()
# #     context = {
# #         "appointments": appointments
# #     }
# #     return render(request, "appointments/calendar.html", context)
#
# def calendar_view(request):
#     return render(request, 'appointments/calendar.html')
#
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         phone_number = request.POST.get('phone_number')
#         role = request.POST.get('role')
#
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect('appointments:register')
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('appointments:register')
#
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered")
#             return redirect('appointments:register')
#
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )
#
#         # Save extra fields if exist on your user model
#         user.phone_number = phone_number
#         user.role = role
#         user.save()
#
#         messages.success(request, "Registration successful! Please log in.")
#         return redirect('appointments:login')
#
#     return render(request, 'appointments/register.html')
#
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('appointments:dashboard')  # or home page
#         else:
#             return render(request, 'appointments/login.html', {"error": "Invalid credentials"})
#     return render(request, 'appointments/login.html')
#
# def home(request):
#     return HttpResponse("Welcome to the Appointments App!")
#
#
# @login_required
# def dashboard_view(request):
#     user = request.user
#
#     # Sample statistics you can customize based on your models
#     total_patients = PatientProfile.objects.count()
#     total_doctors = DoctorProfile.objects.count()
#     total_appointments = Appointment.objects.count()
#     upcoming_appointments = Appointment.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:5]
#     # Data for charts (mock or real data)
#     appointments_per_month = [5, 7, 10, 15, 12, 9]  # Example for last 6 months
#     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
#
#     context = {
#         'total_patients': total_patients,
#         'total_doctors': total_doctors,
#         'total_appointments': total_appointments,
#         'upcoming_appointments': upcoming_appointments,
#         'appointments_per_month': appointments_per_month,
#         'months': months,
#     }
#     return render(request, 'appointments/dashboard.html', context)
#
# @login_required()
# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('login')  # Redirect to login page after logout
#     else:
#         # If someone accesses logout page via GET, you can redirect or handle differently
#         return redirect('dashboard')  # or any other page
#
# @login_required
# def services(request):
#     services_list = Service.objects.all()
#     return render(request, 'appointments/services.html', {'services': services_list})
#
# @login_required
# def clients(request):
#     clients_list = Client.objects.all().order_by('-joined_date')
#     return render(request, 'appointments/clients.html', {'clients': clients_list})
#
# @login_required
# def employees(request):
#     employees_list = Employee.objects.all().order_by('last_name', 'first_name')
#     return render(request, 'appointments/employees.html', {'employees': employees_list})
#
# # appointments/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# class RegisterUserView(APIView):
#     def post(self, request):
#         # Example logic (replace with real registration)
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # You’d normally create the user here
#         return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
import json
from datetime import datetime

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt

from .models import Client, HospitalMessage, HospitalPackage, PackageBooking, Medication, CartItem, Payment
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Appointment

from .models import Appointment, PatientProfile, DoctorProfile, Service, Client, Employee


User = get_user_model()

def home(request):
    return HttpResponse("Welcome to the Appointments App!")

# @login_required
# def dashboard_view(request):
#     total_patients = PatientProfile.objects.count()
#     total_doctors = DoctorProfile.objects.count()
#     total_appointments = Appointment.objects.count()
#
#     context = {
#         'total_patients': total_patients,
#         'total_doctors': total_doctors,
#         'total_appointments': total_appointments,
#         'upcoming_appointments': Appointment.objects.filter(
#             start_time__gte=timezone.now()
#         ).order_by('start_time')[:5],
#         'appointments_per_month': [5, 7, 10, 15, 12, 9],
#         'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
#     }
#
#     # # Add popup messages
#     # messages.info(request, f"Total Patients: {total_patients}")
#     # messages.info(request, f"Total Doctors: {total_doctors}")
#     # messages.info(request, f"Total Appointments: {total_appointments}")
#
#     return render(request, 'appointments/dashboard.html', context)
#
# def dashboard_view(request):
#     """
#     Renders the dashboard page with summary data and a list of upcoming appointments.
#     """
#     # Get the current time, making it timezone-aware
#     now = timezone.now()
#
#     # Query the database for appointments where start_time is greater than or equal to now
#     upcoming_appointments = Appointment.objects.filter(start_time__gte=now).order_by('start_time')
#
#     # Get the counts for your dashboard cards
#     total_patients = PatientProfile.objects.count()
#     total_doctors = DoctorProfile.objects.count()
#     total_appointments = Appointment.objects.count()
#
#     context = {
#         'total_patients': total_patients,
#         'total_doctors': total_doctors,
#         'total_appointments': total_appointments,
#         'upcoming_appointments': upcoming_appointments,  # Pass the upcoming appointments to the template
#     }
#     return render(request, 'appointments/dashboard.html', context)
#

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('appointments:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('appointments:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('appointments:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.phone_number = phone_number
        user.role = role
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('appointments:login')

    return render(request, 'appointments/register.html')
#
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('appointments:dashboard')
#
#     next_url = request.GET.get('next')
#     if next_url == 'None':
#         next_url = None  # Convert string 'None' to None
#
#     if request.method == 'POST':
#         # When POST, get next from POST data, also clean if it equals 'None'
#         next_url = request.POST.get('next')
#         if next_url == 'None':
#             next_url = None
#
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user:
#             login(request, user)
#             if next_url:
#                 return redirect(next_url)
#             else:
#                 return redirect('appointments:dashboard')
#         else:
#             messages.error(request, "Invalid username or password")
#
#     return render(request, 'appointments/login.html', {'next': next_url or ''})
#
# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('appointments:login')

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    # If already logged in, go straight to dashboard
    if request.user.is_authenticated:
        return redirect('appointments:dashboard_dark')

    # Handle "next" parameter (if user was redirected here)
    next_url = request.GET.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(next_url or 'appointments:dashboard_dark')  # go where they wanted, or dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'appointments/login.html', {'next': next_url or ''})


@login_required
def logout_view(request):
    logout(request)
    return redirect('appointments:login')


# Optional: Keep your STATUS dicts here or import them
STATUS_LABELS = {
    "pending": "Pending",
    "confirmed": "Confirmed",
    "completed": "Completed",
    "cancelled": "Cancelled",
}
STATUS_COLORS = {
    "pending": "orange",
    "confirmed": "green",
    "completed": "blue",
    "cancelled": "red",
}
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_dark(request):
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()

    upcoming = Appointment.objects.filter(
        start_time__gte=timezone.now()
    ).order_by("start_time")[:8]

    for a in upcoming:
        a.status_label = STATUS_LABELS.get(a.status, a.status)
        a.status_color = STATUS_COLORS.get(a.status, "gray")

    return render(request, "appointments/dashboard_dark.html", {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "upcoming": upcoming,
    })

@login_required
def calendar_view(request):
    return render(request, 'appointments/calendar.html')

@login_required
def services(request):
    return render(request, 'appointments/services.html', {'services': Service.objects.all()})

@login_required
def clients(request):
    return render(request, 'appointments/clients.html', {'clients': Client.objects.all().order_by('-joined_date')})

@login_required
def employees(request):
    return render(request, 'appointments/employees.html', {'employees': Employee.objects.all().order_by('last_name', 'first_name')})


def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Insert into database
        Client.objects.create(name=name, email=email, phone=phone)

        # Count total clients
        total_clients = Client.objects.count()

        # Show popup message
        messages.success(request, f"Client added successfully! Total Clients: {total_clients}")

        return redirect('client_list')

    return render(request, "add_client.html")

@login_required()
def client_list(request):
    clients = Client.objects.all()
    return render(request, "client_list.html", {"clients": clients})

from django.shortcuts import render
from .models import DoctorProfile  # or your doctor model

#doctor profile views
def doctors_list_view(request):
    doctors = DoctorProfile.objects.all()
    context = {
        'doctors': doctors,
    }
    return render(request, 'appointments/doctor_list.html', context)

#patient profile views

def patient_list_view(request):
    patients = PatientProfile.objects.all()
    context = {
        'patients': patients,
    }
    return render(request, 'appointments/patient_list.html', context)

def doctor_detail(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    context = {
        'doctor': doctor
    }
    return render(request, 'appointments/doctor_detail.html', context)


def patient_detail(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)
    context = {
        'patient': patient
    }
    return render(request, 'appointments/patient_detail.html', context)

# Map query params (string) to DB values (integer)
STATUS_MAP = {
    "requested": Appointment.STATUS_REQUESTED,
    "confirmed": Appointment.STATUS_CONFIRMED,
    "completed": Appointment.STATUS_COMPLETED,
    "cancelled": Appointment.STATUS_CANCELLED
}

def appointments_list(request):
    status_param = request.GET.get("status")  # e.g. ?status=pending
    appointments = Appointment.objects.all()

    # Apply filter only if status param is valid
    if status_param and status_param.lower() in STATUS_MAP:
        appointments = appointments.filter(status=STATUS_MAP[status_param.lower()])

    return render(request, "appointments/appointments_list.html", {
        "appointments": appointments
    })

def appointment_detail_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {
        'appointment': appointment
    }
    return render(request, 'appointments/appointment_detail.html', context)

#
# def schedule_view(request):
#     """
#     Renders a list of all appointments for the schedule page.
#     """
#     appointments = Appointment.objects.all().order_by('start_time')
#     context = {
#         'appointments': appointments
#     }
#     return render(request, 'appointments/schedule_appointment.html', context)

def settings_view(request):
    """
    Renders a placeholder settings page with sample data.
    """
    settings_data = {
        'theme': 'light',
        'notifications_enabled': True,
        'language': 'en-us'
    }
    context = {
        'settings_data': settings_data
    }
    return render(request, 'appointments/settings.html', context)
#
# @login_required()
# def schedule_appointment(request):
#     # This view function remains the same as our previous versions
#     if request.method == 'POST':
#         doctor_name = request.POST.get('doctor_name')
#         patient_name = request.POST.get('patient_name')
#         appointment_date_str = request.POST.get('appointment_date')
#         start_time_str = request.POST.get('start_time')
#
#         if not all([doctor_name, patient_name, appointment_date_str, start_time_str]):
#             doctors = DoctorProfile.objects.all()
#             patients = PatientProfile.objects.all()
#             context = {
#                 'doctors': doctors,
#                 'patients': patients,
#                 'error_message': 'All fields are required.'
#             }
#             return render(request, 'appointments/schedule_appointment.html', context)
#
#         try:
#             combined_datetime_str = f"{appointment_date_str} {start_time_str}"
#             naive_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M')
#             start_datetime = timezone.make_aware(naive_datetime)
#
#             Appointment.objects.create(
#                 doctor_name=doctor_name,
#                 patient_name=patient_name,
#                 start_time=start_datetime
#             )
#             messages.success(request, "Appointment scheduled successfully.")
#             return redirect('appointments:total_appointments')
#
#         except Exception as e:
#             doctors = DoctorProfile.objects.all()
#             patients = PatientProfile.objects.all()
#             context = {
#                 'doctors': doctors,
#                 'patients': patients,
#                 'error_message': f"An unexpected error occurred: {e}"
#             }
#             return render(request, 'appointments/schedule_appointment.html', context)
#     else:
#         doctors = DoctorProfile.objects.all()
#         patients = PatientProfile.objects.all()
#         context = {
#             'doctors': doctors,
#             'patients': patients,
#         }
#         return render(request, 'appointments/schedule_appointment.html', context)

def schedule_appointment(request):
    # Optional: load lists for your select dropdowns (replace with your real models if available)
    try:
        from .models import DoctorProfile, PatientProfile
        doctors = DoctorProfile.objects.all()
        patients = PatientProfile.objects.all()
    except Exception:
        doctors = []
        patients = []

    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name", "").strip()
        patient_name = request.POST.get("patient_name", "").strip()
        date_str = request.POST.get("appointment_date")   # expects YYYY-MM-DD
        time_str = request.POST.get("start_time")         # expects HH:MM (24h)

        # Basic validation
        if not (doctor_name and patient_name and date_str and time_str):
            messages.error(request, "Please fill all fields.")
            # fall through to render page with existing upcoming appointments

        else:
            # Combine date + time into timezone-aware datetime
            start_dt = None
            try:
                naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                start_dt = timezone.make_aware(naive, timezone.get_current_timezone())
            except Exception:
                start_dt = None

            Appointment.objects.create(
                doctor_name=doctor_name,
                patient_name=patient_name,
                start_time=start_dt,
                status=1  # mark as Scheduled Appointment
            )

            messages.success(request, f"Appointment booked successfully for {patient_name} with {doctor_name}.")
            return redirect("appointments:schedule_appointment")

    # GET and fallback after POST error: show upcoming appointments
    now = timezone.now()
    upcoming = Appointment.objects.filter(start_time__gte=now).order_by("start_time")
    # If you want to include records with null start_time, use Appointment.objects.all()

    context = {
        "doctors": doctors,
        "patients": patients,
        "appointments": upcoming,
    }
    return render(request, "appointments/schedule_appointment.html", context)


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        # Get data from the form
        new_doctor_name = request.POST.get('doctor_name')
        new_patient_name = request.POST.get('patient_name')
        new_date_str = request.POST.get('appointment_date')
        new_time_str = request.POST.get('start_time')

        # Make the datetime timezone-aware
        combined_datetime_str = f"{new_date_str} {new_time_str}"
        naive_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M')
        new_start_time = timezone.make_aware(naive_datetime)

        # Update the appointment fields
        appointment.doctor_name = new_doctor_name
        appointment.patient_name = new_patient_name
        appointment.start_time = new_start_time
        appointment.status = int(request.POST.get("status"))
        appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('appointments:appointments_list')

    else:
        # For a GET request, pre-populate the form with current data
        doctors = DoctorProfile.objects.all()
        patients = PatientProfile.objects.all()

        context = {
            'appointment': appointment,
            'doctors': doctors,
            'patients': patients,
        }
        return render(request, 'appointments/edit_appointment.html', context)




def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect('appointments:appointments_list')

    # Optional: Render a confirmation page on GET request
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})

def upcoming_appointments(request):
    appointments = Appointment.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'upcoming_appointments.html', {'appointments': appointments})

#
# def dashboard_dark(request):
#     # quick numbers for the stat cards
#     total_appointments = Appointment.objects.count()
#     total_doctors = Appointment.objects.values("doctor_name").distinct().count()
#     total_patients = Appointment.objects.values("patient_name").distinct().count()
#
#     # few upcoming rows for the table (ajax can refresh)
#     now = timezone.now()
#     upcoming = (Appointment.objects
#                 .filter(start_time__gte=now)
#                 .order_by("start_time")[:5])
#
#     return render(request, "appointments/dashboard_dark.html", {
#         "total_patients": total_patients,
#         "total_doctors": total_doctors,
#         "total_appointments": total_appointments,
#         "upcoming": upcoming,
#     })


# from django.shortcuts import render
# from django.utils import timezone
# from .models import PatientProfile, DoctorProfile, Appointment
# from .constants import STATUS_LABELS, STATUS_COLORS  # adjust import as needed
#
# def dashboard_dark(request):
#     total_patients = PatientProfile.objects.count()
#     total_doctors = DoctorProfile.objects.count()
#     total_appointments = Appointment.objects.count()
#
#     upcoming = Appointment.objects.filter(
#         start_time__gte=timezone.now()
#     ).order_by('start_time')[:8]
#
#     # Add precomputed values to each appointment
#     for a in upcoming:
#         a.status_label = STATUS_LABELS.get(a.status, a.status)
#         a.status_color = STATUS_COLORS.get(a.status, 'gray')
#
#     return render(request, "appointments/dashboard_dark.html", {
#         "total_patients": total_patients,
#         "total_doctors": total_doctors,
#         "total_appointments": total_appointments,
#         "upcoming": upcoming,
#     })


def stats_api(request):
    """Return JSON for donut & monthly chart."""
    now = timezone.now()
    # monthly counts (last 8 months)
    start = (now - timedelta(days=30*7)).replace(day=1)
    qs = Appointment.objects.filter(start_time__isnull=False, start_time__gte=start)
    months = (qs.annotate(m=TruncMonth('start_time')).values('m').annotate(c=Count('id')).order_by('m'))
    monthly = [{"label": m["m"].strftime("%Y-%m"), "value": m["c"]} for m in months]

    # status breakdown
    status_qs = qs.values('status').annotate(c=Count('id'))
    status_breakdown = []
    for s,v in STATUS_LABELS.items():
        rec = next((x for x in status_qs if x['status']==s), None)
        status_breakdown.append({"status": s, "label": v, "value": rec['c'] if rec else 0})

    return JsonResponse({"appointments_per_month": monthly, "status_breakdown": status_breakdown})


def calendar_events_api(request):
    """Return events for FullCalendar."""
    evs = []
    for a in Appointment.objects.exclude(start_time__isnull=True):
        evs.append({
            "id": a.id,
            "title": f"{a.patient_name} — {STATUS_LABELS.get(a.status,'')}",
            "start": a.start_time.isoformat(),
            "end": (a.end_time.isoformat() if a.end_time else (a.start_time + timedelta(minutes=30)).isoformat()),
            "status": a.status,
            # color choices (customize)
            "color": "#3b82f6" if a.status==1 else ("#10b981" if a.status==2 else ("#f59f00" if a.status==0 else "#ef4444"))
        })
    return JsonResponse(evs, safe=False)


def upcoming_api(request):
    now = timezone.now()
    items = Appointment.objects.filter(start_time__gte=now).order_by('start_time')[:20]
    data = []
    for it in items:
        data.append({
            "id": it.id,
            "patient": it.patient_name,
            "doctor": it.doctor_name,
            "start": timezone.localtime(it.start_time).strftime("%b %d, %Y, %I:%M %p"),
            "status": it.status,
            "status_label": STATUS_LABELS.get(it.status)
        })
    return JsonResponse(data, safe=False)


def update_status_api(request):
    """AJAX endpoint to update appointment status. Expects JSON {id, status}."""
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Authentication required")
    try:
        data = json.loads(request.body.decode())
        appointment_id = int(data.get("id"))
        new_status = int(data.get("status"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    appointment = get_object_or_404(Appointment, id=appointment_id)
    if new_status not in STATUS_LABELS:
        return HttpResponseBadRequest("Invalid status")
    appointment.status = new_status
    appointment.save()
    return JsonResponse({"ok": True, "status_label": STATUS_LABELS[new_status]})


def search_api(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)
    qs = Appointment.objects.filter(patient_name__icontains=q)[:20]
    results = []
    for a in qs:
        results.append({
            "id": a.id,
            "title": f"{a.patient_name} — {a.doctor_name}",
            "start": a.start_time.isoformat() if a.start_time else None,
            "status": a.status,
        })
    return JsonResponse(results, safe=False)



# from datetime import timedelta
# from django.db.models import Count
# from django.shortcuts import render
# from django.utils import timezone
#
# from .models import (
#     DoctorProfile, PatientProfile, Appointment
# )
#
# # ----- helpers -----
# STATUS_LABELS = {
#     0: "Requested",
#     1: "Scheduled Appointment",
#     2: "Completed",
#     3: "Cancelled",
# }
# STATUS_COLORS = {   # for badges
#     0: "badge-yellow",
#     1: "badge-blue",
#     2: "badge-green",
#     3: "badge-red",
# }
#
# def _dashboard_context():
#     now = timezone.now()
#
#     total_patients = PatientProfile.objects.count()
#     total_doctors = DoctorProfile.objects.count()
#     total_appointments = Appointment.objects.count()
#
#     # Upcoming (next 10)
#     upcoming = (
#         Appointment.objects
#         .filter(start_time__gte=now)
#         .order_by('start_time')[:10]
#     )
#
#     # Line chart: appointments per day for last 14 days
#     start_14 = (now - timedelta(days=13)).date()
#     per_day_qs = (
#         Appointment.objects
#         .filter(start_time__date__gte=start_14, start_time__date__lte=now.date())
#         .extra(select={'day': "date(start_time)"})
#         .values('day')
#         .annotate(cnt=Count('id'))
#         .order_by('day')
#     )
#     # Normalize to a 14-day series
#     day_labels = []
#     day_counts = []
#     for i in range(14):
#         d = (start_14 + timedelta(days=i))
#         day_labels.append(d.strftime("%a"))  # Mon, Tue...
#         rec = next((x for x in per_day_qs if str(x['day']) == str(d)), None)
#         day_counts.append(rec['cnt'] if rec else 0)
#
#     # Donut: map statuses to slices
#     status_counts_qs = (
#         Appointment.objects
#         .values('status')
#         .annotate(cnt=Count('id'))
#     )
#     donut_labels = [STATUS_LABELS[s] for s in range(0, 4)]
#     donut_counts = []
#     for s in range(0, 4):
#         rec = next((x for x in status_counts_qs if x['status'] == s), None)
#         donut_counts.append(rec['cnt'] if rec else 0)
#
#     # Calendar events (FullCalendar-style)
#     events = []
#     for a in upcoming:
#         events.append({
#             "title": f"{a.patient_name} • {STATUS_LABELS.get(a.status, '')}",
#             "start": a.start_time.isoformat(),
#         })
#
#     return {
#         "total_patients": total_patients,
#         "total_doctors": total_doctors,
#         "total_appointments": total_appointments,
#         "upcoming": upcoming,
#         "STATUS_LABELS": STATUS_LABELS,
#         "STATUS_COLORS": STATUS_COLORS,
#         # charts
#         "line_labels": day_labels,      # ['Mon','Tue',...]
#         "line_values": day_counts,      # [5,7,0,...]
#         "donut_labels": donut_labels,   # ['Requested','Scheduled Appointment',...]
#         "donut_values": donut_counts,   # [x,x,x,x]
#         # calendar
#         "calendar_events": events,
#     }

# # ----- views -----
# def dashboard_dark(request):
#     ctx = _dashboard_context()
#     return render(request, "appointments/dashboard_dark.html", ctx)
#
# def dashboard_light(request):
#     ctx = _dashboard_context()
#     return render(request, "appointments/dashboard_light.html", ctx)




def messages_view(request):
    messages = HospitalMessage.objects.order_by('-created_at')
    return render(request, 'appointments/messages.html', {'messages': messages})

def messages_api(request):
    """Return latest unread messages as JSON (for AJAX polling)."""
    messages = HospitalMessage.objects.filter(is_read=False).order_by('-created_at')
    data = [
        {
            'id': msg.id,
            'title': msg.title,
            'message': msg.message,
            'category': msg.category,
            'created_at': msg.created_at.strftime("%b %d, %Y %H:%M"),
        }
        for msg in messages
    ]
    return JsonResponse({'messages': data, 'count': messages.count()})

# List all packages
def hospital_packages_list(request):
    packages = HospitalPackage.objects.all()
    return render(request, 'hospital_packages/list.html', {'packages': packages})

# View single package details
def hospital_packages_detail(request, slug):
    package = get_object_or_404(HospitalPackage, slug=slug)
    services = package.services_included.split(',')
    return render(request, 'hospital_packages/detail.html', {'package': package})



@login_required
def book_package(request, slug):
    package = get_object_or_404(HospitalPackage, slug=slug)

    # Fail fast if keys missing
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return render(request, "appointments/payment_error.html",
                      {"error": "Razorpay keys are not configured."})

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount_paise = int(package.price * 100)   # Razorpay needs paise
    order_currency = "INR"
    receipt = f"pkg_{package.id}_user_{request.user.id}"

    try:
        order = client.order.create({
            "amount": amount_paise,
            "currency": order_currency,
            "receipt": receipt,
            "payment_capture": 1,   # auto-capture
        })
    except Exception as e:
        # Authentication errors show up here
        return render(request, "hospital_packages/payment_error.html", {"error": str(e)})

    # Persist booking with Razorpay ORDER id
    booking = PackageBooking.objects.create(
        user=request.user,
        package=package,
        payment_id=order["id"],     # store the ORDER id
        amount=package.price,
        status="Pending"
    )

    context = {
        "package": package,
        "booking": booking,
        "razorpay_order_id": order["id"],
        "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        "amount": amount_paise,
        "display_amount": f"{package.price:.2f}",
        "currency": order_currency,
        "callback_url": request.build_absolute_uri(reverse("appointments:payment_handler")),
    }
    return render(request, "hospital_packages/package_payment.html", context)

@csrf_exempt   # Razorpay posts to this URL
def payment_handler(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    params = {
        "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
        "razorpay_order_id": request.POST.get("razorpay_order_id"),
        "razorpay_signature": request.POST.get("razorpay_signature"),
    }
    if not all(params.values()):
        return HttpResponseBadRequest("Missing payment parameters.")

    # Find our booking by order id
    try:
        booking = PackageBooking.objects.select_related("package", "user").get(payment_id=params["razorpay_order_id"])
    except PackageBooking.DoesNotExist:
        return HttpResponseBadRequest("Unknown order.")

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        client.utility.verify_payment_signature(params)
        # If we reach here, signature is valid and payment is captured (payment_capture=1)
        booking.status = "Paid"
        booking.razorpay_payment_id = params["razorpay_payment_id"]
        booking.razorpay_signature = params["razorpay_signature"]
        booking.save()
        return redirect("appointments:payment_success", booking_id=booking.id)
    except razorpay.errors.SignatureVerificationError as e:
        booking.status = "Failed"
        booking.save()
        return redirect("appointments:payment_failed", booking_id=booking.id)
    except Exception as e:
        booking.status = "Failed"
        booking.save()
        return redirect("appointments:payment_failed", booking_id=booking.id)

def payment_success(request, booking_id):
    booking = get_object_or_404(PackageBooking, id=booking_id)
    return render(request, "hospital_packages/payment_success.html", {"booking": booking})

def payment_failed(request, booking_id):
    booking = get_object_or_404(PackageBooking, id=booking_id)
    return render(request, "hospital_packages/payment_failed.html", {"booking": booking})


















def lab_tests_list(request):
    # later you can fetch LabTest objects from DB
    lab_tests = [
        {"name": "Blood Test", "description": "Complete blood count, glucose, cholesterol"},
        {"name": "Urine Test", "description": "Check kidney and urinary tract health"},
        {"name": "ECG", "description": "Heart activity test"},
    ]
    return render(request, "lab_tests/list.html", {"lab_tests": lab_tests})


# appointments/views.py



def pharmacy_list(request):
    category = request.GET.get('category')
    if category:
        medications = Medication.objects.filter(category=category)
    else:
        medications = Medication.objects.all()
    categories = Medication.CATEGORY_CHOICES
    return render(request, "pharmacy/list.html", {"medications": medications, "categories": categories})



cart = []  # For simplicity (you can store in session or DB)

def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medication, id=medicine_id)

    cart = request.session.get("cart", {})

    if str(medicine_id) in cart:
        cart[str(medicine_id)]["quantity"] += 1
    else:
        cart[str(medicine_id)] = {
            "name": medicine.name,
            "price": float(medicine.price),
            "quantity": 1,
        }

    request.session["cart"] = cart
    request.session.modified = True  # ✅ very important

    return redirect("appointments:cart_page")

def cart_page(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render(request, "pharmacy/cart_page.html", {"cart": cart, "total": total})

def buy_now(request):
    total = sum(m.price for m in cart) * 100  # Razorpay needs paisa

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": total,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "pharmacy/payment.html", {
        "order_id": order["id"],
        "amount": total,
        "key": settings.RAZORPAY_KEY_ID,
    })

def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.subtotal() for item in items) * 100  # Razorpay works in paise
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        "amount": int(total_amount),
        "currency": "INR",
        "payment_capture": "1"
    })
    return render(request, "pharmacy/checkout.html", {"items": items, "payment": payment})



#
# @login_required
# def book_package(request, slug):
#     package = get_object_or_404(HospitalPackage, slug=slug)
#
#     # Initialize Razorpay client
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#
#     # Razorpay requires amount in paise (multiply by 100)
#     order_amount = int(package.price * 100)
#     order_currency = 'INR'
#     order_receipt = f'order_rcptid_{package.id}_{request.user.id}'
#
#     try:
#         razorpay_order = client.order.create({
#             "amount": order_amount,
#             "currency": order_currency,
#             "receipt": order_receipt,
#             "payment_capture": 1  # Auto-capture
#         })
#     except Exception as e:
#         # If authentication or order creation fails, handle gracefully
#         return render(request, "hospital_packages/payment_error.html", {"error": str(e)})
#
#     # Save booking with Razorpay order ID
#     booking = PackageBooking.objects.create(
#         user=request.user,
#         package=package,
#         payment_id=razorpay_order["id"],  # store Razorpay order ID
#         status="Pending"
#     )
#
#     context = {
#         "package": package,
#         "booking": booking,
#         "razorpay_order_id": razorpay_order["id"],
#         "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
#         "amount": order_amount,
#         "currency": order_currency,
#         "callback_url": "/appointments/payment/handler/",  # ✅ better to use reverse()
#     }
#     return render(request, "appointments/package_payment.html", context)
#
# @csrf_exempt
# def payment_handler(request):
#     if request.method == "POST":
#         payment_id = request.POST.get('razorpay_payment_id', '')
#         razorpay_order_id = request.POST.get('razorpay_order_id', '')
#         signature = request.POST.get('razorpay_signature', '')
#
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }
#
#         try:
#             # Verify the payment signature - ensures payment is legitimate
#             client.utility.verify_payment_signature(params_dict)
#
#             # Find the booking by razorpay_order_id and update status
#             booking = PackageBooking.objects.get(payment_id=razorpay_order_id)
#             booking.payment_id = payment_id
#             booking.status = 'Successful'
#             booking.save()
#
#             return render(request, 'appointments/payment_success.html', {'booking': booking})
#         except razorpay.errors.SignatureVerificationError:
#             # Handle failed payment signature verification
#             booking = PackageBooking.objects.get(payment_id=razorpay_order_id)
#             booking.status = 'Failed'
#             booking.save()
#             return render(request, 'appointments/payment_failure.html', {'booking': booking})
#     else:
#         return HttpResponseBadRequest()



# @csrf_exempt
# def payment_success(request):
#     data = json.loads(request.body)
#     try:
#         payment = Payment.objects.get(order_id=data['order_id'])
#         payment.payment_id = data['payment_id']
#         payment.status = "success"
#         payment.save()
#
#         # Reduce stock and clear cart
#         cart_items = CartItem.objects.filter(user=payment.user)
#         for item in cart_items:
#             med = item.medication
#             med.stock -= item.quantity
#             med.save()
#         cart_items.delete()
#         return JsonResponse({"success": True, "message": "Payment successful! Stock updated."})
#     except Exception as e:
#         return JsonResponse({"success": False, "message": str(e)})

#
# def _client():
#     return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#
# @login_required
# def payment_history(request):
#     payments = Payment.objects.filter(user=request.user).order_by("-payment_date")
#     return render(request, "payments/history.html", {"payments": payments})
#
# @login_required
# def payment_detail(request, pk):
#     payment = get_object_or_404(Payment, pk=pk, user=request.user)
#     return render(request, "payments/detail.html", {"payment": payment})
#
# @login_required
# def checkout(request, appointment_id):
#     """
#     Amazon-like summary page for one appointment.
#     The real amount should come from your appointment object or pricing rules.
#     For demo, we can pass ?amount=500 or compute from appointment.
#     """
#     from appointments.models import Appointment
#     appt = get_object_or_404(Appointment, pk=appointment_id)
#     amount = request.GET.get("amount")
#     try:
#         amount = decimal.Decimal(amount) if amount else decimal.Decimal("500.00")
#     except Exception:
#         amount = decimal.Decimal("500.00")
#
#     return render(request, "payments/checkout.html", {
#         "appointment": appt,
#         "amount": amount,
#         "currency": getattr(settings, "PAYMENTS_CURRENCY", "INR"),
#         "razorpay_key_id": settings.RAZORPAY_KEY_ID,
#         "site_name": getattr(settings, "SITE_NAME", "MedCare"),
#     })
#
# @login_required
# def create_order(request):
#     """
#     Create Razorpay Order for ONLINE methods (upi/card/netbanking/wallet).
#     """
#     if request.method != "POST":
#         return HttpResponseBadRequest("POST only")
#
#     appointment_id = request.POST.get("appointment_id")
#     amount = decimal.Decimal(request.POST.get("amount"))
#     currency = getattr(settings, "PAYMENTS_CURRENCY", "INR")
#     method = request.POST.get("payment_method", "upi")  # could be upi/card/netbanking/wallet
#
#     # Create DB record (status=created)
#     payment = Payment.objects.create(
#         user=request.user,
#         appointment_id=appointment_id,
#         amount=amount,
#         currency=currency,
#         payment_method=method,
#         status="created",
#         patient_name=request.POST.get("patient_name") or None,
#         patient_email=request.POST.get("patient_email") or None,
#         patient_phone=request.POST.get("patient_phone") or None,
#         billing_address=request.POST.get("billing_address") or None,
#         notes=request.POST.get("notes") or None,
#     )
#
#     # Create Razorpay order (amount in paise)
#     client = _client()
#     order = client.order.create({
#         "amount": int(amount * 100),
#         "currency": currency,
#         "payment_capture": 1,
#         "notes": {
#             "appointment_id": str(appointment_id),
#             "payment_pk": str(payment.pk),
#         },
#     })
#
#     payment.order_id = order["id"]
#     payment.gateway_name = "Razorpay"
#     payment.gateway_response = order
#     payment.save()
#
#     return JsonResponse({
#         "ok": True,
#         "payment_pk": payment.pk,
#         "order_id": order["id"],
#         "key_id": settings.RAZORPAY_KEY_ID,
#         "amount_paise": int(amount * 100),
#         "currency": currency,
#     })
#
# @csrf_exempt
# @login_required
# def verify_payment(request):
#     """
#     Called from frontend handler after successful Razorpay popup.
#     """
#     if request.method != "POST":
#         return HttpResponseBadRequest("POST only")
#
#     payment_pk = request.POST.get("payment_pk")
#     r_order_id = request.POST.get("razorpay_order_id")
#     r_payment_id = request.POST.get("razorpay_payment_id")
#     r_signature = request.POST.get("razorpay_signature")
#
#     payment = get_object_or_404(Payment, pk=payment_pk, user=request.user)
#     client = _client()
#
#     params_dict = {
#         "razorpay_order_id": r_order_id,
#         "razorpay_payment_id": r_payment_id,
#         "razorpay_signature": r_signature,
#     }
#
#     try:
#         client.utility.verify_payment_signature(params_dict)
#         payment.status = "success"
#     except razorpay.errors.SignatureVerificationError:
#         payment.status = "failed"
#
#     payment.transaction_id = r_payment_id
#     # Keep signature & params in gateway_response for audit/debug
#     existing = payment.gateway_response or {}
#     existing["verify"] = params_dict
#     payment.gateway_response = existing
#     payment.save()
#
#     if payment.status == "success":
#         return JsonResponse({"ok": True, "redirect": redirect("payments:success", pk=payment.pk).url})
#     return JsonResponse({"ok": False, "redirect": redirect("payments:failed", pk=payment.pk).url})
#
# @login_required
# def process_cash_payment(request):
#     """
#     For 'cash' method: directly create Payment without Razorpay.
#     You can choose to mark as 'pending' (to be settled at front desk) or 'success'.
#     """
#     if request.method != "POST":
#         return HttpResponseBadRequest("POST only")
#
#     appointment_id = request.POST.get("appointment_id")
#     amount = decimal.Decimal(request.POST.get("amount"))
#     currency = getattr(settings, "PAYMENTS_CURRENCY", "INR")
#
#     payment = Payment.objects.create(
#         user=request.user,
#         appointment_id=appointment_id,
#         amount=amount,
#         currency=currency,
#         payment_method="cash",
#         status="pending",  # or "success" if you collect immediately
#         patient_name=request.POST.get("patient_name") or None,
#         patient_email=request.POST.get("patient_email") or None,
#         patient_phone=request.POST.get("patient_phone") or None,
#         billing_address=request.POST.get("billing_address") or None,
#         notes=request.POST.get("notes") or "Cash at hospital",
#     )
#     return JsonResponse({"ok": True, "redirect": redirect("payments:detail", pk=payment.pk).url})
#
# @login_required
# def process_insurance_payment(request):
#     """
#     For 'insurance' method: store claim info and mark as 'pending'.
#     """
#     if request.method != "POST":
#         return HttpResponseBadRequest("POST only")
#
#     appointment_id = request.POST.get("appointment_id")
#     amount = decimal.Decimal(request.POST.get("amount"))
#     currency = getattr(settings, "PAYMENTS_CURRENCY", "INR")
#
#     payment = Payment.objects.create(
#         user=request.user,
#         appointment_id=appointment_id,
#         amount=amount,
#         currency=currency,
#         payment_method="insurance",
#         status="pending",
#         patient_name=request.POST.get("patient_name") or None,
#         patient_email=request.POST.get("patient_email") or None,
#         patient_phone=request.POST.get("patient_phone") or None,
#         billing_address=request.POST.get("billing_address") or None,
#         insurance_provider=request.POST.get("insurance_provider") or None,
#         insurance_claim_id=request.POST.get("insurance_claim_id") or None,
#         covered_amount=request.POST.get("covered_amount") or 0,
#         patient_payable=request.POST.get("patient_payable") or 0,
#         notes=request.POST.get("notes") or "Insurance claim initiated",
#     )
#     return JsonResponse({"ok": True, "redirect": redirect("payments:detail", pk=payment.pk).url})
#
# @login_required
# def payment_success(request, pk):
#     payment = get_object_or_404(Payment, pk=pk, user=request.user)
#     return render(request, "payments/success.html", {"payment": payment})
#
# @login_required
# def payment_failed(request, pk):
#     payment = get_object_or_404(Payment, pk=pk, user=request.user)
#     return render(request, "payments/failed.html", {"payment": payment})
