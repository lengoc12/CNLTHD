from importlib._common import _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/%Y/%m', default=None)


class Departure(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='images/destinations/%Y/%m', default=None)

    def __str__(self):
        return self.name


class Transport(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='tag/%Y/%m', default=None)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    status = models.BooleanField(default=True)

    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='images/tour/%Y/%m', default=None)
    depart_date = models.DateTimeField()  # ngay bat dau
    duration = models.IntegerField()  # so ngay cua tour
    price = models.IntegerField()  # gia tour
    status = models.BooleanField(default=True)
    discount = models.IntegerField(default=0)
    content = RichTextField()

    departure = models.ForeignKey(Departure, related_name="tours", on_delete=models.SET_NULL,null=True)  # noi khoi hanh
    tags = models.ManyToManyField(Tag, related_name='tours', blank=True, null=True)
    destination = models.ForeignKey(Destination, related_name='tours', on_delete=models.SET_NULL, null=True)  # diem dem

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.price-self.price*self.discount/100


class TourDetail(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL,null=True)
    transports = models.ManyToManyField(Transport, related_name='detail', blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.tour.name


class Receipt(models.Model):

    BOOKING_STATUS =(
        ('New', 'New'),
        ('Booking processing','Booking processing'),
        ('Booking accepted', 'Booking accepted'),
        ('Booking canceled', 'Booking canceled')
    )
    created_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)
    adult = models.IntegerField(validators=[MinValueValidator(1)], default=0)
    children = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    status = models.CharField(max_length=25, choices=BOOKING_STATUS, default="New")

    def __str__(self):
        return self.customer.email

    @property
    def total(self):
        return self.tour.final_price*self.adult+self.tour.final_price*self.children*60/100


class Payment(models.Model):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='images/blog/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    content = RichTextUploadingField()

    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True, null=True)
    destination = models.ForeignKey(Destination, related_name='blogs', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class TourView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE)


class Slider(models.Model):
    image = models.ImageField(upload_to='images/slider/%Y/%m', default=None)
    name = models.CharField(max_length=255, default=None)

