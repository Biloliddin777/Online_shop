from django.contrib import admin
from django.contrib.auth.models import User, Group

from online_shop.models import Product, Category, Comment, Order

# Register your models here.

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Comment)
# admin.site.register(Order)

admin.site.unregister(User)
admin.site.unregister(Group)


class IsVeryExpensiveFilter(admin.SimpleListFilter):
    title = 'Is Very Expensive Product'
    parameter_name = 'is_very_expensive_product'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(price__gt=30_000)
        elif value == 'No':
            return queryset.exclude(price__gt=30_000)
        return queryset


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','product_count')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'discount', 'get_image_url', 'is_very_expensive_product')
    search_fields = ['name']
    list_filter = ['category', IsVeryExpensiveFilter]

    def is_very_expensive_product(self, obj):
        return obj.price > 30_000

    is_very_expensive_product.boolean = True


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'quantity')
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body')
    search_fields = ['name']
    list_filter = ['name']
