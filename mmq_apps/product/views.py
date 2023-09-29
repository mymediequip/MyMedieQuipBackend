import hashlib
#Django Rest Framework Import
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
import rest_framework.status as status


#Djagno Import
from django.conf import settings

from django.utils.translation import gettext as _
from django.db.models import Q
from mmq.functions import *
from mmq.services.users.otp_management import *
from mmq.token_authentication import ExpiringTokenAuthentication
from .models import *
from .serializers import *
from mmq.common_list_data import common_list_data
from mmq.functions import *


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Equipment'

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        equipment_id = data.get("equipment_id",None)
        print(type(data['category']))
        cate = data.get('category')
        cat = cate.split(',')
        print(cat)
        data['category'] = cat
        print(data,"data")
        try:
            if equipment_id:
                queryset = Equipment.objects.get(id=equipment_id)
                serializer_obj = EquipmentSerializer(queryset,data=data)
            else:
                serializer_obj = EquipmentSerializer(data=data)

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
        q_field = ["name"]
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        
        try:
            resp_data = common_list_data(request, data, q_field, EquipmentSerializer, Equipment,orderfilter)
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
        

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    permission_classes = (IsAuthenticated,)
    name = 'Speciality'

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        speciality_id = data.get("speciality_id",None)
        try:
            if speciality_id:
                queryset = Speciality.objects.get(id=speciality_id)
                serializer_obj = SpecialitySerializer(queryset,data=data)
            else:
                serializer_obj = SpecialitySerializer(data=data)

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
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def lists(self,request):
        data = request.data.copy()
        q_field = ["name"]
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        
        try:
            resp_data = common_list_data(request, data, q_field, SpecialitySerializer, Speciality,orderfilter)
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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Product'


    def get_permissions(self):

        if self.action == 'plists' or self.action == 'filter_list':
            print("\n in self action")
            return [AllowAny(), ] 
        return super(ProductViewSet, self).get_permissions()


    @action(detail = False,methods=['post'])
    def plists(self,request):
        data = request.data.copy()
        q_field = ["equip_name"]
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        
        try:
            resp_data = common_list_data(request, data, q_field, ProductDetailSerializer, Product,orderfilter)
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
    def add(self,request):
        data = request.data.copy()
        product_id = data.get("product_id",None)
        post_type= data.get('post_type')
        data['user'] = request.user.uid
        if not post_type:
            return SimpleResponse(
                    {"msg":"post_type is required field"},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        

        try:
            if product_id:
                queryset = Product.objects.get(id=product_id)
                serializer_obj = ProductSerializer(queryset,data=data)
            else:
                serializer_obj = ProductSerializer(data=data)

            if serializer_obj.is_valid():
                add = serializer_obj.save()
                image = {}
                video = {}
                if 'images' in request.FILES:
                    files = request.FILES.getlist('images')
                    for f in files:
                        file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'product/image/',f)
                        print(file)
                        if file:
                            image.update({"product":add.uid,"p_image":file})
                            image_serializer_obj = ProductImageSerializer(data=image)
                            try:
                                if image_serializer_obj.is_valid():
                                    image_serializer_obj.save()
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

                        print("msg",msg)


                if 'videos' in request.FILES:
                    files = request.FILES.getlist('videos')
                    for f in files:
                        file = file_save_by_source(request,settings.FILE_UPLOAD_PATH+'product/video/',f)
                        print(file)
                        if file:
                            video.update({"product":add.uid,"video":file})
                            video_serializer_obj = ProductVideoSerializer(data=video)
                            try:
                                if video_serializer_obj.is_valid():
                                    video_serializer_obj.save()
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

                        print("msg",msg)
                
               
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
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def lists(self,request):
        data = request.data.copy()
        q_field = ["equip_name"]
        orderfilter = '-id'
        data['user'] = request.user.uid
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        
        try:
            resp_data = common_list_data(request, data, q_field, ProductDetailSerializer, Product,orderfilter)
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
    def filter_list(self,request):
        data = request.data.copy()
        q_field = ["equip_name"]
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        list_data = {}
        # data['exclude'] = {"user":}
        
        try:
            resp_data = common_list_data(request, data, q_field, ProductDetailSerializer, Product,orderfilter)
            list_data = {
            "new_products":resp_data['data'],
            "featured_products":resp_data['data'],
            "best_seller_products":resp_data['data']
            }


            return SimpleResponse(
                        {"data":list_data},
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
    def details(self,request):
        data = request.data.copy()
        product_id = data.get("product_id")
        
        try:
            if product_id:
                queryset = Product.objects.get(uid=product_id)
                serializer_obj = ProductDetailSerializer(queryset)
                return SimpleResponse(
                            {"data":serializer_obj.data},
                            status=status.HTTP_200_OK
                )
            else:
                return SimpleResponse(
                    {"msg":"product_id is required field"},
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
    def schedule_meeting(self,request):
        data=request.data.copy()
        try:
            serializer_obj=ScheduleMeetingSerializer(data=data)
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
        


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Product'

    def get_permissions(self):

        if self.action == 'menulist' or self.action == 'search_category' or self.action == 'forgot_password' or self.action == 'reset_password':
            print("\n in self action")
            return [AllowAny(), ] 
        return super(CategoryViewSet, self).get_permissions()

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        category_id = data.get("category_id",None)
        try:
            if category_id:
                queryset = Category.objects.get(id=category_id)
                serializer_obj = CategorySerializer(queryset,data=data)
            else:
                serializer_obj = CategorySerializer(data=data)

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
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def lists(self,request):
        data = request.data.copy()
        try:
            queryset = Category.objects.filter(status=1)
            serializer_obj = CategoryListSerializer(queryset,many=True)
            return SimpleResponse(
                        {"data":serializer_obj.data},
                        status=status.HTTP_200_OK
                    )            

        except Exception as e:
            print("Error",str(e))
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def menulist(self,request):
        data = request.data.copy()
        q_field = ["name"]
        orderfilter = '-id'
        sort = data.get('sort',None)
        if sort =='asc':
            orderfilter = 'id'
        if 'q' not in data and 'name' not in data and 'id' not in data and 'parent' not in data:
            data['parent'] = None

        print(data)
        try:
            resp_data = common_list_data(request, data, q_field, CategorySerializer, Category,orderfilter)
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
    def search_category(self,request):
        data = request.data.copy()
        category_id = data.get("id",None)
        search = data.get('search',None)
        try:
            if category_id:
                queryset = Category.objects.filter(id=category_id)
            else:
                queryset = Category.objects.filter(parent=None)
            serializer_obj = CategorySerializer(queryset,many=True)
            
            return SimpleResponse(
                        {"data":serializer_obj.data},
                        status=status.HTTP_200_OK
                    )            

        except Exception as e:
            print("Error",str(e))
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
        
        

    @action(detail = False,methods=['post'])
    def parentlist(self,request):
        data = request.data.copy()
        try:
            queryset = Category.objects.filter(parent=None)
            serializer_obj = CategoryListSerializer(queryset,many=True)
            return SimpleResponse(
                        {"data":serializer_obj.data},
                        status=status.HTTP_200_OK
                    )            

        except Exception as e:
            print("Error",str(e))
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
        
    
    @action(detail = False,methods=['post'])
    def subcategorylist(self,request):
        data = request.data.copy()
        parent_id = data.get('parent_id')
        try:
            queryset = Category.objects.filter(parent=parent_id)
            serializer_obj = CategoryListSerializer(queryset,many=True)
            return SimpleResponse(
                        {"data":serializer_obj.data},
                        status=status.HTTP_200_OK
                    )            

        except Exception as e:
            print("Error",str(e))
            return SimpleResponse(
                    {"msg":str(e)},
                    status= status.HTTP_400_BAD_REQUEST,
                    validate_errors =1
                )
# class ScheduleMeetingViewSet(viewsets.ModelViewSet):
#     queryset = ScheduleMeeting.objects.all()
#     serializer_class = ScheduleMeetingSerializer
#     permission_classes = (IsAuthenticated,)
#     name = 'ScheduleMeeting'

#     #  def get_permissions(self):

#         # if self.action == 'schedule_meeting':
#         #     print("\n in self action")
#         #     return [AllowAny(), ] 
#         # return super(ScheduleMeetingViewSet, self).get_permissions()

    

#     @action(detail = False,methods=['post'])
#     def schedule_meeting(request):
#         data=request.data()
#         try:
#             serializer_obj=ScheduleMeetingSerializer(data=data)
#             if serializer_obj.is_valid():
#                 serializer_obj.save()
#                 return SimpleResponse(
#                         {"data":serializer_obj.data},
#                         status=status.HTTP_200_OK
#                     )
#             else:
#                 return SimpleResponse(
#                     {"msg":str(serializer_obj.errors)},
#                     status= status.HTTP_400_BAD_REQUEST,
#                     validate_errors =1
#                 )
                
#         except Exception as e:
#             print("Error",str(e))
#             printException()
#             return SimpleResponse(
#                     {"msg":str(e)},
#                     status= status.HTTP_400_BAD_REQUEST,
#                     validate_errors =1
#                 )







