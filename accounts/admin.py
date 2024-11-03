from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
#from django.contrib.auth.admin import UserAdmin
from .models import User,Yoyaku_ID,Kiyaku

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'id', )

admin.site.register(User,UserAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします
admin.site.register(Yoyaku_ID)
admin.site.register(Kiyaku)
