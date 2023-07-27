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


    def countCustomerProvider(request, pass_dict):
        provider_count = 0
        customer_count = 0
        provider_obj = []
        try:
            filter_data = {}

            if 'year' in pass_dict:
                filter_data = {'created_date__year':pass_dict['year']}
            if 'month' in pass_dict:
                filter_data = {'created_date__year':pass_dict['year'], 'created_date__month':pass_dict['month']}
            if 'day' in pass_dict:
                filter_data = {'created_date__year':pass_dict['year'], 'created_date__month':pass_dict['month'], 'created_date__day':pass_dict['day']}

            if 'one_week_ago' in pass_dict and 'today_date' in pass_dict:
                filter_data = {'created_date__gte':pass_dict['one_week_ago'], 'created_date__lte':pass_dict['today_date']}

            try:
                print(filter_data,'-----------filter_data')
                provider_obj = User.objects.filter(**filter_data).all()
                print(provider_obj,'-----------provider_obj')
            except Exception as e:
                print(e,'-----------error')
            if 'all_data' in pass_dict and pass_dict['all_data'] == 'all':
                try:
                    provider_obj = User.objects.all()
                except Exception as e:
                    print(e, 'error????????')
            if len(provider_obj)>0:
                for provider in provider_obj:
                    if provider.user_type.id == 3:
                        provider_count = provider_count+1
                    if provider.user_type.id == 2:
                        customer_count = customer_count+1
            resp_data = {'customer_count':customer_count, 'provider_count':provider_count} 
            return resp_data
        except Exception as e:
            print(e,'----error')


    