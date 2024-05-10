import nested_admin
from django.contrib import admin

from .models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    SeasonalEvent,
)

admin.site.register(ProductLine)


class ProductImageInline(nested_admin.NestedStackedInline):
    model = ProductImage
    extra = 1


class ProductLineInline(nested_admin.NestedStackedInline):
    model = ProductLine
    inlines = [ProductImageInline]
    extra = 1


class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductLineInline]

    list_display = ("name", "category", "stock_status", "is_active")

    list_filter = (
        "category",
        "stock_status",
        "is_active",
    )

    search_fields = ("name",)


admin.site.register(Product, ProductAdmin)


class SeasonalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")


admin.site.register(SeasonalEvent, SeasonalEventAdmin)


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


admin.site.register(Attribute, AttributeAdmin)


# show any types of children inline if they exist
class ChildTypeInline(admin.TabularInline):
    model = ProductType
    fk_name = "parent"
    extra = 1


class ParentTypeAdmin(admin.ModelAdmin):
    inlines = [ChildTypeInline]


admin.site.register(ProductType, ParentTypeAdmin)


# show any children inline if they exist
class ChildCategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    extra = 1


class ParentCategoryAdmin(admin.ModelAdmin):
    inlines = [ChildCategoryInline]
    list_display = (
        "name",
        "parent_name",
    )

    # look at the parent field of the category and return the parent name if it exists
    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None


admin.site.register(Category, ParentCategoryAdmin)
