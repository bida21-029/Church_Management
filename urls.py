from django.urls import path
from . import views 
from .views import staff_dashboard

from .views import (
    home,
    member_list,
    member_detail,
    member_new,
    member_edit,
    member_delete,
    event_list,
    event_detail,
    event_new,
    event_edit,
    event_delete,
    donation_list,
    donation_detail,
    donation_new,
    message_list,
    message_detail,
    message_new,
    register_user,

    upcoming_birthdays,
    upcoming_events,
    donation_history,
   


    profile_view,
    profile_edit,
    
    
)


app_name = 'church_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('member_dashboard/', views.member_dashboard, name='member_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    ###############################################

    #########################################
    ###########PROFILE
    path('profile_view/', profile_view, name='profile_view'),
    path('profile_edit/<int:pk>/', profile_edit, name='profile_edit'),


    #MEMBERS
    path('members/', member_list, name='member_list'),
    path('church_app/members/<int:pk>/',member_detail, name='member_detail'),
    path('church_app/members/new/',member_new, name='member_new'),
    path('members/edit/<int:pk>/', member_edit, name='member_edit'),
    path('members/delete/<int:pk>/', member_delete, name='member_delete'),
    ######################################
    ##################EVENT
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('events/new/', event_new, name='event_new'),
    path('events/edit/<int:pk>/', event_edit, name='event_edit'),
    path('events/delete/<int:pk>/', event_delete, name='event_delete'),
    ###################################
    ###################DONATION
    path('donations/', donation_list, name='donation_list'),
    path('donations/<int:pk>/', donation_detail, name='donation_detail'),
    path('donations/new/', donation_new, name='donation_new'),
    #############################
    ####################COMMUNICATION
    path('messages/', message_list, name='message_list'),
    path('messages/<int:pk>/', message_detail, name='message_detail'),
    path('messages/new/', message_new, name='message_new'),




    ##########################
    ##################UPCOMING BIRTHDAY
     path('upcoming_birthdays/', upcoming_birthdays,  name='upcoming_birthdays'),
     ###################################
     #########################UPCOMING EVENT
     path('upcoming_events/', views.upcoming_events, name='upcoming_events'),

     ###################
     ##############DONATION HISTORY
     path('history/', donation_history, name='donation_history'),

     ####################################
     #################STATISTICS
    
 

]