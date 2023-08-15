import datetime
from django.conf import settings
from mmq_apps.users.models import User


def backendDateFormat(request, date):
    date_check = bool(date)
    print(date,'-??????????date')
    if date_check == True:
        date = datetime.datetime.strptime(date, settings.FRONT_DATE_FORMATE).strftime(settings.BACKEND_DATE_FORMATE)
        return date
    else:
        date = None
        return date


def checkDateFormat(request, date):
    try:
        return datetime.datetime.strptime(date, settings.FRONT_DATE_FORMATE).strftime(settings.BACKEND_DATE_FORMATE)
    except Exception as e:
        return CustomeResponse(request=request, log_data=json.dumps(str(e), cls=UUIDEncoder), comment="Date Format Error", message="Date Format Error", data=json.dumps({}, cls=UUIDEncoder),status=status.HTTP_400_BAD_REQUEST,validate_errors=1)


class CommonClass():
    
    def getUserType(self, user_type_id):
        user_type_obj = UserType.objects.filter(id=user_type_id).values('user_type')
        if len(user_type_obj):
            return user_type_obj[0]['user_type']
        else:
            return None


    

    