from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def createCustomer(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=Customer)
def createUsername(sender, instance, created, *args, **kwargs):
    if created:
        instance.username = f"customer{instance.id}"
        instance.save()


class Departure(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='destinations/%Y/%m', default=None)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="100" />'.format(self.image.url))
        else:
            return ""


class Transport(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m', default=None)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" />'.format(self.image.url))
        else:
            return ""


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
    image = models.ImageField(upload_to='tours/%Y/%m', default=None)
    depart_date = models.DateTimeField() # ngay bat dau
    duration = models.IntegerField()  # so ngay cua tour
    price = models.IntegerField()  # gia tour
    status = models.BooleanField(default=True)
    discount = models.IntegerField(default=0)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=40)

    departure = models.ForeignKey(Departure, related_name="tours", on_delete=models.SET_NULL,null=True)  # noi khoi hanh
    categories = models.ManyToManyField(Category, related_name='tours', blank=True, null=True)
    destination = models.ManyToManyField(Destination, related_name='tours',blank=True, null=True)  # diem dem

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.price-self.price*self.discount/100

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="100" />'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default=None)
    image = models.ImageField(upload_to='tours/', default=None)

    def __str__(self):
        return self.name


class TourDetail(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL,null=True)
    transports = models.ManyToManyField(Transport, related_name='detail', blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.tour.name


class Booking(models.Model):

    BOOKING_STATUS =(
        ('New', 'New'),
        ('Booking processing','Booking processing'),
        ('Booking accepted', 'Booking accepted'),
        ('Booking canceled', 'Booking canceled')
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)
    adult = models.IntegerField(validators=[MinValueValidator(1)], default=0)
    children = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    status = models.CharField(max_length=25, choices=BOOKING_STATUS, default="New")
    private_room = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def tour_name(self):
        return self.tour.name

    @property
    def total(self):
        if self.private_room == False:
            return self.tour.final_price*self.adult+self.tour.final_price*self.children*60/100
        return self.tour.final_price*self.adult+self.tour.final_price*self.children*60/100 + 800000

    @property
    def quantity(self):
        return self.adult+self.children

    def slot(self):
        if self.quantity is not None:
            slt = self.tour.quantity - self.quantity
            return slt


class Payment(models.Model):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(upload_to='blogs/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    content = RichTextUploadingField()

    category = models.ManyToManyField(Category, related_name='blogs', blank=True, null=True)
    destination = models.ForeignKey(Destination, related_name='blogs', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="100" />'.format(self.image.url))
        else:
            return ""


class TourView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE)


class Slider(models.Model):
    image = models.ImageField(upload_to='slides/%Y/%m', default=None)
    caption = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.caption

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="100" />'.format(self.image.url))
        else:
            return ""


