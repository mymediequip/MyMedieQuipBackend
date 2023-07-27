import os
import re
import datetime
import shutil

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status

# serializer_context is used for context paramer for serializer and its value will in dict format
def common_list_data(request, data, q_fields, serializer_name, model_name, order_by_field=None, distinct_fields=None, all=True, serializer_context=None,multiple_exclude_field=None, qlist_date_fields=[]):
    if request.user.is_superuser or all is True:
        querysets = model_name.objects.filter()
    else:
        querysets = model_name.objects.filter(
            created_by_id=request.user.uid).all()

    # querysets = model_name.objects.filter()

    # print(data,"....date")
    if 'to_date' in data.keys() and 'from_date' in data.keys():
        try:
            querysets = querysets.filter(created_date__gte=data['from_date'],created_date__lte=data['to_date'])
        except Exception as e:
            print(e)

    for key, value in data.items():

        if key == '_page' or key == '_limit':
            pass
        elif key == 'exclude_field':
            pass
        elif key == 'exclude':
            if isinstance(value, list):
                filter_arr = {data["exclude_field"]+'__in': value}
            else:
                filter_arr = {data["exclude_field"]: value}

            try:
                querysets = querysets.exclude(**filter_arr)
            except Exception as e:
                pass
        elif key == 'q' and value != "":
            if isinstance(value, list):
                filter_arr = {}
                if len(value) > 0:
                    for inner_item in value:
                        if len(inner_item) > 0 and inner_item["search_value"] != "":
                            if inner_item["search_by"] in qlist_date_fields:
                                date_value = datetime.datetime.strptime(
                                    inner_item["search_value"], settings.FRONT_DATE_FORMATE)
                                filter_arr[inner_item["search_by"]
                                           ] = date_value
                            else:
                                filter_arr[inner_item["search_by"]
                                           ] = inner_item["search_value"]
                    querysets = querysets.filter(**filter_arr)
            else:
                # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>q")
                queries = [Q(**{field+'__icontains': value})
                           for field in q_fields]
                print("queries",queries)
                query = queries.pop()
                print("query",query)
                for item in queries:
                    query |= item
                print("query",query)

                querysets = querysets.filter(query)
            # print(">>>>>>>>>>>>>>>>>>:",querysets)
        else:
            if isinstance(value, list):
                filter_arr = {key+'__in': value}
            else:
                # print(">>>>>>>>>>>>>>>>>....else")
                filter_arr = {key: value}

            try:
                querysets = querysets.filter(**filter_arr)
            except Exception as e:
                pass

    if multiple_exclude_field:
        querysets = querysets.exclude(**multiple_exclude_field)
            


    if order_by_field is not None:
        querysets = querysets.order_by(order_by_field)

    if distinct_fields is not None:
        querysets = querysets.distinct(*distinct_fields)

    #print(querysets.query, "ttttttttttttt")
    if '_page' in data.keys() and '_limit' in data.keys():
        page = data['_page']
        per_page = data['_limit']
        paginator = Paginator(querysets, per_page)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            return {"page": page, "per_page": per_page, "total": paginator.count, "total_pages": paginator.num_pages, "data": []}

        serializer = serializer_name(queryset, many=True)
        response_data = {"page": page, "per_page": per_page, "total": paginator.count,
                         "total_pages": paginator.num_pages, "data": serializer.data}
    else:
        if serializer_context is None:
            serializer = serializer_name(querysets, many=True)
        else:
            serializer = serializer_name(
                querysets, many=True, context=serializer_context)
        response_data = {"data": serializer.data}
    # print(querysets.query)
    return response_data

