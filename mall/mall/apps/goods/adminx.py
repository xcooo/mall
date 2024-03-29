from django.contrib import admin
import xadmin
from xadmin import views

# Register your models here.

from . import models
#
#

class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "幸运商城运营管理系统"  # 设置站点标题
    site_footer = "幸运商城"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    list_editable = ['price', 'stock']


class SKUSpecificationAdmin(object):
    def save_models(self):
        # 保存数据对象
        obj = self.new_obj
        obj.save()

        # 补充自定义行为
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self):
        # 删除数据对象
        obj = self.obj
        sku_id = obj.sku.id
        obj.delete()

        # 补充自定义行为
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku_id)

xadmin.site.register(models.GoodsCategory)
xadmin.site.register(models.GoodsChannel)
xadmin.site.register(models.Goods)
xadmin.site.register(models.Brand)
xadmin.site.register(models.GoodsSpecification)
xadmin.site.register(models.SpecificationOption, SKUSpecificationAdmin)
xadmin.site.register(models.SKU, SKUAdmin)
xadmin.site.register(models.SKUSpecification)
xadmin.site.register(models.SKUImage)








# class SKUAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.id)
#
#
# class SKUSpecificationAdmin(admin.ModelAdmin):
#     # 设置SKU规格
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.sku.id)
#
#     def delete_model(self, request, obj):
#         sku_id = obj.sku.id
#         obj.delete()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(sku_id)
#
#
# class SKUImageAdmin(admin.ModelAdmin):
#     # 设置SKU图片
#     def save_model(self, request, obj, form, change):
#         obj.save()
#
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.sku.id)
#
#         # 设置SKU默认图片
#         sku = obj.sku
#         if not sku.default_image_url:
#             sku.default_image_url = obj.image.url
#             sku.save()
#
#     def delete_model(self, request, obj):
#         sku_id = obj.sku.id
#         obj.delete()
#
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(sku_id)
#
#
# admin.site.register(models.GoodsCategory)
# admin.site.register(models.GoodsChannel)
# admin.site.register(models.Goods)
# admin.site.register(models.Brand)
# admin.site.register(models.GoodsSpecification)
# admin.site.register(models.SpecificationOption)
# admin.site.register(models.SKU, SKUAdmin)
# admin.site.register(models.SKUSpecification, SKUSpecificationAdmin)
# admin.site.register(models.SKUImage, SKUImageAdmin)