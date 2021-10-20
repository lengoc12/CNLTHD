from django.contrib import auth
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "is_superuser", "is_staff",]
        extra_kwargs = {'password': {"write_only": True, 'required': True}, }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', ]


class DestinationSerializer(ModelSerializer):

    class Meta:
        model = Destination
        fields = "__all__"


class DepartureSerializer(ModelSerializer):
    class Meta:
        model = Departure
        fields = "__all__"


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class TransportSerializer(ModelSerializer):
    class Meta:
        model = Transport
        fields = "__all__"


class TourSerializer(ModelSerializer):
    depart_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    updated_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"
        depth = 1


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class TourDetailViewSet(ModelSerializer):
    depart_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)

    class Meta:
        model = TourDetail
        fields = "__all__"
        depth = 1


class TourViewSerializer(ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    depart_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)

    class Meta:
        model = TourView
        fields = "__all__"
        depth = 1

        def to_representation(self, instance):
            response = super().to_representation(instance)
            request = self.context.get('request')
            response['tour'] = TourSerializer(instance.product, context={'request': request}).data
            return response


class NewTourSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    depart_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"
        depth = 1

        def to_representation(self, instance):
            response = super().to_representation(instance)
            request = self.context.get('request')
            response['tour'] = TourSerializer(instance.product, context={'request': request}).data
            return response


class SliderSerializer(ModelSerializer):
    class Meta:
        model = Slider
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"
