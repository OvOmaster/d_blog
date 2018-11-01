from django.contrib import admin
from .models import User, Posts

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # 设置显示字段
    list_display = ['pk', 'username', 'email', 'is_active', 'is_superuser', 'date_joined', 'last_login']
    # 添加搜索字段
    search_fields = ['username']
    # 分页
    list_per_page = 5
    # 过滤字段
    list_filter = ['username']


class PostsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'article', 'visit', 'upload_time', 'user']
    search_fields = ['title']
    list_per_page = 5
    list_filter = ['title']
    # fieldsets = [("基本信息", {"fields": ['title', 'article', 'visit']}),
    #               ('其他信息', {'fields': ['upload_time', 'user']})]


admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
