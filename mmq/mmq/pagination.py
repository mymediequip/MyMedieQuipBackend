import os
import re
import datetime
import shutil

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status


def pagination(request, data, serializer_name,querysets):
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
        response_data = {"page": page, "per_page": per_page, "total":paginator.count,"total_pages": paginator.num_pages, "data": serializer.data}
        return response_data