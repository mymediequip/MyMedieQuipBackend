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
            profile_data = ProfileSerializer(queryset).data
        except Exception as e:
            pass
        return profile_data

    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileDetailSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')
    cozuntry_name = serializers.ReadOnlyField(source='country.name')
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


class ExpertiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expertise
        fields = '__all__'


class OurClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OurClient
        fields = '__all__'