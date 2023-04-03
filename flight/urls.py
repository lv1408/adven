from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("query/places/<str:q>", views.query, name="query"),
    path("adven", views.booking, name="flight"),
    path("review", views.review, name="review"),
    path("adven/ticket/book", views.book, name="book"),
    path("adven/ticket/payment", views.payment, name="payment"),
    path('flight/ticket/api/<str:ref>', views.ticket_data, name="ticketdata"),
    path('adven/ticket/print',views.get_ticket, name="getticket"),
    path('adven/bookings', views.bookings, name="bookings"),
    path('adven/ticket/cancel', views.cancel_ticket, name="cancelticket"),
    path('adven/ticket/resume', views.resume_booking, name="resumebooking"),
    path('contact', views.contact, name="contact"),
    path('privacy-policy', views.privacy_policy, name="privacypolicy"),
    path('terms-and-conditions', views.terms_and_conditions, name="termsandconditions"),
    path('about-us', views.about_us, name="aboutus"),
    path('mountain-adven', views.mountain_adven, name="mountain_adven"),
    path('water-adven', views.water_adven, name="water_adven"),
    path('road-adven', views.road_adven, name="road_adven"),
    path('air-adven', views.air_adven, name="air_adven"),
]