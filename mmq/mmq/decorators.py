import os
from django.conf import settings
from mmq.functions import *
import rest_framework.status as status

# User Permission decorators

def isAdminLogin(func): 
    def checkAdmin(request):
        if request.user.user_type.id != 1:
            return CustomeResponse(request=request, comment="Only Admin User Allowed", message="Only Admin User Allowed", data=json.dumps({}, cls=UUIDEncoder), status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        return func(request)
    return checkAdmin


def isCustomerLogin(func): 
    def checkCustomer(request):
        if request.user.user_type.id != 2:
            return CustomeResponse(request=request, comment="Only Customer User Allowed", message="Only Admin User Allowed", data=json.dumps({}, cls=UUIDEncoder), status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        return func(request)
    return checkCustomer

def isMerchantLogin(func): 
    def checkMerchant(request):
        if request.user.user_type.id != 3:
            return CustomeResponse(request=request, comment="Only Merchant User Allowed", message="Only Admin User Allowed", data=json.dumps({}, cls=UUIDEncoder), status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        return func(request)
    return checkMerchant