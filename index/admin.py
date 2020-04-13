from django.contrib import admin
from .models import *

class GoodsAdmin(admin.ModelAdmin):
    #指定在列表頁中顯示的字段們
    list_display = ('title','goodstype','price','spec')
    #指定右側顯示的過濾器
    list_filter = ('goodstype',)
    #指定在上方顯示搜索字段們
    search_fields = ('title',)

# Register your models here.
admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(User)