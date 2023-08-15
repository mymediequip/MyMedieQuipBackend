from .models import *
from rest_framework import serializers
from django.conf import settings




class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children')
