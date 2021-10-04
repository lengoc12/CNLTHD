from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, request, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import filters
from rest_framework import viewsets, permissions, status, generics
from .serializers import *
from rest_framework.decorators import action


def index(request):
    return render(request, 'index.html', context={'name': 'DU LỊCH VIỆT'})


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['price', 'name', 'id', 'duration', 'departure__name', 'destination__name']
    #permission_classes = [permissions.IsAuthenticated,]

    #def get_permissions(self):
    #    if self.action == 'list':
    #        return [permissions.AllowAny()]
    #
    #    return [permissions.IsAuthenticated()]
    @swagger_auto_schema(
        operation_description="Hide Tour",
        responses={
            status.HTTP_200_OK: TourSerializer()
        }
    )
    @action(methods=['post'], detail=True)
    def hide_tour(self, request, pk, url_path='hide-tour', url_name='hide-tour'):
        try:
            t = Tour.objects.get(pk=pk)
            t.status = False
            t.save()
        except Tour.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=TourSerializer(t, context={'request': request}).data, status=status.HTTP_200_OK)

    def get_queryset(self):
        tours = Tour.objects.filter(status=True)
        q = self.request.query_params.get('q')
        if q is not None:
            tours = tours.filter(subject__contains=q)

        des_id = self.request.query_params.get('destination_id')
        if des_id is not None:
            tours = tours.filter(destination_id=des_id)
        return tours

    @action(methods=['post'], detail=True, url_path='tags')
    def add_tag(self, request, pk):
        try:
            tour = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _=Tag.objects.get_or_create(name=tag)
                    tour.tags.add(t)
                tour.save()
                return Response(self.serializer_class(tour).data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = TourView.objects.get_or_create(tour=self.get_object())
        v.views = F('views') + 1
        v.save()

        # v.views = int(v.views)
        v.refresh_from_db()

        return Response(TourViewSerializer(v).data, status=status.HTTP_200_OK)


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    @action(methods=['get'], detail=True, url_path='tours')
    def get_tours(self, request, pk):
        tours = Destination.objects.get(pk=pk).tours.filter(status=True)
        q = request.query_params.get('q')
        if q is not None:
            tours = tours.filter(subjects__icontains=q)
        return Response(TourSerializer(tours, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.ListAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email',]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)


class DepartureViewset(viewsets.ModelViewSet):
    queryset = Departure.objects.all()
    serializer_class = DepartureSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['total', 'tour_name', 'id']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class TransprotViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'name']


class TourDetailViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = TourDetail.objects.all()
    serializer_class = TourDetailViewSet
    filter_backends = [filters.SearchFilter]
    search_fields = ['tour__name', 'transports__name', 'hotel__name',]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer