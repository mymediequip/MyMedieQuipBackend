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
import requests


def get_access_token(mobile,password):
    try:
        print(mobile,password)
        api_url = settings.API_URL + 'token/'
        r = requests.post(api_url,{"mobile":mobile, "password":password})
        if r.status_code == requests.codes.ok:
            print(">>>>>>>>>>>>>>>>>>>token deleted")
        else:
            print(">>>>>>>>>>>>>>>>>>>>>>>token could not deteted")
        token_data = r.json()
        print("token_data",token_data)
        if token_data:
            access_token = token_data["access"]
            refresh_token = token_data["refresh"]
        else:
            access_token = ""
            refresh_token = ""
    except Exception as e:
        print("Error",e)
        printException()
        access_token = ""
        refresh_token = ""

    return {'access_token':str(access_token),'refresh_token':refresh_token}

def productImage(request,booking_id):
    try:
        data = {}
        user = request.user
        msg = False
        if 'product_image' in request.FILES:
            files = request.FILES.getlist('product_image')
            for f in files:
                file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'products/',f)
                if file:
                    data.update({"booking_id":booking_id,"image":file,"created_by":user.uid})
                    # serializer_obj = ProductImagesSerializer(data=data)
                    try:
                        if serializer_obj.is_valid():
                            add_save = serializer_obj.save()
                            msg = True
                        else:
                            msg = False

                    except Exception as e:
                        printException()
                        print("error...",e)
                        msg =  False
                    print("file........",file)
                else:
                    msg =  False
        return msg
       
    except Exception as e:
        print(e, '--------------error')
        printException()
        return False

def fetch_blob_data(blob_url):
    response = requests.get(blob_url)
    print(response)

    if response.status_code == 200:
        return response.content  # Binary data as bytes
    else:
        print(f"Failed to fetch blob data from {blob_url}")
        return None
    
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
            This method is used for otp generate

        """

        try:

            data = request.data.copy()
            print(data)
            email = data.get("email",None)
            mobile = data.get("mobile",None)

            try:
                if mobile:
                    otp =  Otp.objects.get(mobile=mobile)
                if email:
                    otp =  Otp.objects.get(email=email)



            except Otp.DoesNotExist:
                if mobile:
                    otp = Otp.objects.create(mobile=mobile)
                else:
                    otp = Otp.objects.create(email=email)

                # otp = User.objects.get(email=email)


            otp.counter += 1
            otp.save()
            manage_otp = OtpManagement()
            if mobile:
                otp_dict = manage_otp.generateotp(otp.mobile,otp.counter)
            if email:
                otp_dict = manage_otp.generateotp(otp.email,otp.counter)

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
            printException()
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
        email = request.data.get("email",None)
        code =  request.data.get("otp",None)
        username = None
        if mobile:
            username = mobile
        if email:
            username = email
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
        
        is_verified = manage_otp.verifyotp(code, otp.mobile if mobile else otp.email, otp.counter)
        try:
            if is_verified:
                otp.is_verified=True
                otp.save()
                # user_auth = True

                try:
                    if email:
                        user = User.objects.get(email=email)
                        user_auth = authenticate(username=email,user_type=2)
                    if mobile:
                        user = User.objects.get(mobile=mobile)
                        user_auth = authenticate(username=mobile,user_type=2)
                    # print("user",user)
                
                    
                    # print(user_auth)
            
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

                        # print("log_object is ", log_object)

                except User.DoesNotExist:
                    print("Error",1)
                    printException()
                    usertype = UserType.objects.get(id=2)
                    user = User.objects.create(
                        username = mobile,
                        mobile=mobile,
                        email=email,
                        is_mobile_verified = True,
                        user_type = usertype,
                        device_type = 1
                    )
                    
                    print("user>>>",user)
                    user.set_unusable_password()
                    user.save( )
                # print("user.id",)
                token = createToken(user_id = user.id)
                print("username",username)
                jwt_token = get_access_token(mobile=username,password='123456')
                print(jwt_token)
                serializer_obj = UserSetSerializer(user).data
                # print("serializer_obj",serializer_obj)
                serializer_obj.update({"token":str(token)})

                # print(serializer_obj)
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
                print(request.FILES)
                print(data,"data")
                # if 'image' in data:
                #     image =  fetch_blob_data(data['image'])
                #     print(image)
                if 'image' in request.FILES:
                    image = request.FILES.get('image')
                    file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'profile/',image)
                    data['profile_image'] = file

                print("data",data)
                
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

    def get_permissions(self):

        if self.action == 'lists':
            print("\n in self action")
            return [AllowAny(), ] 
        return super(BannerViewSet, self).get_permissions()

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        banner_id = data.get("banner_id",None)
        try:
            if 'image' in request.FILES:
                image = request.FILES.get('image')
                file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'banner/',image)
                data['banner_image'] = file
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
            resp_data = common_list_data(request, data, q_field, BannerDeatilSerializer, Banner,orderfilter)
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



class MasterViewSet(viewsets.ModelViewSet):
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Master'

    def get_permissions(self):

        if self.action == 'list_expertise' or self.action == 'list_ourclient':
            print("\n in self action")
            return [AllowAny(), ] 
        return super(MasterViewSet, self).get_permissions()

    @action(detail = False,methods=['post'])
    def add_expertise(self,request):
        data = request.data.copy()
        expertise_id = data.get("expertise_id",None)
        try:
            if 'image' in request.FILES:
                image = request.FILES.get('image')
                file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'expertise/',image)
                data['expertise_image'] = file
            if expertise_id:
                queryset = Expertise.objects.get(uid=expertise_id)
                serializer_obj = ExpertiseSerializer(queryset,data=data)
            else:
                serializer_obj = ExpertiseSerializer(data=data)

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
    def list_expertise(self,request):
        data = request.data.copy()
        q_field = ['id']
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        try:
            resp_data = common_list_data(request, data, q_field, ExpertiseDeatilSerializer, Expertise,orderfilter)
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
        


    
    @action(detail = False,methods=['post'])
    def add_ourclient(self,request):
        data = request.data.copy()
        client_id = data.get("client_id",None)
        try:
            if 'image' in request.FILES:
                image = request.FILES.get('image')
                file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'client/',image)
                data['client_image'] = file

            if client_id:
                queryset = OurClient.objects.get(uid=client_id)
                serializer_obj = OurClientSerializer(queryset,data=data)
            else:
                serializer_obj = OurClientSerializer(data=data)

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
    def list_ourclient(self,request):
        data = request.data.copy()
        q_field = ['id']
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        try:
            resp_data = common_list_data(request, data, q_field, OurClientDetailSerializer, OurClient,orderfilter)
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

           
      


