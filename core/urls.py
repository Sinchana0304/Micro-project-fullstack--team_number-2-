from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ----------------------------
    # Authentication & Registration
    # ----------------------------
    path('choose-role/', views.choose_role, name='choose_role'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ----------------------------
    # Dashboards
    # ----------------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('organiser/dashboard/', views.organiser_dashboard, name='organiser_dashboard'),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),

    # ----------------------------
    # Disaster Management (Organiser)
    # ----------------------------
    path('organiser/post-disaster/', views.post_disaster, name='post_disaster'),
    path('organiser/disaster/<int:disaster_id>/', views.view_disaster, name='view_disaster'),
    path('organiser/disaster/<int:disaster_id>/edit/', views.edit_disaster, name='edit_disaster'),
    path('organiser/disaster/<int:disaster_id>/delete/', views.delete_disaster, name='delete_disaster'),
    path('organiser/messages/', views.organiser_messages, name='organiser_messages'),
    path('organiser/feedback/', views.organiser_feedback, name='organiser_feedback'),
    path('organiser/donations/', views.organiser_donations, name='organiser_donations'),

    # ----------------------------
    # Donation & Interaction (Donor)
    # ----------------------------
    path('donor/disaster/<int:disaster_id>/donate/', views.donate_to_disaster, name='donate_to_disaster'),
    path('donor/donations/', views.donor_donations, name='donor_donations'),
    path('donor/feedback/', views.donor_feedback, name='donor_feedback'),
    path('donor/messages/', views.donor_messages, name='donor_messages'),

    # ----------------------------
    # Shared Features
    # ----------------------------
    path('messages/<int:disaster_id>/', views.message_thread, name='message_thread'),
    path('feedback/<int:disaster_id>/submit/', views.submit_feedback, name='submit_feedback'),
    path('profile/', views.user_profile, name='user_profile'),
]
