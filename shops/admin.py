from django.contrib import admin
from .models import Shop, ShopTag, RegularHoliday

# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopTag)
admin.site.register(RegularHoliday)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'phoneNumber', 'address')
    filter_horizontal = ('regularHoliday',)  # 横にフィルターを適用してクリアボタンを表示