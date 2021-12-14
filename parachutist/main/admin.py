from django.contrib import admin
from django.utils.safestring import mark_safe

from main import models


admin.site.register(models.RoomType)


@admin.register(models.ImageRoom)
class IamgeRoomAdmin(admin.ModelAdmin):
    fields = ('image', 'thumb', 'room_type')
    readonly_fields = ('thumb',)
    list_display = ('thumb', 'room_type')

    def thumb(self, obj):
        return mark_safe("<img src='{}' style='height: 100px; width: 100px; object-fit: contain' />".format(obj.image.url))

    thumb.allow_tags = True
    thumb.__name__ = 'Фото'


@admin.register(models.Gallery)
class PersonAdmin(admin.ModelAdmin):
    fields = ('image', 'thumb', 'type')
    readonly_fields = ('thumb',)
    list_display = ('thumb', 'type')

    def thumb(self, obj):
        return mark_safe("<img src='{}' style='height: 100px; width: 100px; object-fit: contain' />".format(obj.image.url))

    thumb.allow_tags = True
    thumb.__name__ = 'Фото'


@admin.register(models.BookedRoom)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'room_type', 'start_date', 'end_date')
    list_filter = ('start_date',)

