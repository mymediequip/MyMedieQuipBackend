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
    user_type_value = serializers.ReadOnlyField(source='user_type.user_type')
    profile_details = serializers.SerializerMethodField('get_user_name')

    def get_user_name(self, obj):
        profile_detail = {}
        profile_obj = Profile.objects.filter(user=obj.id)
        if len(profile_obj)>0:
            profile_detail = ProfileDetailSerializer(profile_obj[0]).data
        else:
            profile_detail = profile_detail
        return profile_detail
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'mobile', 'user_type', 'profile_details', 'user_type_value', 'uid','is_mobile_verified','is_email_verified','is_pancard_verified','is_adhar_verified','verify_type','last_login','verify_type', 'default_instId','wallet_address','wallet_privatekey','usertypes','is_passport_verified','is_voter_verified','is_licence_verified','virtual_id')


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
    document = serializers.SerializerMethodField('get_document')
    sub_account = serializers.SerializerMethodField('get_sub_account')

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

    def get_sub_account(self, obj):
        detail = {}
        try:
            queryset = SubAccount.objects.get(user=obj.id)
            detail = SubAccountDetailSerializer(queryset).data
        except Exception as e:
            print("subaccount error",e)

        return detail

    class Meta:
        model = User
        fields = ('id', 'email', 'mobile', 'user_type', 'user_type_value', 'uid','is_mobile_verified','is_email_verified','is_pancard_verified','is_adhar_verified','verify_type','last_login','profile','document','sub_account','default_instId','wallet_address','wallet_privatekey','is_passport_verified','is_voter_verified','is_licence_verified','virtual_id')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileDetailSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')
    country_name = serializers.ReadOnlyField(source='country.name')
    class Meta:
        model = Profile
        fields = '__all__'

