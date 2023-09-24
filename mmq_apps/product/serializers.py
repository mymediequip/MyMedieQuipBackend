from .models import *
from rest_framework import serializers
from django.conf import settings


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'

class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):

    product_images = serializers.SerializerMethodField('get_product_images')
    product_video = serializers.SerializerMethodField('get_product_video')

    


    def get_product_images(self, obj):
        video = []
        try:
            queryset = ProductImage.objects.filter(product=obj.uid)
            serializer_obj = ProductImageSerializer(queryset,many=True)
            return serializer_obj.data
            
        except Exception as e:
            print("error",e)
            return []

    def get_product_video(self, obj):
        video = []
        try:
            queryset = ProductVideo.objects.filter(product=obj.uid)
            serializer_obj = ProductVideoSerializer(queryset,many=True)
            return serializer_obj.data
            
        except Exception as e:
            print("error",e)
            return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation

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



class ProductImageSerializer(serializers.ModelSerializer):

    product_images = serializers.SerializerMethodField('get_product_images')


    def get_product_images(self, obj):
        path = ''
        try:
            image = obj.p_image
            print(image,"...........s_image")
            if image:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/product/image/'+image

            return path
        except Exception as e:
            print("error",e)
            return path

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVideoSerializer(serializers.ModelSerializer):
    product_video = serializers.SerializerMethodField('get_product_video')

    def get_product_video(self, obj):
        path = ''
        try:
            video = obj.video
            print(video,"...........s_image")
            if video:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/product/video/'+video

            return path
        except Exception as e:
            print("error",e)
            return path
    

    class Meta:
        model = ProductVideo
        fields = '__all__'

class ScheduleMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model=ScheduleMeeting
        fields='__all__'
