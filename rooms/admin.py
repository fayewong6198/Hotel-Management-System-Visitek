from django.contrib import admin
from .models import Room
from .models import RoomImage
from .models import Payment
# Register your models here.


class RoomImageAdmin(admin.ModelAdmin):
    pass


class RoomImageInline(admin.StackedInline):
    model = RoomImage
    max_num = 20
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, ]

    list_display = ('id', 'room_id', 'price', 'adults', 'children')
    list_display_links = ('id', 'room_id')
    list_per_page = 25


class PaymentAmdin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'total',
                    'expected_check_in_date', 'expected_check_out_date', 'created_at')


admin.site.register(Room, RoomAdmin)
admin.site.register(Payment, PaymentAmdin)
