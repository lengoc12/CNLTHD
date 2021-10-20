from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('tours', views.TourViewSet, 'tour')
router.register("users", views.UserViewSet, 'user')
router.register('blogs', views.BlogViewSet)
router.register('departures', views.DepartureViewset)
router.register('bookings', views.BookingViewSet)
router.register('tourdetails', views.TourDetailViewSet)
router.register('transport', views.TransprotViewSet)
router.register('destinations', views.DestinationViewSet)
router.register('categories', views.CategoryViewSet)
router.register('sliders', views.SliderViewSet)
router.register('hotels', views.HotelView)
router.register('newtours', views.NewToursView, 'new')

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('mostviewtours/', views.MostViewsTours.as_view()),
    #path('newtours/', views.NewToursView.as_view()),
]