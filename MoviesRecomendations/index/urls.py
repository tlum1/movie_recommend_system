from django.urls import path
from .views import home_redirect, Search, MovieDetailView, set_rating

urlpatterns = [
    path('', home_redirect, name='home'),
    path('search/', Search.as_view(), name='search'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name="movie_view"),
    path('set_rating/',set_rating, name='set_rating'),
    # path('apartments-list', ApartmentsListView.as_view(), name='apartments_list'),
    # path('buildings-list', BuildingsListView.as_view(), name='buildings_list'),
    # path('meetings-list', MeetingsListView.as_view(), name='meetings_list'),
    # path('add-customer-form', get_model, name='add_customer_form'),
    # path('add-customer', get_model, name='add_customer'),
    # path('add-building-form', get_model, name='add_building_form'),
    # path('add-building', get_model, name='add_building'),
    # path('add-meeting-form', create_meeting_view, name='add_meeting_form'),
    # path('add-meeting', create_meeting_view, name='add_meeting'),
    # path('accounts/profile/', home_redirect)
]
