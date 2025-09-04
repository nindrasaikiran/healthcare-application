# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#
# from . import views
# from .api.views import DoctorProfileView, PatientProfileView, BookAppointmentView
# from .views import RegisterUserView
#
# from .api import (
#     DoctorAppointmentsView,
#     PatientAppointmentsView,
#     DoctorViewSet,
#     PatientViewSet,
#     AppointmentViewSet,
# )
#
#
# app_name = 'appointments'
#
# router = DefaultRouter()
# router.register(r'doctors', DoctorViewSet, basename='doctor')
# router.register(r'patients', PatientViewSet, basename='patient')
# router.register(r'appointments', AppointmentViewSet, basename='appointment')
#
#
# urlpatterns = [
#     # Frontend views
#     path('', views.home, name='home'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('register/', views.register_view, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#
#     # API auth
#     # path('api/register/', RegisterUserView.as_view(), name='api_register'),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#
#     # Other frontend pages
#     path('services/', views.services, name='services'),
#     path('clients/', views.clients, name='clients'),
#     path('employees/', views.employees, name='employees'),
#
#     # Calendar and Profiles
#     path('calendar/', views.calendar_view, name='calendar'),
#     path('doctor/profile/', DoctorProfileView.as_view(), name='doctor_profile'),
#     path('patient/profile/', PatientProfileView.as_view(), name='patient_profile'),
#
#     # Appointment APIs handled by class-based views
#     path('api/appointment/book/', BookAppointmentView.as_view(), name='book_appointment'),
#     path('api/appointments/patient/', PatientAppointmentsView.as_view(), name='patient_appointments'),
#     path('api/appointments/doctor/', DoctorAppointmentsView.as_view(), name='doctor_appointments'),
#
#     # Include DRF router URLs for viewsets
#     path('api/', include(router.urls)),
# ]


from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views
from .api.views import DoctorProfileView, PatientProfileView, BookAppointmentView, DoctorAppointmentsView, PatientAppointmentsView
from .api.viewsets import DoctorViewSet, PatientViewSet, AppointmentViewSet
from .views import doctors_list_view
app_name = 'appointments'

# DRF router for ViewSets
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # Frontend pages
    path('', views.home, name='home'),

    # Authentication URLs


    path("login/", views.login_view, name="login"),
    path('register/', views.register_view, name='register'),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_dark, name="dashboard_dark"),

    # Dashboard pages
    path('services/', views.services, name='services'),
    path('clients/', views.client_list, name='client_list'),  # merged duplicate
    path('clients/add/', views.add_client, name='add_client'),
    path('employees/', views.employees, name='employees'),
    path('schedule/new/', views.schedule_appointment, name='schedule_appointment'),
    path('settings/', views.settings_view, name='settings_view'),

    # Doctor & Patient profiles
    path('doctors/list', views.doctors_list_view, name='doctor_list'),
    path('patients/list', views.patient_list_view, name='patient_list'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('messages/', views.messages_view, name='messages'),

    # Appointments
    path('appointments/list/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:pk>/', views.appointment_detail_view, name='appointment_detail'),
    path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointments/upcoming/', views.upcoming_appointments, name='upcoming_appointments'),

    # Calendar & Profiles
    path('calendar/', views.calendar_view, name='calendar'),
    path('doctor/profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient_profile'),

    # Appointment APIs
    path('api/appointment/book', BookAppointmentView.as_view(), name='book_appointment'),
    path('api/appointments/patient', PatientAppointmentsView.as_view(), name='patient_appointments'),
    path('api/appointments/doctor', DoctorAppointmentsView.as_view(), name='doctor_appointments'),
    path('messages/api/', views.messages_api, name='messages_api'),

    # JWT Auth
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # APIs the frontend uses
    path('api/stats/', views.stats_api, name='stats_api'),
    path('api/upcoming/', views.upcoming_api, name='upcoming_api'),
    path('api/events/', views.calendar_events_api, name='calendar_events_api'),
    path('api/update-status/', views.update_status_api, name='update_status_api'),
    path('api/search/', views.search_api, name='search_api'),

    # DRF Router endpoints
    path('api/', include(router.urls)),

    # ✅ Payment routes inside appointments
   #Hospital Packages Urls
    path('hospital/packages/list', views.hospital_packages_list, name='hospital_packages_list'),
    path('hospital/package/<slug:slug>/', views.hospital_packages_detail, name='hospital_packages_detail'),
    path('hospital/package/book/<slug:slug>/', views.book_package, name='book_package'),
    path('payment/handler/', views.payment_handler, name='payment_handler'),
    path("payment/success/<int:booking_id>/", views.payment_success, name="payment_success"),
    path("payment/failed/<int:booking_id>/", views.payment_failed, name="payment_failed"),

    #Lab Tests urls
    path("lab-tests/", views.lab_tests_list, name="lab_tests_list"),


    path("pharmacy/list", views.pharmacy_list, name="pharmacy_list"),
    path("add-to-cart/<int:medicine_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_page, name="cart_page"),
    path("buy-now/", views.buy_now, name="buy_now"),
    # path("medicines/", views.medicine_list, name="medicine_list"),
    path("pharmacy/checkout/", views.checkout, name="checkout"),
    path("pharmacy/payment-success/", views.payment_success, name="payment_success"),

    #Insurence Urls
    # path("insurance/", views.insurance,name="insurance")

    # path('payments/', views.payment_list, name='payment_list'),  # list of all payments
    # path('payments/checkout/<int:appointment_id>/', views.payment_checkout, name='payment_checkout'),  # checkout
    # path('payments/success/<int:payment_id>/', views.payment_success, name='payment_success'),  # success
    # path('payments/failure/<int:payment_id>/', views.payment_failure, name='payment_failure'),  # failure
]
