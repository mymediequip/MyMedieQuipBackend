import hashlib
#Django Rest Framework Import
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
import rest_framework.status as status


#Djagno Import
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.db.models import Q

from mmq.auth_frontend import authenticate_frontend
from mmq.functions import *
from mmq.services.users.otp_management import *
#from shopinzip.pagination import GetPagination
from mmq.token_authentication import ExpiringTokenAuthentication

from .functions import getToken,deleteToken
from django.contrib.auth import authenticate,login
from .models import *
from .serializers import *



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = OtpSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    name = 'users'

    def get_permissions(self):

        if self.action == 'generateotp' or self.action == 'verifyotp' or self.action == 'forgot_password' or self.action == 'reset_password':
            print("\n in self action")
            return [AllowAny(), ] 
        return super(UserViewSet, self).get_permissions()


    @action(detail=False, methods=['post'])
    def generateotp(self,request):  
        """
            This method is used for otp genera

        """

        try:

            data = request.data.copy()
            print(data)
            email = data.get("email",None)
            mobile = data.get("mobile",None)

            try:
                otp =  Otp.objects.get(mobile=mobile)


            except Otp.DoesNotExist:
                otp = Otp.objects.create(mobile=mobile)
                # otp = User.objects.get(email=email)


            otp.counter += 1
            otp.save()
            manage_otp = OtpManagement()
            otp_dict = manage_otp.generateotp(otp.mobile,otp.counter)
            print(otp_dict["code"])
            # obj = send_mail(
            #       'Registration',
            #       'Here is opt for login to Shopinzip.   '+otp_dict["code"],
            #       settings.DEFAULT_FROM_EMAIL,
            #       [email],
            #       fail_silently=False,
            # )

            new_data = {}
            new_data["otp"] = otp_dict["code"]

            return SimpleResponse(
                        {"data":new_data},
                        status=status.HTTP_200_OK
                    )

        except Exception as e:
            return SimpleResponse(
                        {"msg":str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1,
                    )
            




    #addd
    @action(detail=False, methods=['post'])
    def verifyotp(self,request):
        """This Method is Used for login of existing users

        """

        mobile = request.data.get("mobile",None)
        code =  request.data.get("otp",None)
        response_data = {}
        try:
            otp = Otp.objects.get(mobile=mobile)
            print(otp,"otp")

        except Otp.DoesNotExist:
            return SimpleResponse(
                        {"msg": "Mobile Number does not Exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
        manage_otp = OtpManagement()

        is_verified = manage_otp.verifyotp(code,otp.mobile,otp.counter)
        print("is_verified",is_verified)
        if is_verified:
            otp.is_verified=True
            otp.save()
            user_auth = True

            try:
                user = User.objects.get(username=mobile)
                print("user",user)
                user_auth = False
                # user_auth = authenticate(username=mobile)
        
                if not user_auth:
                    return SimpleResponse(
                        {"msg": "Otp is wrong"},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
                else:
                    log_object =login(request, user_auth)
                    user.is_phone_verifed = True
                    user.device_id = 1
                    user.save()

                    print("log_object is ", log_object)

            except User.DoesNotExist:
                print("Error",1)
                usertype = UserType.objects.get(id=2)
                user = User.objects.create(
                    username = mobile,
                    mobile=mobile,
                    is_mobile_verified = True,
                    user_type = usertype,
                    # device_id = 1
                )
                
                print("user>>>",user)
                user.set_unusable_password()
                user.save( )

            # token = getToken(user.id)
            # response_data["token"] = token
            response_data["username"] = user.username
            response_data["email"] = user.email 
            response_data["mobile"] = user.mobile
            response_data["user_id"] = user.id
            # response_data["name"] = user.name
            response_data["is_mobile_verified"] = user.is_mobile_verified
            return SimpleResponse(
                        {"data":response_data},
                        status=status.HTTP_200_OK
                    )
        else:
            return SimpleResponse(
                        {"msg": "Otp is wrong"},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

    @action(detail=False,methods=['post'])
    def update_user_profile(self,request):

        try:
            user = request.user
            data = request.data
            userid = request.user.id
            user_obj = User.objects.get(id=userid)
            serializer = UserSerializer(user_obj,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()

                return CustomeResponse(
                    {"msg": "Profile Updated Successfully"},
                    status=status.HTTP_200_OK
                )

            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )

        except Exception as e:
            return CustomeResponse(
                {"msg":str(e)},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1               

                )
    
    @action(detail=False,methods=['post'])
    def get_user_profile(self,request):
        user = request.user.id
        email = request.user.email
        try:
            userprofile = Profile.objects.get(user=user)
            print("user details>>>",userprofile)
            serializer = ProfileSerializer(userprofile)
            data = {}
            user_profile_data = {}
            user_profile_data = serializer.data
            user_profile_data.update({'email':email})

            data['user_profile'] = user_profile_data
            data['email'] = email
            return CustomeResponse(
                data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return CustomeResponse(
                {"msg":"Record Not ound"},
                status = status.HTTP_201_CREATED
            )
      


    @action(detail = False,methods=['post'])
    def addprofile(self,request):
        data = request.data.copy()
        user = request.user
        data['user'] = user.id
        profile = ''
        name = data.get('name',None)
        if not name:
            return CustomeResponse(
                    {"msg":"name is required field"},
                    status = status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )



        try:
            user.name = data.get('name','')
            user.save()
        except Exception as e:
            print(e)
            printException()

        try:
            try:
                profile = Profile.objects.get(user_id=user.id)
            except Exception as e:
                profile = ''

            if profile:
                serializer = ProfileSerializer(profile,data=data)
            else:
                serializer = ProfileSerializer(data=data)

            try:
                queryset = User.objects.get(id=user.id)
                email = data.get('email',None)
                if email:
                    print(email,"email")
                    queryset.email = email
                    queryset.update_password = False
                    queryset.save()
                   
                    
            except Exception as e:
                printException()
                print(e)
            
            if serializer.is_valid():
                serializer.save()
                return CustomeResponse(
                    {"msg":"User Profile saved successfully"},
                    status = status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    {"msg":serializer.errors},
                    status = status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Exception as e:
            return CustomeResponse(
                {"msg":str(e)},
                status= status.HTTP_400_BAD_REQUEST,
                validate_errors =1
            )

    @action(detail = False,methods=['post'])
    def search_user(self,request):
        data = request.data.copy()
        search = data.get("search",None)
        try:
            queryset = User.objects.filter(Q(name__icontains=search) | Q(phone_no__icontains=search) ).filter(user_type=2)
            # print(queryset)
            serializer = UserSelectListSerializer(queryset,many=True)
            if len(list_data) > 0:
                return CustomeResponse(
                    serializer.data,
                    status = status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    {"msg":"Record Not Found"},
                    status = status.HTTP_200_OK
                )
        except Exception as e:
            printException()
            return CustomeResponse(
                {"msg":str(e)},
                status= status.HTTP_400_BAD_REQUEST,
                validate_errors =1
            )

    @action(detail = False,methods=['post'])
    def user_all_detail(self, request):
        data = request.data.copy()
        user_id = request.user.id
        try:
            queryset = User.objects.get(id=user_id)
            serializer_obj = UserDetailSerializer(queryset).data
            return CustomeResponse(
                serializer_obj,
                status = status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Error..",e)
            printException()
            return CustomeResponse(
                {"msg":str(e)},
                status= status.HTTP_400_BAD_REQUEST,
                validate_errors =1
            )






