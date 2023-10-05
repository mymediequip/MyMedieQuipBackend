from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings


class OtpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Otp


class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    user_type_value = serializers.ReadOnlyField(source='user_type.user_type')
    profile = serializers.SerializerMethodField('get_profile')
    document = serializers.SerializerMethodField('get_document')
    

    def get_profile(self, obj):
        profile_data = {}
        try:
            queryset = Profile.objects.get(user=obj.id)
            profile_data = ProfileDetailSerializer(queryset).data
        except Exception as e:
            pass
        return profile_data

    def get_document(self, obj):
        document_data = {}
        try:
            queryset = Document.objects.filter(user=obj.id)
            document_data = DocumentSerializer(queryset,many=True).data
        except Exception as e:
            print(e)
            pass
        return document_data

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'mobile', 'user_type', 'user_type_value', 'uid','is_mobile_verified','is_email_verified','is_pancard_verified','is_adhar_verified','verify_type','last_login','profile','document','default_instId','wallet_address','wallet_privatekey','is_passport_verified','is_voter_verified','is_licence_verified','virtual_id')


class UserDetailSerializer(serializers.ModelSerializer):
    user_type_value = serializers.ReadOnlyField(source='user_type.user_type')
    profile = serializers.SerializerMethodField('get_profile')

    def get_profile(self, obj):
        profile_data = {}
        try:
            queryset = Profile.objects.get(user=obj.id)
            print("queryset",queryset)
            profile_data = ProfileDetailSerializer(queryset).data
        except Exception as e:
            pass
        return profile_data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation 

    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileDetailSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField('get_profile_image')

    def get_profile_image(self, obj):
        path = ''
        try:
            image = obj.profile_image
            print(image,"...........s_image")
            if image:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/profile/'+image

            return path
        except Exception as e:
            print("error",e)
            return path

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation
    
    class Meta:
        model = Profile
        fields = '__all__'



# class ProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = '__all__'

# class ProductDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = '__all__'

# class ProductuniqueSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = ('id')


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class BannerDeatilSerializer(serializers.ModelSerializer):

    banner_image = serializers.SerializerMethodField('get_banner_image')

    def get_banner_image(self, obj):
        path = ''
        try:
            image = obj.banner_image
            print(image,"...........s_image")
            if image:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/banner/'+image

            return path
        except Exception as e:
            print("error",e)
            return path

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation

    class Meta:
        model = Banner
        fields = '__all__'

class ExpertiseSerializer(serializers.ModelSerializer):


    class Meta:
        model = Expertise
        fields = '__all__'

class ExpertiseDeatilSerializer(serializers.ModelSerializer):
    expertise_image = serializers.SerializerMethodField('get_expertise_image')

    def get_expertise_image(self, obj):
        path = ''
        try:
            image = obj.expertise_image
            print(image,"...........s_image")
            if image:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/expertise/'+image

            return path
        except Exception as e:
            print("error",e)
            return path

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation

    class Meta:
        model = Expertise
        fields = '__all__'

class OurClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OurClient
        fields = '__all__'

class OurClientDetailSerializer(serializers.ModelSerializer):
    client_image = serializers.SerializerMethodField('get_client_image')

    def get_client_image(self, obj):
        path = ''
        try:
            image = obj.client_image
            print(image,"...........s_image")
            if image:
                path =  str(settings.BASE_FILE_PATH)+'static/upload/client/'+image

            return path
        except Exception as e:
            print("error",e)
            return path

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        created_date = instance.created_date.strftime(settings.FRONT_DATE_FORMATE) if instance.created_date is not None and instance.created_date!="" else None
        representation['date'] = created_date
        return representation

    class Meta:
        model = OurClient
        fields = '__all__'



class PaymentOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentOption
        fields = '__all__'