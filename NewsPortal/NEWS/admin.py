from django.contrib import admin
from .models import Category, Product, Author, Post, PostCategory, Comment


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(quantity=0)
    nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'dataCreation', 'rating', 'categoryType') 
    list_filter = ('author', 'rating', 'categoryType')  
    search_fields = ('name', 'category__name')  
    actions = [nullfy_rating]  


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
# admin.site.unregister(Product)
