from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.db.models import Count
from django.urls import path
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from .models import *


@admin.register(User)
class UserAdmin(UserAdmin):
    class Meta:
        model = User
        filter = '__all__'


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


class TourInline(admin.StackedInline):
    model = Tour
    fk_name = 'destination'


class DestinationAdmin(admin.ModelAdmin):
    inlines = (TourInline, BlogInline)


class TransportInlineAdmin(admin.TabularInline):
    model = TourDetail.transports.through


class TourTagInlineAdmin(admin.TabularInline):
    model = Tour.tags.through


class BlogTagInlineAdmin(admin.TabularInline):
    model = Blog.tags.through


class TagAdmin(admin.ModelAdmin):
    inlines = [TourTagInlineAdmin, BlogTagInlineAdmin, ]


class TransportAdmin(admin.ModelAdmin):
    inlines = [TransportInlineAdmin,]


class TourAdmin(admin.ModelAdmin):
    form = TourForm
    inlines = [TourTagInlineAdmin, ]
    list_display = ['id', 'name', 'depart_date', 'duration', 'price', 'discount', 'departure', 'destination', 'status', ]
    search_fields = ['name', 'depart_date', 'duration', 'price', 'departure', 'destination']
    list_filter = ['depart_date', 'duration', 'price']
    readonly_fields = ['avatar']

    def avatar(self, tour):
        return mark_safe(
            '<img src="/static/images/{img_url}" alt="{alt}" width="200px" />'.format(img_url=tour.image.name, alt=tour.name))


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    inlines = [BlogTagInlineAdmin, ]
    list_display = ['id', 'title', 'created_date', 'destination', 'status', ]
    search_fields = ['title', 'destination', ]
    list_filter = ['created_date', ]

    readonly_fields = ['image_tag']

    def image_tag(self, blog):
        return mark_safe(
            '<img src="/static/images/{img_url}" alt="{alt}" width="200px" />'.format(img_url=blog.image.name, alt=blog.name))


class TourDetailAdmin(admin.ModelAdmin):
    inlines = [TransportInlineAdmin,]


class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'tour', 'adult', 'children', 'status', 'total', 'created_date']
    list_filter = ['created_date']
    search_fields = ['tour']


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


admin.site.site_header ="HỆ THỐNG QUẢN LÝ TOUR DU LỊCH VIỆT"
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Departure)
admin.site.register(Hotel)
#admin.site.register(Employee)
admin.site.register(TourDetail, TourDetailAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Transport)
admin.site.register(Receipt)
admin.site.register(Tag, TagAdmin)
admin.site.register(Permission)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Slider)
