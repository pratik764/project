from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index '),
    path('about/',views.about,name='about'),
    path('rent-venue/',views.rent_venue,name='rent-venue'),
    path('shows-events/',views.shows_events,name='shows-events'),
    path('tickets/',views.tickets,name='tickets'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('profile/',views.profile,name='profile'),
    path('manager-add-event/',views.manager_add_event,name='manager-add-event'),
    path('manager-view-event/',views.manager_view_event,name='manager-view-event'),
    path('manager-edit-event/<int:pk>/',views.manager_edit_event,name='manager-edit-event'),
    path('manager-delete-event/<int:pk>/',views.manager_delete_event,name='manager-delete-event'),
    path('event-details/<int:pk>/',views.event_details,name='event-details'),
    path('book-event/<int:pk>/',views.book_event,name='book-event'),
    path('myevents/',views.myevents,name='myevents'),
    path('payment/<int:pk>/',views.payment,name='payment'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
]