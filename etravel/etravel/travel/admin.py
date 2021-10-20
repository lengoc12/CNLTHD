from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db.models import Count
from django.urls import path
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.template.response import TemplateResponse
import admin_thumbnails
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', ]
    ordering = ['name']


@admin_thumbnails.thumbnail('image')
class TourImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

        content = forms.CharField(widget=CKEditorUploadingWidget)


class BlogInline(admin.StackedInline):
    model = Blog
    fk_name = 'destination'


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'

    content = forms.CharField(widget=CKEditorUploadingWidget)


class DestinationAdmin(admin.ModelAdmin):
    inlines = (BlogInline, )
    list_display = ["id", "name", "image_tag"]
    readonly_fields = ["image_tag", ]


class TransportInlineAdmin(admin.TabularInline):
    model = TourDetail.transports.through


class TourCategoryInlineAdmin(admin.TabularInline):
    model = Tour.categories.through


class TourDestinationInlineAdmin(admin.TabularInline):
    model = Tour.destination.through


class BlogCategoryInlineAdmin(admin.TabularInline):
    model = Blog.category.through


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image_tag"]
    readonly_fields = ["image_tag", ]
    inlines = [TourCategoryInlineAdmin, BlogCategoryInlineAdmin, ]


class TransportAdmin(admin.ModelAdmin):
    inlines = [TransportInlineAdmin,]


class TourAdmin(admin.ModelAdmin):
    form = TourForm
    inlines = [TourCategoryInlineAdmin, TourDestinationInlineAdmin, TourImageInline,]
    list_display = ['id', 'name', 'depart_date', 'duration', 'price', 'discount', 'departure', 'status', ]
    search_fields = ['name', 'depart_date', 'duration', 'price', 'departure', 'destination']
    list_filter = ['depart_date', 'duration', 'price']
    readonly_fields = ('image_tag',)
    ordering = ["-created_at"]


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    inlines = [BlogCategoryInlineAdmin, ]
    list_display = ['id', 'title', 'created_date', 'destination', 'status', ]
    search_fields = ['title', 'destination', ]
    list_filter = ['created_date', ]

    readonly_fields = ('image_tag',)


class TourDetailAdmin(admin.ModelAdmin):
    inlines = [TransportInlineAdmin,]
    list_display = ["id", "tour", "hotel",]


class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", 'customer', "tour_name", "quantity", "private_room", 'status', 'total',]
    list_filter = ['status']
    search_fields = ['customer']


class TourAppAdminSite(admin.AdminSite):
    def get_urls(self):
        return [
                   path('tour_stats/', self.tour_stats)
               ] + super().get_urls()

    def tour_stats(self, request):
        tour_count = Tour.objects.count()
        destination = Destination.objects.count()
        stats = Destination.objects.annotate(so_luong=Count('tours')).values('id', 'name', 'so_luong')

        return TemplateResponse(request, 'admin/tour-stats.html', {
            'tour_count': tour_count,
            'destination': destination,
            'stats': stats,

        })

    site_header = 'HỆ THỐNG QUẢN LÝ TOUR DU LỊCH'


class SlideAdmin(admin.ModelAdmin):
    list_display = ["id", "caption", "image_tag",]
    readonly_fields = ["image_tag", ]


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'name', 'image_thumbnail']


admin.site.site_header ="HỆ THỐNG QUẢN LÝ TOUR DU LỊCH VIỆT"
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Departure)
admin.site.register(Hotel)
#admin.site.register(Employee)
admin.site.register(TourDetail, TourDetailAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Transport)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Permission)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Slider, SlideAdmin)
admin.site.register(Images, ImagesAdmin)
