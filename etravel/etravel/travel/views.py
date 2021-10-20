from django.conf import settings
from django.db.models import F
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import filters
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from django.http import HttpResponsePermanentRedirect
import os
from .permission import UserPermission
from .serializers import *
from rest_framework.decorators import action


def index(request):
    return render(request, 'index.html', context={'name': 'DU LỊCH VIỆT'})


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.filter(status=True)
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['duration', 'departure__name', 'destination__name', 'depart_date']

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

    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = TourView.objects.get_or_create(tour=self.get_object())
        v.views = F('views') + 1
        v.save()
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


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [UserPermission]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        elif self.action == 'block-user':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='block-user', url_name='block-user')
    def block_user(self, request, pk):
        try:
            t = User.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except User.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=UserSerializer(t, context={'request': request}).data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path="create-staff", url_name="create-staff")
    def create_staff(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['put'],detail=False, serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class DepartureViewset(viewsets.ModelViewSet):
    queryset = Departure.objects.all()
    serializer_class = DepartureSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tour__name', 'id']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]


class HotelView(viewsets.ModelViewSet):
    queryset = Hotel.objects.filter(status=True)
    serializer_class = HotelSerializer


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = TagSerializer


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


class MostViewsTours(APIView):
    def get(self, request):
        tour_obj = TourView.objects.all().order_by('-views')[:12]
        tour_obj_data = TourViewSerializer(tour_obj, many=True, context={'request': request}).data
        return Response(tour_obj_data)


class NewToursView(viewsets.ViewSet):
    queryset = Tour.objects.all()

    def list(self, request):
        tour_obj = self.queryset.order_by('created_at')[:12]
        tour_obj_data = NewTourSerializer(tour_obj, many=True, context={'request': request}).data
        return Response(tour_obj_data)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)