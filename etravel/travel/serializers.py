from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    avatar = SerializerMethodField()

    def get_avatar(self, user):
        request = self.context['request']
        if user.avatar:
            name = user.avatar.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'password',]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class TagSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, tag):
        request = self.context['request']
        if tag.image:
            name = tag.image.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'image', ]


class DestinationSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, destination):
        request = self.context['request']
        if destination.image:
            name = destination.image.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = Destination
        fields = ['id', 'name', 'image']


class DepartureSerializer(ModelSerializer):
    class Meta:
        model = Departure
        fields = ['id', 'name']


class BlogSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    image = SerializerMethodField()

    def get_image(self, blog):
        request = self.context['request']
        if blog.image:
            name = blog.image.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'created_date', 'destination', 'content', 'tags', 'image',]


class ReceiptSerializer(ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'created_date','tour', 'customer', 'total', 'adult', 'children', 'status', ]


class TransportSerializer(ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id', 'name']


class TourDetailViewSet(ModelSerializer):
    transports = TransportSerializer(many=True)

    class Meta:
        model = TourDetail
        fields = ['id', 'transports', 'tour', 'hotel']


class TourSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    departure = DepartureSerializer()
    destination = DestinationSerializer()

    image = SerializerMethodField()

    def get_image(self, tour):
        request = self.context['request']
        if tour.image:
            name = tour.image.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'price', 'discount', 'destination', 'departure', 'duration', 'depart_date', 'tags']


class TourViewSerializer(ModelSerializer):
    class Meta:
        model = TourView
        fields = ["id", "views", "tour"]


class SliderSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, slider):
        request = self.context['request']
        if slider.image:
            name = slider.image.name
            if name.startswith("static/"):
                path = '/%s' % name
            else:
                path = '/static/%s' % name

            return request.build_absolute_uri(path)

    class Meta:
        model = Slider
        fields = ['id', 'image',]

