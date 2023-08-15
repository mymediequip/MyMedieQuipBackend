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

from .functions import createToken
from django.contrib.auth import authenticate,login
from .models import *
from .serializers import *
from mmq.common_list_data import common_list_data
from mmq.functions import *



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
            print(new_data)

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
        try:
            if is_verified:
                otp.is_verified=True
                otp.save()
                # user_auth = True

                try:
                    user = User.objects.get(username=mobile)
                    print("user",user)
                
                    user_auth = authenticate(mobile=mobile)
                    print(user_auth)
            
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
                    printException()
                    usertype = UserType.objects.get(id=2)
                    user = User.objects.create(
                        username = mobile,
                        mobile=mobile,
                        is_mobile_verified = True,
                        user_type = usertype,
                        device_type = 1
                    )
                    
                    print("user>>>",user)
                    user.set_unusable_password()
                    user.save( )
                print("user.id",)
                token = createToken(user_id = user.id)
                serializer_obj = UserSetSerializer(user).data
                print("serializer_obj",serializer_obj)
                serializer_obj.update({"token":str(token)})

                print(serializer_obj)
                return SimpleResponse(
                            {"data":serializer_obj},
                            status=status.HTTP_200_OK
                        )
            else:
                return SimpleResponse(
                            {"msg": "Otp is wrong"},
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1
                        )
        except Exception as e:
            printException()
            return SimpleResponse(
                            {"msg": str(e)},
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1
                        )


    @action(detail=False,methods=['post'])
    def add_profile(self,request):

        try:
            data = request.data.copy()
            user = request.user
            userid = user.id
            data['user'] = userid
            user_obj = User.objects.get(id=userid)
            serializer = UserSerializer(user_obj,data=data,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                try:
                    queryset = Profile.objects.get(user=userid)
                    serializer_obj = ProfileSerializer(queryset,data=data)
                except Profile.DoesNotExist:
                    serializer_obj = ProfileSerializer(data=data)
                
                if serializer_obj.is_valid():
                    serializer_obj.save()
                    print(serializer_obj.data)

                    return SimpleResponse(
                            {"data":serializer_obj.data},
                            status=status.HTTP_200_OK
                        )
                else:

                    return SimpleResponse(
                        {"msg": str(serializer_obj.errors)},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

            else:
                return SimpleResponse(
                        {"msg": str(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

        except Exception as e:
            return SimpleResponse(
                        {"msg": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
    
    @action(detail=False,methods=['post'])
    def get_user_detail(self,request):
        user = request.user.id
        print(user,"user")
        try:
            queryset = User.objects.get(id=user)
            serializer_obj = UserDetailSerializer(queryset)
            # resp_data = common_list_data(request, data, q_field, UserDetailSerializer, User,'-id')
            return SimpleResponse(
                            {"data":serializer_obj.data},
                            status=status.HTTP_200_OK
                        )
            
        except Exception as e:
            printException()
            print("Error",e)
            return SimpleResponse(
                        {"msg": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
      
         


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Banner'

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        banner_id = data.get("banner_id",None)
        try:
            if banner_id:
                queryset = Banner.objects.get(id=banner_id)
                serializer_obj = BannerSerializer(queryset,data=data)
            else:
                serializer_obj = BannerSerializer(data=data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return SimpleResponse(
                        {"data":serializer_obj.data},
                        status=status.HTTP_200_OK
                    )
            else:
                return SimpleResponse(
                    {"msg":str(serializer_obj.errors)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        except Exception as e:
            print("Error",str(e))
            printException()
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def lists(self,request):
        data = request.data.copy()
        q_field = ['id']
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        try:
            resp_data = common_list_data(request, data, q_field, BannerSerializer, Banner,orderfilter)
            return SimpleResponse(
                        {"data":resp_data['data']},
                        status=status.HTTP_200_OK
            )

        except Exception as e:
            print("Error",str(e))
            printException()
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )









