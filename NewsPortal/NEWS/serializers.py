from .models import *
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['name', 'title', 'text', 'rating', 'categoryType', 'postCategory', 'dataCreation', ]

#
# class ArticleSerializer(serializers. ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'name', 'rating', 'title', 'text', 'rating', ]
#
#
# class PostSerializer(serializers. ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'name', 'title', 'text', 'rating', ]
#
#
# # class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = PostCategory
# #         fields = ['id', 'name', ]
#
#
