from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tours', views.TourViewSet, 'tour')
router.register('users', views.UserViewSet)
router.register('blogs', views.BlogViewSet)
router.register('departures', views.DepartureViewset)
router.register('recepits', views.ReceiptViewSet)
router.register('tourdetails', views.TourDetailViewSet)
router.register('transport', views.TransprotViewSet)
router.register('destinations', views.DestinationViewSet)
router.register('tags', views.TagViewSet)
router.register('sliders', views.SliderViewSet)

urlpatterns = [
    path('home/', views.index, name='index'),
    path('', include(router.urls)),
]