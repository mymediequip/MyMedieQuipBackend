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



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    name = 'Product'

    @action(detail = False,methods=['post'])
    def add(self,request):
        data = request.data.copy()
        product_id = data.get("product_id",None)
        try:
            if product_id:
                queryset = Product.objects.get(id=product_id)
                serializer_obj = ProductSerializer(queryset,data=data)
            else:
                serializer_obj = ProductSerializer(data=data)

            if serializer_obj.is_valid():
                save = serializer_obj.save()
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
            queryset = Product.objects.filter(status=1)
            serializer_obj = ProductSerializer(queryset,many=True)
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







