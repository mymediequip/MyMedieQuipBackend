import os
import math

from django.db import connection, transaction
import datetime
import pytz
from decimal import Decimal
import json
import random
import string
from django.utils import timezone
import calendar
import time
import linecache
import sys

# For execute Raw Queries #####
from mmq.encryption import encrypt,decrypt

from django.conf import settings
from uuid import UUID


def sql_select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    list = []
    i = 0
    for row in results:
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field + 1
            except IndexError as e:
                break
        i = i + 1
        list.append(dict)
    return list


# ---------- Work for all api response -----------------#
from django.template.response import SimpleTemplateResponse
from rest_framework.response import Response
from django.urls import resolve


class CustomeResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(
            self,
            request=None,
            comment=None,
            log_data=None,
            message=None,
            encrypted=None,
            data=None,
            status=None,
            template_name=None,
            headers=None,
            exception=False,
            content_type=None,
            validate_errors=None,
            already_exist=None,
            ExtraParam=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        # db.log.remove()
        page = resolve(request.path_info).url_name if request is not None else ""
        module = resolve(request.path).app_name if request is not None else ""
        # print("########################################Respdata", data)
        super(Response, self).__init__(None, status=status)
        tempData = {}

        if status:
            tempData['status_code'] = status

        if log_data:
            comment = str(log_data)
        else:
            comment = str(comment)

        try:
            user_log = db.log.insert({"user_id":str(request.user) if request is not None else "", "module":module, "page":page, "comment":comment, "status":status, "ip_address":get_client_ip(request), "req_agent":request.META['HTTP_USER_AGENT'] if request is not None else "", "log_time":str(datetime.datetime.now())})
        except Exception as e:
            print("Could not add user log")
        

        # for x in db.log.find():
        #     print('>>>>>>>>>>>>',x)

        # -------- Condition for validate_errors ---------#
        #print(data,'>>>>>>>>>>>>>>>>>>>>>>>>>')
        errorStr = ''
        if validate_errors or already_exist:
            if 'msg' in data:
                tempData['message'] = data['msg']
            else:

                if isinstance(data, dict):
                    for val in data.items():
                        errorStr = errorStr + '$' + \
                            str(val[1][0])
                        break
                    errorStr = errorStr[1:]
                    tempData['message'] = errorStr

                else:
                    tempData['message'] = str(data) if message is None or message == '' else message
            if already_exist:
                tempData['status'] = True
            else:
                tempData['status'] = False
            tempData['data'] = {}
            tempData['encoded'] = {"data":False}
        else:
            tempData['message'] = message
            if tempData['status_code']==200:
                if not encrypted:
                    tempData['data'] = data
                    tempData['encoded'] = {"data":False}
                else:
                    data = json.dumps(data, cls=UUIDEncoder)
                    tempData['data'] = encrypt(str(data).replace('null', '""'))
                    print("tempData",tempData)
                    tempData['encoded'] = {"data":True}
            else:
                tempData['data'] = data
                tempData['encoded'] = {"data":False}

            tempData['status'] = True
        # for pagination put count,next,previous in upper dictionary level
        if ExtraParam:
           for key,val in ExtraParam.iteritems():
               tempData[key] =  val   
        # -------  End ----------------------------------------#
        # assign current time stamp
        tempData['currentTimeStamp'] = pytz.utc.localize(
            datetime.datetime.now())
        # end

        # data = encrypt(data).decode('utf-8')

        # tempData = "hello"
        # self.data = encrypt(str(tempData))
        self.data = rem_none(tempData)


        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


def rem_none(d):
    for key, value in list(d.items()):
        if value is None:
            d[key] = ""
        elif isinstance(value, dict):
            rem_none(value)
    return d  # For convenience

class SimpleResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(
            self,
            data=None,
            status=None,
            template_name=None,
            headers=None,
            exception=False,
            content_type=None,
            validate_errors=None,
            already_exist=None,ExtraParam=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        tempData = {}

        if status:
            tempData['status_code'] = status

        # -------- Condition for validate_errors ---------#
        errorStr = ''
        if validate_errors or already_exist:
            if 'msg' in data:
                # tempData['data'] = data['msg']
                tempData['msg'] = data['msg']
            else:

                if isinstance(data, dict):
                    for val in data.items():
                        errorStr = errorStr + '$' + \
                            str(val[1][0])
                        break
                    errorStr = errorStr[1:]
                    # tempData['data'] = errorStr
                    tempData['msg'] = errorStr

                else:
                    tempData['data'] = str(data)
            if already_exist:
                tempData['status'] = True
            else:
                tempData['status'] = False
        else:
            
            #new addition
            
            if data:
                if 'msg' in data:
                    tempData['msg'] = data['msg']
                else:
                    tempData['data'] = data
            else:
                pass
            #end

            tempData['status'] = True

        # for pagination put count,next,previous in upper dictionary level
        if ExtraParam:
           # for key,val in ExtraParam.iteritems():
           for key,val in ExtraParam.items():
               tempData[key] =  val   
        # -------  End ----------------------------------------#
        # assign current time stamp
        tempData['currentTimeStamp'] = pytz.utc.localize(
            datetime.datetime.now())
        # end
        self.data = tempData

        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


def rawResponse(msg=None, status=False, status_code=404):
    data = {}
    if msg:
        data['data'] = msg
        data['status'] = status
        data['status_code'] = status_code
    return data

#------------------ End ----------------------------------#
                     
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        
        if isinstance(obj, datetime.datetime):
            try:
                new_date = obj.strftime(settings.FRONT_DATE_FORMATE + " %H:%M:%S")
                if "00:00:00" in new_date:  # if "00:00:00" in date then extract from it
                    return new_date.split(" ")[0]
                else:
                    return new_date
            except Exception as e:
                return str(obj)

        if isinstance(obj, datetime.date):
            try:
                return obj.strftime(settings.FRONT_DATE_FORMATE)
                #return datetime.datetime.strptime(str(obj), "%Y-%m-%d").strftime(settings.FRONT_DATE_FORMATE)
            except Exception as e:
                return str(obj)

        if isinstance(obj, Decimal):
            s = str(Decimal(obj))
            return s.rstrip('0').rstrip('.') if '.' in s else s

        if isinstance(obj, ObjectId):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)

        return json.JSONEncoder.default(self, obj)


def printException(): # this function is used for printing error on which line no and what error occured
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    error_str = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print(error_str)
    return error_str



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') if request is not None else ""
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') if request is not None else ""
    return ip


def getCurrentTimeStamp():
    return timezone.now().strftime('%d%m%Y%H%M%S%f')



def concate_file_name_with_timezone(fileName):
    fileName = str(fileName)
    fileName = fileName.replace(" ", "_")
    file_arr = fileName.split('.')[0:-1]
    file_name = ".".join(file_arr)
    file_extension = fileName.split('.')[-1]
    current_time = getCurrentTimeStamp()
    final_final_name = file_name+"_"+current_time+"."+file_extension
    return final_final_name

def handle_uploaded_file(f, path, on_upload="local"):
    
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    
def file_save_by_source(request, path,filename=None,on_upload="local"):
          
    try:        
        if filename != None :  
            source = filename

        fileName = concate_file_name_with_timezone(source.name)
        filePath = path
        
        if not os.path.isdir(filePath):
            os.makedirs( filePath, 493 )
        handle_uploaded_file(source, filePath + '/'+ fileName, on_upload=on_upload)
        
        return fileName

    except Exception as e:
        print(e)
        return ""


def remove_file(request,path,filename):
    try:
        filepath = path+filename

        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print("The file does not exist")

        return True

    except Exception as e:
        print(e)
        return False
            